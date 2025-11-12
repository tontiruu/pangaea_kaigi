"""ファシリテーターAgent"""
import json
import uuid
from typing import List, Optional, Callable, Awaitable
from models.discussion import AgendaItem
from models.agent import Agent, AgentRole
from services.openai_client import OpenAIResponsesClient
from services.agent_manager import AgentManager
from utils.prompts import (
    FACILITATOR_CREATE_AGENDA,
    FACILITATOR_GENERATE_AGENTS,
)
import logging

logger = logging.getLogger(__name__)


class Facilitator:
    """ファシリテーターAgent"""

    def __init__(self, openai_client: OpenAIResponsesClient, agent_manager: AgentManager):
        self.openai_client = openai_client
        self.agent_manager = agent_manager
        self.response_id: Optional[str] = None
        self.agent: Optional[Agent] = None

    def initialize(self):
        """ファシリテーターAgentを初期化"""
        self.agent = self.agent_manager.create_agent(
            name="ファシリテーター",
            perspective="議論を円滑に進め、全員の合意を促進する",
            role=AgentRole.FACILITATOR,
        )
        logger.info("ファシリテーター初期化完了")

    async def create_agenda(self, topic: str) -> List[AgendaItem]:
        """議題からアジェンダを作成"""
        return await self.create_agenda_with_context(topic, "")

    async def create_agenda_with_context(
        self,
        topic: str,
        context: str,
        on_stream: Optional[Callable[[str], Awaitable[None]]] = None,
    ) -> List[AgendaItem]:
        """議題と背景知識からアジェンダを作成（ストリーミング対応）"""
        prompt = FACILITATOR_CREATE_AGENDA.format(topic=topic)

        # 背景知識がある場合はプロンプトに追加
        if context:
            prompt = f"{context}\n\n{prompt}\n\n上記の背景知識を考慮してアジェンダを作成してください。"

        # ストリーミングコールバック
        async def chunk_callback(chunk: str):
            if on_stream:
                await on_stream(chunk)

        # ストリーミング対応の場合
        if on_stream:
            response = await self.openai_client.create_with_streaming(
                input_text=prompt,
                previous_response_id=self.response_id,
                on_chunk=chunk_callback,
            )
        else:
            response = await self.openai_client.create_with_retry(
                input_text=prompt,
                previous_response_id=self.response_id,
            )

        self.response_id = response["id"]

        try:
            agenda_data = self._extract_json(response["content"])
            agenda_items = []

            for idx, item in enumerate(agenda_data):
                agenda_id = f"agenda_{uuid.uuid4().hex[:8]}"
                agenda_item = AgendaItem(
                    id=agenda_id,
                    title=item["title"],
                    description=item["description"],
                    order=item.get("order", idx + 1),
                )
                agenda_items.append(agenda_item)

            logger.info(f"アジェンダ作成完了: {len(agenda_items)}個")
            return agenda_items

        except Exception as e:
            logger.error(f"アジェンダ解析エラー: {e}")
            logger.error(f"レスポンス内容: {response['content']}")
            raise

    async def generate_agents(self, topic: str, agenda: List[AgendaItem]) -> List[Agent]:
        """議題とアジェンダから参加Agentを生成"""
        agenda_text = "\n".join([
            f"{item.order}. {item.title}: {item.description}"
            for item in agenda
        ])

        prompt = FACILITATOR_GENERATE_AGENTS.format(
            topic=topic,
            agenda=agenda_text,
        )

        response = await self.openai_client.create_with_retry(
            input_text=prompt,
            previous_response_id=self.response_id,
        )

        self.response_id = response["id"]

        try:
            agents_data = self._extract_json(response["content"])
            agents = []

            for agent_info in agents_data:
                agent = self.agent_manager.create_agent(
                    name=agent_info["name"],
                    perspective=agent_info["perspective"],
                    role=AgentRole.PARTICIPANT,
                )
                agents.append(agent)

            logger.info(f"Agent生成完了: {len(agents)}人")
            return agents

        except Exception as e:
            logger.error(f"Agent解析エラー: {e}")
            logger.error(f"レスポンス内容: {response['content']}")
            raise

    def _extract_json(self, text: str) -> dict | list:
        """テキストからJSON部分を抽出してパース"""
        # マークダウンのコードブロックを削除
        text = text.replace("```json", "").replace("```", "")
        text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # JSON部分を探す
            start_idx = text.find("[")
            if start_idx == -1:
                start_idx = text.find("{")

            end_idx = text.rfind("]")
            if end_idx == -1:
                end_idx = text.rfind("}")

            if start_idx != -1 and end_idx != -1:
                json_text = text[start_idx:end_idx + 1]
                return json.loads(json_text)

            raise
