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
from services.context_retriever import ContextRetriever
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

        # 背景知識の取得
        await self._send_message(
            agent=self.facilitator.agent,
            content="関連する背景知識を収集しています...",
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
                content=f"{len(context_items)}件の関連情報を取得しました",
                message_type=MessageType.SYSTEM,
            )

        # アジェンダ作成
        self.session.phase = DiscussionPhase.AGENDA_CREATION
        await self._send_message(
            agent=self.facilitator.agent,
            content="議論を開始します。まずアジェンダを作成します...",
            message_type=MessageType.SYSTEM,
        )

        # ストリーミングは一旦無効化（安定性優先）
        agenda = await self.facilitator.create_agenda_with_context(
            topic,
            self.background_context,
            on_stream=None,
        )
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

        # 全Agent並列で意見生成（背景知識を渡す）
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

        # 投票結果を集計（誰がどの意見に投票したかを記録）
        vote_counter = Counter(votes)
        vote_details = []  # 詳細な投票情報
        for idx, voted_opinion_id in enumerate(votes):
            voter = self.agents[idx]
            vote_details.append({
                "voter_id": voter.id,
                "voter_name": voter.name,
                "opinion_id": voted_opinion_id,
            })

        for opinion in opinions:
            opinion.votes = vote_counter.get(opinion.id, 0)

        # 1票以上の意見のみ残す
        filtered_opinions = [op for op in opinions if op.votes > 0]

        # 意見の詳細情報を含めて送信
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

        # 各Agentが支持している意見を記録
        agent_opinions = {op.agent_id: op for op in opinions}

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
                counter_arguments = []
                for agent in self.agents:
                    if agent.id != persuader.id:
                        # 各Agentが支持している意見と他の意見を取得
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

                        # 反論があった場合は記録
                        if not is_agreement:
                            counter_arguments.append((agent, response_msg))

                # 反論があった場合、元の意見の発言者が再応答
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

    async def _retrieve_background_context(self, topic: str) -> list:
        """議論トピックから背景知識を取得"""
        try:
            # トピックからキーワードを抽出（簡易版）
            keywords = self._extract_keywords(topic)

            # コンテキスト取得
            context_items = await self.context_retriever.retrieve_context(topic, keywords)
            return context_items

        except Exception as e:
            logger.error(f"Error retrieving background context: {e}")
            return []

    def _extract_keywords(self, topic: str) -> List[str]:
        """トピックからキーワードを抽出（簡易版）"""
        # TODO: より高度なキーワード抽出を実装
        # 現在は単純にスペース区切りで分割
        keywords = [word.strip() for word in topic.split() if len(word.strip()) > 2]
        return keywords[:5]  # 最大5個まで

    def _generate_final_conclusion(self) -> str:
        """最終結論を生成"""
        conclusions = [item.conclusion for item in self.session.agenda if item.conclusion]
        return "\n\n".join([
            f"{idx + 1}. {self.session.agenda[idx].title}: {conclusion}"
            for idx, conclusion in enumerate(conclusions)
        ])
