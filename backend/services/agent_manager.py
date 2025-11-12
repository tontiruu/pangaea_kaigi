"""Agent generation and management"""
import uuid
from typing import List, Dict, Optional
from models.agent import Agent, AgentRole
from models.message import Opinion
from services.openai_client import OpenAIResponsesClient
from utils.prompts import (
    AGENT_INDEPENDENT_OPINION,
    AGENT_VOTE,
    AGENT_PERSUASION,
    AGENT_RESPOND_TO_PERSUASION,
    AGENT_FINAL_DECISION,
)
import logging

logger = logging.getLogger(__name__)


class AgentManager:
    """Class for generating and managing Agents"""

    def __init__(self, openai_client: OpenAIResponsesClient):
        self.openai_client = openai_client
        self.agents: Dict[str, Agent] = {}

    def create_agent(self, name: str, perspective: str, role: AgentRole = AgentRole.PARTICIPANT) -> Agent:
        """Create a new Agent"""
        agent_id = f"agent_{uuid.uuid4().hex[:8]}"
        agent = Agent(
            id=agent_id,
            name=name,
            perspective=perspective,
            role=role,
        )
        self.agents[agent_id] = agent
        logger.info(f"Agent created: {agent.name} (ID: {agent.id})")
        return agent

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get Agent from Agent ID"""
        return self.agents.get(agent_id)

    def get_all_agents(self) -> List[Agent]:
        """Get all Agents"""
        return list(self.agents.values())

    async def generate_independent_opinion(
        self,
        agent: Agent,
        agenda_title: str,
        agenda_description: str,
        background_context: str = "",
    ) -> tuple[str, str]:
        """Have the Agent generate an independent opinion"""
        prompt = AGENT_INDEPENDENT_OPINION.format(
            name=agent.name,
            perspective=agent.perspective,
            agenda_title=agenda_title,
            agenda_description=agenda_description,
            background_context=background_context,
        )

        response = await self.openai_client.create_with_retry(
            input_text=prompt,
            previous_response_id=agent.response_id,
        )

        # Update response_id
        agent.response_id = response["id"]
        self.agents[agent.id] = agent

        logger.info(f"{agent.name} generated opinion")
        return response["content"], response["id"]

    async def vote_for_opinion(
        self,
        agent: Agent,
        opinions: List[Opinion],
    ) -> str:
        """Have the Agent vote for an opinion"""
        opinions_text = "\n\n".join([
            f"ID: {op.id}\nAgent: {op.agent_name}\nContent: {op.content}"
            for op in opinions
        ])

        prompt = AGENT_VOTE.format(
            name=agent.name,
            opinions=opinions_text,
        )

        response = await self.openai_client.create_with_retry(
            input_text=prompt,
            previous_response_id=agent.response_id,
        )

        agent.response_id = response["id"]
        self.agents[agent.id] = agent

        voted_opinion_id = response["content"].strip()
        logger.info(f"{agent.name} voted: {voted_opinion_id}")
        return voted_opinion_id

    async def persuade(
        self,
        agent: Agent,
        opinion: Opinion,
    ) -> tuple[str, str]:
        """Have the Agent perform persuasion"""
        prompt = AGENT_PERSUASION.format(
            name=agent.name,
            your_opinion=opinion.content,
        )

        response = await self.openai_client.create_with_retry(
            input_text=prompt,
            previous_response_id=agent.response_id,
        )

        agent.response_id = response["id"]
        self.agents[agent.id] = agent

        logger.info(f"{agent.name} started persuasion")
        return response["content"], response["id"]

    async def respond_to_persuasion(
        self,
        agent: Agent,
        persuasion_message: str,
        your_opinion: str,
        other_opinions: List[str],
    ) -> tuple[str, str, bool]:
        """Have the Agent respond to persuasion

        Returns:
            tuple[content, response_id, is_agreement]: Response content, response_id, whether agreed
        """
        other_opinions_text = "\n".join([f"- {op}" for op in other_opinions])

        prompt = AGENT_RESPOND_TO_PERSUASION.format(
            name=agent.name,
            your_opinion=your_opinion,
            other_opinions=other_opinions_text,
            persuasion_message=persuasion_message,
        )

        response = await self.openai_client.create_with_retry(
            input_text=prompt,
            previous_response_id=agent.response_id,
        )

        agent.response_id = response["id"]
        self.agents[agent.id] = agent

        content = response["content"]
        # Determine if it's agreement or counter-argument
        is_agreement = "Agree" in content or "agree" in content

        logger.info(f"{agent.name} responded: {'Agreement' if is_agreement else 'Counter-argument'}")
        return content, response["id"], is_agreement

    async def respond_to_counter_argument(
        self,
        agent: Agent,
        counter_argument: str,
        original_opinion: str,
    ) -> tuple[str, str, bool]:
        """The original opinion holder responds to a counter-argument

        Returns:
            tuple[content, response_id, maintains_position]: Response content, response_id, whether to maintain original opinion
        """
        prompt = f"""You are {agent.name}.

Your original opinion: {original_opinion}

The following counter-argument was made: {counter_argument}

Please state your thoughts on this counter-argument.
Indicate whether you will continue to support your original opinion or agree with the counter-argument, and state your reasons.

Output format:
Decision: [Support original opinion/Agree with counter-argument]
Reason: [Briefly state your thoughts]"""

        response = await self.openai_client.create_with_retry(
            input_text=prompt,
            previous_response_id=agent.response_id,
        )

        agent.response_id = response["id"]
        self.agents[agent.id] = agent

        content = response["content"]
        # Determine whether to maintain original opinion
        maintains_position = "Support" in content or "support" in content

        logger.info(f"{agent.name} responded to counter-argument: {'Maintains original opinion' if maintains_position else 'Agrees with counter-argument'}")
        return content, response["id"], maintains_position

    async def make_final_decision(
        self,
        agent: Agent,
        proposed_opinion: str,
    ) -> tuple[bool, str]:
        """Have the Agent make a final decision"""
        prompt = AGENT_FINAL_DECISION.format(
            name=agent.name,
            proposed_opinion=proposed_opinion,
        )

        response = await self.openai_client.create_with_retry(
            input_text=prompt,
            previous_response_id=agent.response_id,
        )

        agent.response_id = response["id"]
        self.agents[agent.id] = agent

        content = response["content"]
        agrees = "Yes" in content or "yes" in content

        logger.info(f"{agent.name}'s decision: {'Agree' if agrees else 'Disagree'}")
        return agrees, content
