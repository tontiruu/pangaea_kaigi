"""背景知識を取得するためのサービス（Dedalus Labs MCP統合）"""
import logging
import os
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from dedalus_labs import AsyncDedalus
from config import settings

logger = logging.getLogger(__name__)


@dataclass
class ContextItem:
    """取得したコンテキスト情報"""
    source: str  # "notion", "slack", "atlassian"
    title: str
    content: str
    url: Optional[str] = None
    metadata: Optional[Dict] = None


class ContextRetriever:
    """Dedalus Labsを使用して複数のMCPサービスから背景知識を取得"""

    def __init__(self, use_mock: bool = True):
        self.enabled = settings.enable_context_retrieval
        self.use_mock = use_mock  # モックデータ使用フラグ
        self.dedalus_client: Optional[AsyncDedalus] = None

        if self.enabled and settings.dedalus_api_key and not use_mock:
            self.dedalus_client = AsyncDedalus(
                api_key=settings.dedalus_api_key
            )
            logger.info("ContextRetriever initialized with Dedalus SDK")
        else:
            if use_mock:
                logger.info("ContextRetriever using mock data")
            else:
                logger.warning("ContextRetriever disabled or missing API key")

    async def retrieve_context(self, topic: str, keywords: List[str]) -> List[ContextItem]:
        """
        議論トピックとキーワードに基づいて背景知識を取得

        Args:
            topic: 議論のトピック
            keywords: トピックから抽出されたキーワード

        Returns:
            取得したコンテキスト情報のリスト
        """
        # モックデータを使用する場合
        if self.use_mock:
            return await self._retrieve_from_mock()

        if not self.enabled or not self.dedalus_client:
            logger.info("Context retrieval is disabled")
            return []

        contexts = []

        # Notionから情報を取得
        if settings.notion_token:
            notion_contexts = await self._retrieve_from_notion(topic, keywords)
            contexts.extend(notion_contexts)

        # Slackから情報を取得
        if settings.slack_bot_token:
            slack_contexts = await self._retrieve_from_slack(topic, keywords)
            contexts.extend(slack_contexts)

        # Atlassianから情報を取得
        if settings.atlassian_api_token:
            atlassian_contexts = await self._retrieve_from_atlassian(topic, keywords)
            contexts.extend(atlassian_contexts)

        logger.info(f"Retrieved {len(contexts)} context items for topic: {topic}")
        return contexts

    async def _retrieve_from_mock(self) -> List[ContextItem]:
        """モックデータファイルから背景知識を読み込み"""
        try:
            mock_file = Path(__file__).parent.parent / "mock_data.txt"

            if not mock_file.exists():
                logger.warning(f"Mock data file not found: {mock_file}")
                return []

            with open(mock_file, "r", encoding="utf-8") as f:
                content = f.read()

            # ファイルをセクションごとに分割
            contexts = []
            current_section = None
            current_title = None
            current_content = []
            current_url = None

            for line in content.split("\n"):
                line = line.strip()

                if line.startswith("## "):
                    # 新しい大セクション
                    current_section = line[3:].strip()
                elif line.startswith("### "):
                    # 新しい項目 - 前の項目を保存
                    if current_title and current_content:
                        source = "notion" if "Notion" in current_section else \
                                "slack" if "Slack" in current_section else \
                                "atlassian" if "Atlassian" in current_section else "unknown"

                        contexts.append(ContextItem(
                            source=source,
                            title=current_title,
                            content="\n".join(current_content),
                            url=current_url,
                            metadata={"section": current_section}
                        ))

                    # 新しい項目を開始
                    current_title = line[4:].strip()
                    current_content = []
                    current_url = None
                elif line.startswith("URL: "):
                    current_url = line[5:].strip()
                elif line and not line.startswith("#"):
                    current_content.append(line)

            # 最後の項目を保存
            if current_title and current_content:
                source = "notion" if "Notion" in current_section else \
                        "slack" if "Slack" in current_section else \
                        "atlassian" if "Atlassian" in current_section else "unknown"

                contexts.append(ContextItem(
                    source=source,
                    title=current_title,
                    content="\n".join(current_content),
                    url=current_url,
                    metadata={"section": current_section}
                ))

            logger.info(f"Loaded {len(contexts)} context items from mock data")
            return contexts

        except Exception as e:
            logger.error(f"Error loading mock data: {e}")
            return []

    async def _retrieve_from_notion(
        self, topic: str, keywords: List[str]
    ) -> List[ContextItem]:
        """
        Notionから関連情報を取得

        【Dedalus Labs使用方法の例】
        この関数はDedalus Labsの実際の使用方法を示しています。
        """
        try:
            # Dedalus Labs経由でNotionのMCPサーバーを呼び出し
            search_query = f"{topic} {' '.join(keywords)}"

            # 【ステップ1】MCPツールを使用したプロンプトを構築
            # Dedalusは自然言語でMCPツールの呼び出しを指示できます
            prompt = f"""
            Use the Notion MCP server to search for pages and databases related to: {search_query}

            Please search for:
            1. Pages containing these keywords
            2. Recent updates related to this topic
            3. Relevant documentation

            Return the results in a structured format with title, content snippet, and URL.
            """

            # 【ステップ2】Dedalus APIを呼び出し
            # AsyncDedalus.chat.completions.createメソッドを使用
            # OpenAI互換のインターフェースでMCPツールを統合
            response = await self.dedalus_client.chat.completions.create(
                model="openai/gpt-4o",  # 使用するLLMモデル
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that retrieves and structures information from Notion."
                    },
                    {"role": "user", "content": prompt}
                ],
                # 【重要】MCPツールの指定
                # ここでNotion MCPサーバーを指定し、認証情報を渡す
                tools=[{
                    "type": "mcp",
                    "server": "notion",  # MCPサーバー名（要確認）
                    "config": {
                        "token": settings.notion_token  # Notion統合トークン
                    }
                }]
            )

            # 【ステップ3】レスポンスをパースしてContextItemに変換
            contexts = self._parse_notion_response(response)
            logger.info(f"Retrieved {len(contexts)} items from Notion")
            return contexts

        except Exception as e:
            logger.error(f"Error retrieving from Notion: {e}")
            return []

    async def _retrieve_from_slack(
        self, topic: str, keywords: List[str]
    ) -> List[ContextItem]:
        """
        Slackから関連情報を取得

        【Dedalus Labs + Slack MCP統合の例】
        """
        try:
            search_query = f"{topic} {' '.join(keywords)}"

            prompt = f"""
            Use the Slack MCP server to search for messages and threads related to: {search_query}

            Please search for:
            1. Recent channel discussions about this topic
            2. Important threads and decisions
            3. Relevant conversations from the past 30 days

            Return the results with message content, channel name, author, and timestamp.
            """

            # Slack MCPサーバーを使用する例
            # bot_tokenとteam_idを設定に渡す
            response = await self.dedalus_client.chat.completions.create(
                model="openai/gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that retrieves and structures information from Slack."
                    },
                    {"role": "user", "content": prompt}
                ],
                tools=[{
                    "type": "mcp",
                    "server": "slack",  # Slack MCPサーバー名（要確認）
                    "config": {
                        "bot_token": settings.slack_bot_token,
                        "team_id": settings.slack_team_id
                    }
                }]
            )

            contexts = self._parse_slack_response(response)
            logger.info(f"Retrieved {len(contexts)} items from Slack")
            return contexts

        except Exception as e:
            logger.error(f"Error retrieving from Slack: {e}")
            return []

    async def _retrieve_from_atlassian(
        self, topic: str, keywords: List[str]
    ) -> List[ContextItem]:
        """Atlassian (Jira/Confluence) から関連情報を取得"""
        try:
            search_query = f"{topic} {' '.join(keywords)}"

            prompt = f"""
            Use the Atlassian MCP server to search for relevant information about: {search_query}

            Please search for:
            1. Related Jira tickets and issues
            2. Confluence documentation pages
            3. Project specifications and requirements

            Return the results with title, description, status (for Jira), and URL.
            """

            response = await self.dedalus_client.chat.completions.create(
                model="openai/gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that retrieves and structures information from Jira and Confluence."
                    },
                    {"role": "user", "content": prompt}
                ],
                tools=[{
                    "type": "mcp",
                    "server": "atlassian",
                    "config": {
                        "email": settings.atlassian_email,
                        "api_token": settings.atlassian_api_token,
                        "domain": settings.atlassian_domain
                    }
                }]
            )

            contexts = self._parse_atlassian_response(response)
            logger.info(f"Retrieved {len(contexts)} items from Atlassian")
            return contexts

        except Exception as e:
            logger.error(f"Error retrieving from Atlassian: {e}")
            return []

    def _parse_notion_response(self, response) -> List[ContextItem]:
        """Notionのレスポンスをパース"""
        contexts = []
        try:
            # レスポンスから構造化されたデータを抽出
            content = response.choices[0].message.content

            # 簡易的なパース（実際のレスポンス形式に応じて調整が必要）
            # TODO: 実際のDedalusレスポンス形式に合わせて実装
            contexts.append(ContextItem(
                source="notion",
                title="Notion Search Results",
                content=content,
                url=None,
                metadata={"raw_response": content}
            ))
        except Exception as e:
            logger.error(f"Error parsing Notion response: {e}")

        return contexts

    def _parse_slack_response(self, response) -> List[ContextItem]:
        """Slackのレスポンスをパース"""
        contexts = []
        try:
            content = response.choices[0].message.content

            # TODO: 実際のDedalusレスポンス形式に合わせて実装
            contexts.append(ContextItem(
                source="slack",
                title="Slack Search Results",
                content=content,
                url=None,
                metadata={"raw_response": content}
            ))
        except Exception as e:
            logger.error(f"Error parsing Slack response: {e}")

        return contexts

    def _parse_atlassian_response(self, response) -> List[ContextItem]:
        """Atlassianのレスポンスをパース"""
        contexts = []
        try:
            content = response.choices[0].message.content

            # TODO: 実際のDedalusレスポンス形式に合わせて実装
            contexts.append(ContextItem(
                source="atlassian",
                title="Atlassian Search Results",
                content=content,
                url=None,
                metadata={"raw_response": content}
            ))
        except Exception as e:
            logger.error(f"Error parsing Atlassian response: {e}")

        return contexts

    def format_contexts_for_prompt(self, contexts: List[ContextItem]) -> str:
        """
        取得したコンテキストをプロンプトに埋め込むための文字列に整形

        Returns:
            整形されたコンテキスト文字列
        """
        if not contexts:
            return ""

        formatted = ["## 背景知識\n"]

        for ctx in contexts:
            formatted.append(f"### [{ctx.source.upper()}] {ctx.title}")
            formatted.append(f"{ctx.content}\n")
            if ctx.url:
                formatted.append(f"URL: {ctx.url}\n")

        return "\n".join(formatted)
