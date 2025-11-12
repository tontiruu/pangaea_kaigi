"""OpenAI Responses API クライアント"""

import asyncio
from openai import AsyncOpenAI
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class OpenAIResponsesClient:
    """OpenAI Responses API クライアント"""

    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-5-nano"  # 最新の小型モデル

    async def create_response(
        self,
        input_text: str,
        previous_response_id: Optional[str] = None,
        store: bool = True,
    ) -> dict:
        """
        OpenAI Responses API でレスポンスを生成

        Responses APIを使用して会話状態を管理します。
        previous_response_idを指定することで会話を継続できます。

        Args:
            input_text: 入力プロンプト
            previous_response_id: 前回のresponse_id（会話を継続する場合）
            store: サーバー側に会話を保存するか

        Returns:
            {"id": response_id, "content": content}
        """
        try:
            # Responses API のパラメータ構築
            params = {
                "model": self.model,
                "input": input_text,
            }

            # previous_response_idがある場合は追加
            if previous_response_id:
                params["previous_response_id"] = previous_response_id

            # storeパラメータを追加
            if store:
                params["store"] = True

            # Responses API 呼び出し
            response = await self.client.responses.create(**params)

            logger.info(f"OpenAI Response ID: {response.id}")
            content = self._extract_content(response)
            logger.info(f"Extracted content length: {len(content)}")

            return {
                "id": response.id,
                "content": content,
            }

        except Exception as e:
            logger.error(f"OpenAI API エラー: {e}", exc_info=True)
            raise

    def _extract_content(self, response) -> str:
        """レスポンスからコンテンツを抽出"""
        try:
            # Responses API の構造: response.output_text
            if hasattr(response, "output_text") and response.output_text:
                return response.output_text

            logger.error(f"レスポンス構造が想定外: {response}")
            return ""
        except Exception as e:
            logger.error(f"コンテンツ抽出エラー: {e}", exc_info=True)
            return ""

    async def create_with_retry(
        self,
        input_text: str,
        previous_response_id: Optional[str] = None,
        max_retries: int = 3,
        base_delay: float = 1.0,
    ) -> dict:
        """
        リトライ機能付きでレスポンスを生成

        Args:
            input_text: 入力プロンプト
            previous_response_id: 前回のresponse_id
            max_retries: 最大リトライ回数
            base_delay: 基本待機時間（秒）

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
                    f"リトライ {attempt + 1}/{max_retries}。{delay}秒後に再試行: {e}"
                )
                await asyncio.sleep(delay)
