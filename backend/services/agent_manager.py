"""Agent の生成と管理"""
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
    """Agent の生成と管理を行うクラス"""

    def __init__(self, openai_client: OpenAIResponsesClient):
        self.openai_client = openai_client
        self.agents: Dict[str, Agent] = {}

    def create_agent(self, name: str, perspective: str, role: AgentRole = AgentRole.PARTICIPANT) -> Agent:
        """新しいAgentを作成"""
        agent_id = f"agent_{uuid.uuid4().hex[:8]}"
        agent = Agent(
            id=agent_id,
            name=name,
            perspective=perspective,
            role=role,
        )
        self.agents[agent_id] = agent
        logger.info(f"Agent作成: {agent.name} (ID: {agent.id})")
        return agent

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Agent IDからAgentを取得"""
        return self.agents.get(agent_id)

    def get_all_agents(self) -> List[Agent]:
        """すべてのAgentを取得"""
        return list(self.agents.values())

    async def generate_independent_opinion(
        self,
        agent: Agent,
        agenda_title: str,
        agenda_description: str,
        background_context: str = "",
    ) -> tuple[str, str]:
        """Agentに独立した意見を生成させる"""
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

        # response_idを更新
        agent.response_id = response["id"]
        self.agents[agent.id] = agent

        logger.info(f"{agent.name}が意見を生成")
        return response["content"], response["id"]

    async def vote_for_opinion(
        self,
        agent: Agent,
        opinions: List[Opinion],
    ) -> str:
        """Agentに意見への投票を行わせる"""
        opinions_text = "\n\n".join([
            f"ID: {op.id}\nAgent: {op.agent_name}\n内容: {op.content}"
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
        logger.info(f"{agent.name}が投票: {voted_opinion_id}")
        return voted_opinion_id

    async def persuade(
        self,
        agent: Agent,
        opinion: Opinion,
    ) -> tuple[str, str]:
        """Agentに説得を行わせる"""
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

        logger.info(f"{agent.name}が説得を開始")
        return response["content"], response["id"]

    async def respond_to_persuasion(
        self,
        agent: Agent,
        persuasion_message: str,
        your_opinion: str,
        other_opinions: List[str],
    ) -> tuple[str, str, bool]:
        """Agentに説得への応答を行わせる

        Returns:
            tuple[content, response_id, is_agreement]: 応答内容、response_id、合意したかどうか
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
        # 合意か反論かを判定
        is_agreement = "合意" in content or "同意" in content or "賛成" in content

        logger.info(f"{agent.name}が応答: {'合意' if is_agreement else '反論'}")
        return content, response["id"], is_agreement

    async def respond_to_counter_argument(
        self,
        agent: Agent,
        counter_argument: str,
        original_opinion: str,
    ) -> tuple[str, str, bool]:
        """元の意見の発言者が反論に対して応答する

        Returns:
            tuple[content, response_id, maintains_position]: 応答内容、response_id、元の意見を維持するか
        """
        prompt = f"""あなたは{agent.name}です。

あなたの元の意見: {original_opinion}

以下の反論がありました: {counter_argument}

この反論に対して、あなたの考えを述べてください。
元の意見を支持し続けるのか、相手の反論に賛同するのかを表明し、その理由を述べてください。

出力形式：
判断: [元の意見を支持/反論に賛同]
理由: [あなたの考えを簡潔に述べてください]"""

        response = await self.openai_client.create_with_retry(
            input_text=prompt,
            previous_response_id=agent.response_id,
        )

        agent.response_id = response["id"]
        self.agents[agent.id] = agent

        content = response["content"]
        # 元の意見を維持するかを判定
        maintains_position = "支持" in content or "維持" in content

        logger.info(f"{agent.name}が反論に応答: {'元の意見を維持' if maintains_position else '反論に賛同'}")
        return content, response["id"], maintains_position

    async def make_final_decision(
        self,
        agent: Agent,
        proposed_opinion: str,
    ) -> tuple[bool, str]:
        """Agentに最終判断を行わせる"""
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
        agrees = "Yes" in content or "yes" in content or "合意" in content

        logger.info(f"{agent.name}の判断: {'合意' if agrees else '不合意'}")
        return agrees, content
