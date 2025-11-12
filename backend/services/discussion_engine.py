"""議論フローを制御するエンジン"""
import uuid
import asyncio
from typing import List, Dict, Callable, Awaitable, Optional
from collections import Counter
from models.discussion import DiscussionSession, AgendaItem, DiscussionPhase
from models.agent import Agent
from models.message import Message, Opinion, MessageType
from services.facilitator import Facilitator
from services.agent_manager import AgentManager
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DiscussionEngine:
    """議論フローを制御するエンジン"""

    def __init__(
        self,
        facilitator: Facilitator,
        agent_manager: AgentManager,
        message_callback: Callable[[Dict], Awaitable[None]],
    ):
        self.facilitator = facilitator
        self.agent_manager = agent_manager
        self.message_callback = message_callback
        self.session: Optional[DiscussionSession] = None
        self.agents: List[Agent] = []

    async def start_discussion(self, topic: str) -> DiscussionSession:
        """議論を開始"""
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        self.session = DiscussionSession(
            id=session_id,
            topic=topic,
        )

        await self._send_event("discussion_started", {
            "discussion_id": session_id,
            "topic": topic,
        })

        # ファシリテーター初期化
        self.facilitator.initialize()

        # アジェンダ作成
        self.session.phase = DiscussionPhase.AGENDA_CREATION
        await self._send_message(
            agent=self.facilitator.agent,
            content="議論を開始します。まずアジェンダを作成します...",
            message_type=MessageType.SYSTEM,
        )

        agenda = await self.facilitator.create_agenda(topic)
        self.session.agenda = agenda

        await self._send_event("agenda_created", {
            "agenda": [item.model_dump() for item in agenda],
        })

        # Agent生成
        self.session.phase = DiscussionPhase.AGENT_GENERATION
        await self._send_message(
            agent=self.facilitator.agent,
            content="参加者を選定します...",
            message_type=MessageType.SYSTEM,
        )

        self.agents = await self.facilitator.generate_agents(topic, agenda)

        await self._send_event("agents_created", {
            "agents": [agent.model_dump() for agent in self.agents],
        })

        # 各アジェンダについて議論
        for idx, agenda_item in enumerate(self.session.agenda):
            self.session.current_agenda_index = idx
            await self._discuss_agenda_item(agenda_item)

        # 議論完了
        self.session.phase = DiscussionPhase.COMPLETED
        await self._send_message(
            agent=self.facilitator.agent,
            content=f"すべてのアジェンダについて合意が得られました。",
            message_type=MessageType.SYSTEM,
        )

        await self._send_event("discussion_completed", {
            "final_conclusion": self._generate_final_conclusion(),
        })

        return self.session

    async def _discuss_agenda_item(self, agenda_item: AgendaItem):
        """個別のアジェンダについて議論"""
        await self._send_message(
            agent=self.facilitator.agent,
            content=f"アジェンダ {agenda_item.order}: {agenda_item.title}",
            message_type=MessageType.SYSTEM,
        )

        # Phase 1: 独立した意見出し
        opinions = await self._run_independent_opinions_phase(agenda_item)

        # Phase 2: 投票
        opinions = await self._run_voting_phase(opinions)

        # Phase 3: 説得プロセス
        conclusion = await self._run_persuasion_phase(opinions, agenda_item)

        agenda_item.conclusion = conclusion
        await self._send_event("agenda_completed", {
            "agenda_index": self.session.current_agenda_index,
            "conclusion": conclusion,
        })

    async def _run_independent_opinions_phase(self, agenda_item: AgendaItem) -> List[Opinion]:
        """Phase 1: 独立した意見出し"""
        self.session.phase = DiscussionPhase.INDEPENDENT_OPINIONS

        await self._send_event("phase_changed", {
            "phase": "independent_opinions",
            "agenda_index": self.session.current_agenda_index,
        })

        await self._send_message(
            agent=self.facilitator.agent,
            content="各参加者が独立して意見を述べます。",
            message_type=MessageType.SYSTEM,
        )

        # 全Agent並列で意見生成
        tasks = []
        for agent in self.agents:
            task = self.agent_manager.generate_independent_opinion(
                agent=agent,
                agenda_title=agenda_item.title,
                agenda_description=agenda_item.description,
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

        logger.info(f"{len(opinions)}個の意見が提出されました")
        return opinions

    async def _run_voting_phase(self, opinions: List[Opinion]) -> List[Opinion]:
        """Phase 2: 投票"""
        self.session.phase = DiscussionPhase.VOTING

        await self._send_event("phase_changed", {
            "phase": "voting",
            "agenda_index": self.session.current_agenda_index,
        })

        await self._send_message(
            agent=self.facilitator.agent,
            content="投票を開始します。",
            message_type=MessageType.SYSTEM,
        )

        # 全Agent並列で投票
        tasks = []
        for agent in self.agents:
            task = self.agent_manager.vote_for_opinion(agent=agent, opinions=opinions)
            tasks.append(task)

        votes = await asyncio.gather(*tasks)

        # 投票結果を集計
        vote_counter = Counter(votes)
        for opinion in opinions:
            opinion.votes = vote_counter.get(opinion.id, 0)

        # 1票以上の意見のみ残す
        filtered_opinions = [op for op in opinions if op.votes > 0]

        await self._send_event("voting_result", {
            "votes": {op.id: op.votes for op in opinions},
            "remaining_opinions": len(filtered_opinions),
        })

        logger.info(f"投票完了: {len(filtered_opinions)}個の意見が残りました")
        return filtered_opinions

    async def _run_persuasion_phase(self, opinions: List[Opinion], agenda_item: AgendaItem) -> str:
        """Phase 3: 説得プロセス"""
        self.session.phase = DiscussionPhase.PERSUASION

        await self._send_event("phase_changed", {
            "phase": "persuasion",
            "agenda_index": self.session.current_agenda_index,
        })

        if len(opinions) == 1:
            return opinions[0].content

        # 少数派から順に説得
        max_rounds = 10
        for round_num in range(max_rounds):
            opinions_sorted = sorted(opinions, key=lambda x: x.votes)

            for opinion in opinions_sorted:
                persuader = self.agent_manager.get_agent(opinion.agent_id)

                # 説得
                persuasion_msg, _ = await self.agent_manager.persuade(persuader, opinion)
                await self._send_message(
                    agent=persuader,
                    content=persuasion_msg,
                    message_type=MessageType.PERSUASION,
                )

                # 他のAgentが応答
                for agent in self.agents:
                    if agent.id != persuader.id:
                        response_msg, _ = await self.agent_manager.respond_to_persuasion(
                            agent, persuasion_msg
                        )
                        await self._send_message(
                            agent=agent,
                            content=response_msg,
                            message_type=MessageType.RESPONSE,
                        )

                # 合意判定
                if await self._check_consensus(opinion):
                    await self._send_message(
                        agent=self.facilitator.agent,
                        content=f"全員の合意が得られました！",
                        message_type=MessageType.CONCLUSION,
                    )
                    return opinion.content

        return opinions[0].content

    async def _check_consensus(self, opinion: Opinion) -> bool:
        """全員の合意を確認"""
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
        """メッセージを送信"""
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
        """イベントを送信"""
        await self.message_callback({
            "type": event_type,
            "data": data,
        })

    def _generate_final_conclusion(self) -> str:
        """最終結論を生成"""
        conclusions = [item.conclusion for item in self.session.agenda if item.conclusion]
        return "\n\n".join([
            f"{idx + 1}. {self.session.agenda[idx].title}: {conclusion}"
            for idx, conclusion in enumerate(conclusions)
        ])
