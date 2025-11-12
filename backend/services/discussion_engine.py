"""Discussion flow control engine"""
import uuid
import asyncio
from typing import List, Dict, Callable, Awaitable, Optional
from collections import Counter
from models.discussion import DiscussionSession, AgendaItem, DiscussionPhase
from models.agent import Agent
from models.message import Message, Opinion, MessageType
from services.facilitator import Facilitator
from services.agent_manager import AgentManager
from services.context_retriever import ContextRetriever
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DiscussionEngine:
    """Discussion flow control engine"""

    def __init__(
        self,
        facilitator: Facilitator,
        agent_manager: AgentManager,
        message_callback: Callable[[Dict], Awaitable[None]],
        context_retriever: Optional[ContextRetriever] = None,
    ):
        self.facilitator = facilitator
        self.agent_manager = agent_manager
        self.message_callback = message_callback
        self.context_retriever = context_retriever or ContextRetriever()
        self.session: Optional[DiscussionSession] = None
        self.agents: List[Agent] = []
        self.background_context: str = ""

    async def start_discussion(self, topic: str) -> DiscussionSession:
        """Start discussion"""
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        self.session = DiscussionSession(
            id=session_id,
            topic=topic,
        )

        await self._send_event("discussion_started", {
            "discussion_id": session_id,
            "topic": topic,
        })

        # Initialize facilitator
        self.facilitator.initialize()

        # Retrieve background knowledge
        await self._send_message(
            agent=self.facilitator.agent,
            content="Collecting relevant background knowledge...",
            message_type=MessageType.SYSTEM,
        )

        context_items = await self._retrieve_background_context(topic)
        self.background_context = self.context_retriever.format_contexts_for_prompt(context_items)

        if context_items:
            await self._send_event("context_retrieved", {
                "count": len(context_items),
                "sources": list(set(ctx.source for ctx in context_items)),
            })
            await self._send_message(
                agent=self.facilitator.agent,
                content=f"Retrieved {len(context_items)} pieces of relevant information",
                message_type=MessageType.SYSTEM,
            )

        # Create agenda
        self.session.phase = DiscussionPhase.AGENDA_CREATION
        await self._send_message(
            agent=self.facilitator.agent,
            content="Starting discussion. First, creating agenda...",
            message_type=MessageType.SYSTEM,
        )

        # Disable streaming for now (prioritize stability)
        agenda = await self.facilitator.create_agenda_with_context(
            topic,
            self.background_context,
            on_stream=None,
        )
        self.session.agenda = agenda

        await self._send_event("agenda_created", {
            "agenda": [item.model_dump() for item in agenda],
        })

        # Generate agents
        self.session.phase = DiscussionPhase.AGENT_GENERATION
        await self._send_message(
            agent=self.facilitator.agent,
            content="Selecting participants...",
            message_type=MessageType.SYSTEM,
        )

        self.agents = await self.facilitator.generate_agents(topic, agenda)

        await self._send_event("agents_created", {
            "agents": [agent.model_dump() for agent in self.agents],
        })

        # Discuss each agenda item
        for idx, agenda_item in enumerate(self.session.agenda):
            self.session.current_agenda_index = idx
            await self._discuss_agenda_item(agenda_item)

        # Discussion complete
        self.session.phase = DiscussionPhase.COMPLETED
        await self._send_message(
            agent=self.facilitator.agent,
            content=f"Agreement has been reached on all agenda items.",
            message_type=MessageType.SYSTEM,
        )

        await self._send_event("discussion_completed", {
            "final_conclusion": self._generate_final_conclusion(),
        })

        return self.session

    async def _discuss_agenda_item(self, agenda_item: AgendaItem):
        """Discuss individual agenda item"""
        await self._send_message(
            agent=self.facilitator.agent,
            content=f"Agenda {agenda_item.order}: {agenda_item.title}",
            message_type=MessageType.SYSTEM,
        )

        # Phase 1: Independent opinions
        opinions = await self._run_independent_opinions_phase(agenda_item)

        # Phase 2: Voting
        opinions = await self._run_voting_phase(opinions)

        # Phase 3: Persuasion process
        conclusion = await self._run_persuasion_phase(opinions, agenda_item)

        agenda_item.conclusion = conclusion
        await self._send_event("agenda_completed", {
            "agenda_index": self.session.current_agenda_index,
            "conclusion": conclusion,
        })

    async def _run_independent_opinions_phase(self, agenda_item: AgendaItem) -> List[Opinion]:
        """Phase 1: Independent opinions"""
        self.session.phase = DiscussionPhase.INDEPENDENT_OPINIONS

        await self._send_event("phase_changed", {
            "phase": "independent_opinions",
            "agenda_index": self.session.current_agenda_index,
        })

        await self._send_message(
            agent=self.facilitator.agent,
            content="Each participant will state their opinion independently.",
            message_type=MessageType.SYSTEM,
        )

        # Generate opinions from all agents in parallel (passing background knowledge)
        tasks = []
        for agent in self.agents:
            task = self.agent_manager.generate_independent_opinion(
                agent=agent,
                agenda_title=agenda_item.title,
                agenda_description=agenda_item.description,
                background_context=self.background_context,
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        opinions = []
        for idx, (content, response_id) in enumerate(results):
            agent = self.agents[idx]
            opinion = Opinion(
                id=f"opinion_{uuid.uuid4().hex[:8]}",
                agent_id=agent.id,
                agent_name=agent.name,
                content=content,
            )
            opinions.append(opinion)

            await self._send_message(
                agent=agent,
                content=content,
                message_type=MessageType.OPINION,
            )

        logger.info(f"{len(opinions)} opinions submitted")
        return opinions

    async def _run_voting_phase(self, opinions: List[Opinion]) -> List[Opinion]:
        """Phase 2: Voting"""
        self.session.phase = DiscussionPhase.VOTING

        await self._send_event("phase_changed", {
            "phase": "voting",
            "agenda_index": self.session.current_agenda_index,
        })

        await self._send_message(
            agent=self.facilitator.agent,
            content="Starting voting.",
            message_type=MessageType.SYSTEM,
        )

        # Vote from all agents in parallel
        tasks = []
        for agent in self.agents:
            task = self.agent_manager.vote_for_opinion(agent=agent, opinions=opinions)
            tasks.append(task)

        votes = await asyncio.gather(*tasks)

        # Aggregate voting results (record who voted for which opinion)
        vote_counter = Counter(votes)
        vote_details = []  # Detailed voting information
        for idx, voted_opinion_id in enumerate(votes):
            voter = self.agents[idx]
            vote_details.append({
                "voter_id": voter.id,
                "voter_name": voter.name,
                "opinion_id": voted_opinion_id,
            })

        for opinion in opinions:
            opinion.votes = vote_counter.get(opinion.id, 0)

        # Keep only opinions with at least 1 vote
        filtered_opinions = [op for op in opinions if op.votes > 0]

        # Send with detailed opinion information
        await self._send_event("voting_result", {
            "votes": {op.id: op.votes for op in opinions},
            "vote_details": vote_details,
            "opinions": [
                {
                    "id": op.id,
                    "agent_id": op.agent_id,
                    "agent_name": op.agent_name,
                    "content": op.content,
                    "votes": op.votes,
                }
                for op in opinions
            ],
            "remaining_opinions": len(filtered_opinions),
        })

        logger.info(f"Voting complete: {len(filtered_opinions)} opinions remaining")
        return filtered_opinions

    async def _run_persuasion_phase(self, opinions: List[Opinion], agenda_item: AgendaItem) -> str:
        """Phase 3: Persuasion process"""
        self.session.phase = DiscussionPhase.PERSUASION

        await self._send_event("phase_changed", {
            "phase": "persuasion",
            "agenda_index": self.session.current_agenda_index,
        })

        if len(opinions) == 1:
            return opinions[0].content

        # Record which opinion each agent supports
        agent_opinions = {op.agent_id: op for op in opinions}

        # Persuade in order from minority opinions
        max_rounds = 10
        for round_num in range(max_rounds):
            opinions_sorted = sorted(opinions, key=lambda x: x.votes)

            for opinion in opinions_sorted:
                persuader = self.agent_manager.get_agent(opinion.agent_id)

                # Persuade
                persuasion_msg, _ = await self.agent_manager.persuade(persuader, opinion)
                await self._send_message(
                    agent=persuader,
                    content=persuasion_msg,
                    message_type=MessageType.PERSUASION,
                )

                # Other agents respond
                counter_arguments = []
                for agent in self.agents:
                    if agent.id != persuader.id:
                        # Get the opinion each agent supports and other opinions
                        your_opinion = agent_opinions.get(agent.id).content if agent.id in agent_opinions else ""
                        other_opinions_list = [op.content for op in opinions if op.agent_id != agent.id]

                        response_msg, _, is_agreement = await self.agent_manager.respond_to_persuasion(
                            agent, persuasion_msg, your_opinion, other_opinions_list
                        )
                        await self._send_message(
                            agent=agent,
                            content=response_msg,
                            message_type=MessageType.RESPONSE,
                        )

                        # Record if there's a counter-argument
                        if not is_agreement:
                            counter_arguments.append((agent, response_msg))

                # If there are counter-arguments, original opinion holder responds
                if counter_arguments:
                    for counter_agent, counter_msg in counter_arguments:
                        rebuttal_msg, _, maintains = await self.agent_manager.respond_to_counter_argument(
                            persuader, counter_msg, opinion.content
                        )
                        await self._send_message(
                            agent=persuader,
                            content=rebuttal_msg,
                            message_type=MessageType.RESPONSE,
                        )

                # Check consensus
                if await self._check_consensus(opinion):
                    await self._send_message(
                        agent=self.facilitator.agent,
                        content=f"Consensus has been reached!",
                        message_type=MessageType.CONCLUSION,
                    )
                    return opinion.content

        return opinions[0].content

    async def _check_consensus(self, opinion: Opinion) -> bool:
        """Check consensus from all participants"""
        tasks = []
        for agent in self.agents:
            task = self.agent_manager.make_final_decision(
                agent=agent,
                proposed_opinion=opinion.content,
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return all(agrees for agrees, _ in results)

    async def _send_message(
        self,
        agent: Agent,
        content: str,
        message_type: MessageType,
    ):
        """Send message"""
        message = Message(
            id=f"msg_{uuid.uuid4().hex[:8]}",
            agent_id=agent.id,
            agent_name=agent.name,
            content=content,
            message_type=message_type,
            timestamp=datetime.now(),
        )

        await self.message_callback({
            "type": "message",
            "data": message.model_dump(mode="json"),
        })

    async def _send_event(self, event_type: str, data: dict):
        """Send event"""
        await self.message_callback({
            "type": event_type,
            "data": data,
        })

    async def _retrieve_background_context(self, topic: str) -> list:
        """Retrieve background knowledge from discussion topic"""
        try:
            # Extract keywords from topic (simplified version)
            keywords = self._extract_keywords(topic)

            # Retrieve context
            context_items = await self.context_retriever.retrieve_context(topic, keywords)
            return context_items

        except Exception as e:
            logger.error(f"Error retrieving background context: {e}")
            return []

    def _extract_keywords(self, topic: str) -> List[str]:
        """Extract keywords from topic (simplified version)"""
        # TODO: Implement more sophisticated keyword extraction
        # Currently just split by spaces
        keywords = [word.strip() for word in topic.split() if len(word.strip()) > 2]
        return keywords[:5]  # Maximum 5 keywords

    def _generate_final_conclusion(self) -> str:
        """Generate final conclusion"""
        conclusions = [item.conclusion for item in self.session.agenda if item.conclusion]
        return "\n\n".join([
            f"{idx + 1}. {self.session.agenda[idx].title}: {conclusion}"
            for idx, conclusion in enumerate(conclusions)
        ])
