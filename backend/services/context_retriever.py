"""Service for retrieving background knowledge (Dedalus Labs MCP integration)"""
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
    """Retrieved context information"""
    source: str  # "notion", "slack", "atlassian"
    title: str
    content: str
    url: Optional[str] = None
    metadata: Optional[Dict] = None


class ContextRetriever:
    """Retrieve background knowledge from multiple MCP services using Dedalus Labs"""

    def __init__(self, use_mock: bool = True):
        self.enabled = settings.enable_context_retrieval
        self.use_mock = use_mock  # Mock data usage flag
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
        Retrieve background knowledge based on discussion topic and keywords

        Args:
            topic: Discussion topic
            keywords: Keywords extracted from topic

        Returns:
            List of retrieved context information
        """
        # Use mock data
        if self.use_mock:
            return await self._retrieve_from_mock()

        if not self.enabled or not self.dedalus_client:
            logger.info("Context retrieval is disabled")
            return []

        contexts = []

        # Retrieve information from Notion
        if settings.notion_token:
            notion_contexts = await self._retrieve_from_notion(topic, keywords)
            contexts.extend(notion_contexts)

        # Retrieve information from Slack
        if settings.slack_bot_token:
            slack_contexts = await self._retrieve_from_slack(topic, keywords)
            contexts.extend(slack_contexts)

        # Retrieve information from Atlassian
        if settings.atlassian_api_token:
            atlassian_contexts = await self._retrieve_from_atlassian(topic, keywords)
            contexts.extend(atlassian_contexts)

        logger.info(f"Retrieved {len(contexts)} context items for topic: {topic}")
        return contexts

    async def _retrieve_from_mock(self) -> List[ContextItem]:
        """Load background knowledge from mock data file"""
        try:
            mock_file = Path(__file__).parent.parent / "mock_data.txt"

            if not mock_file.exists():
                logger.warning(f"Mock data file not found: {mock_file}")
                return []

            with open(mock_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Split file by sections
            contexts = []
            current_section = None
            current_title = None
            current_content = []
            current_url = None

            for line in content.split("\n"):
                line = line.strip()

                if line.startswith("## "):
                    # New major section
                    current_section = line[3:].strip()
                elif line.startswith("### "):
                    # New item - save previous item
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

                    # Start new item
                    current_title = line[4:].strip()
                    current_content = []
                    current_url = None
                elif line.startswith("URL: "):
                    current_url = line[5:].strip()
                elif line and not line.startswith("#"):
                    current_content.append(line)

            # Save last item
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
        Retrieve related information from Notion

        [Example of using Dedalus Labs]
        This function demonstrates the actual usage of Dedalus Labs.
        """
        try:
            # Call Notion MCP server via Dedalus Labs
            search_query = f"{topic} {' '.join(keywords)}"

            # [Step 1] Build prompt using MCP tools
            # Dedalus allows natural language instructions to call MCP tools
            prompt = f"""
            Use the Notion MCP server to search for pages and databases related to: {search_query}

            Please search for:
            1. Pages containing these keywords
            2. Recent updates related to this topic
            3. Relevant documentation

            Return the results in a structured format with title, content snippet, and URL.
            """

            # [Step 2] Call Dedalus API
            # Use AsyncDedalus.chat.completions.create method
            # Integrate MCP tools with OpenAI-compatible interface
            response = await self.dedalus_client.chat.completions.create(
                model="openai/gpt-4o",  # LLM model to use
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that retrieves and structures information from Notion."
                    },
                    {"role": "user", "content": prompt}
                ],
                # [Important] Specify MCP tools
                # Specify Notion MCP server here and pass authentication info
                tools=[{
                    "type": "mcp",
                    "server": "notion",  # MCP server name (needs verification)
                    "config": {
                        "token": settings.notion_token  # Notion integration token
                    }
                }]
            )

            # [Step 3] Parse response and convert to ContextItem
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
        Retrieve related information from Slack

        [Example of Dedalus Labs + Slack MCP integration]
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

            # Example of using Slack MCP server
            # Pass bot_token and team_id in config
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
                    "server": "slack",  # Slack MCP server name (needs verification)
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
        """Retrieve related information from Atlassian (Jira/Confluence)"""
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
        """Parse Notion response"""
        contexts = []
        try:
            # Extract structured data from response
            content = response.choices[0].message.content

            # Simple parsing (needs adjustment based on actual response format)
            # TODO: Implement according to actual Dedalus response format
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
        """Parse Slack response"""
        contexts = []
        try:
            content = response.choices[0].message.content

            # TODO: Implement according to actual Dedalus response format
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
        """Parse Atlassian response"""
        contexts = []
        try:
            content = response.choices[0].message.content

            # TODO: Implement according to actual Dedalus response format
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
        Format retrieved contexts into a string for embedding in prompts

        Returns:
            Formatted context string
        """
        if not contexts:
            return ""

        formatted = ["## Background Knowledge\n"]

        for ctx in contexts:
            formatted.append(f"### [{ctx.source.upper()}] {ctx.title}")
            formatted.append(f"{ctx.content}\n")
            if ctx.url:
                formatted.append(f"URL: {ctx.url}\n")

        return "\n".join(formatted)
