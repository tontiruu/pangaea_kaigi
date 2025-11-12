"""OpenAI Responses API client"""

import asyncio
from openai import AsyncOpenAI
from typing import Optional, Callable, Awaitable
import logging

logger = logging.getLogger(__name__)


class OpenAIResponsesClient:
    """OpenAI Responses API client"""

    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-5-nano"  # Latest compact model

    async def create_response(
        self,
        input_text: str,
        previous_response_id: Optional[str] = None,
        store: bool = True,
    ) -> dict:
        """
        Generate response using OpenAI Responses API

        Manage conversation state using the Responses API.
        Conversations can be continued by specifying previous_response_id.

        Args:
            input_text: Input prompt
            previous_response_id: Previous response_id (for continuing conversation)
            store: Whether to save conversation on server side

        Returns:
            {"id": response_id, "content": content}
        """
        try:
            # Build Responses API parameters
            params = {
                "model": self.model,
                "input": input_text,
            }

            # Add previous_response_id if present
            if previous_response_id:
                params["previous_response_id"] = previous_response_id

            # Add store parameter
            if store:
                params["store"] = True

            # Call Responses API
            response = await self.client.responses.create(**params)

            logger.info(f"OpenAI Response ID: {response.id}")
            content = self._extract_content(response)
            logger.info(f"Extracted content length: {len(content)}")

            return {
                "id": response.id,
                "content": content,
            }

        except Exception as e:
            logger.error(f"OpenAI API error: {e}", exc_info=True)
            raise

    def _extract_content(self, response) -> str:
        """Extract content from response"""
        try:
            # Responses API structure: response.output_text
            if hasattr(response, "output_text") and response.output_text:
                return response.output_text

            logger.error(f"Unexpected response structure: {response}")
            return ""
        except Exception as e:
            logger.error(f"Content extraction error: {e}", exc_info=True)
            return ""

    async def create_with_retry(
        self,
        input_text: str,
        previous_response_id: Optional[str] = None,
        max_retries: int = 3,
        base_delay: float = 1.0,
    ) -> dict:
        """
        Generate response with retry functionality

        Args:
            input_text: Input prompt
            previous_response_id: Previous response_id
            max_retries: Maximum number of retries
            base_delay: Base wait time (seconds)

        Returns:
            {"id": response_id, "content": content}
        """
        for attempt in range(max_retries):
            try:
                return await self.create_response(
                    input_text=input_text,
                    previous_response_id=previous_response_id,
                )
            except Exception as e:
                if attempt == max_retries - 1:
                    raise

                delay = base_delay * (2**attempt)
                logger.warning(
                    f"Retry {attempt + 1}/{max_retries}. Retrying after {delay} seconds: {e}"
                )
                await asyncio.sleep(delay)

    async def create_with_streaming(
        self,
        input_text: str,
        previous_response_id: Optional[str] = None,
        store: bool = True,
        on_chunk: Optional[Callable[[str], Awaitable[None]]] = None,
    ) -> dict:
        """
        Generate response with streaming

        Args:
            input_text: Input prompt
            previous_response_id: Previous response_id
            store: Whether to save conversation on server side
            on_chunk: Callback function called for each chunk

        Returns:
            {"id": response_id, "content": complete content}
        """
        try:
            params = {
                "model": self.model,
                "input": input_text,
                "stream": True,
            }

            if previous_response_id:
                params["previous_response_id"] = previous_response_id

            if store:
                params["store"] = True

            response_stream = await self.client.responses.create(**params)

            full_content = ""
            response_id = None

            async for chunk in response_stream:
                if hasattr(chunk, "id") and chunk.id:
                    response_id = chunk.id

                if hasattr(chunk, "output_text") and chunk.output_text:
                    chunk_text = chunk.output_text
                    full_content = chunk_text

                    if on_chunk:
                        await on_chunk(chunk_text)

            logger.info(f"OpenAI Streaming Response ID: {response_id}")
            logger.info(f"Total content length: {len(full_content)}")

            return {
                "id": response_id,
                "content": full_content,
            }

        except Exception as e:
            logger.error(f"OpenAI API streaming error: {e}", exc_info=True)
            raise
