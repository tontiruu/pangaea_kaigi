"""APIルート定義"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from api.websocket import manager
from services.openai_client import OpenAIResponsesClient
from services.agent_manager import AgentManager
from services.facilitator import Facilitator
from services.discussion_engine import DiscussionEngine
from config import settings
import logging
import asyncio

logger = logging.getLogger(__name__)

router = APIRouter()


class StartDiscussionRequest(BaseModel):
    """議論開始リクエスト"""
    topic: str


@router.post("/api/discussions/start")
async def start_discussion_endpoint(request: StartDiscussionRequest):
    """議論開始エンドポイント（HTTPベース）"""
    try:
        # TODO: 実装
        return {"message": "議論を開始します", "topic": request.topic}
    except Exception as e:
        logger.error(f"議論開始エラー: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/ws/discussion")
async def websocket_discussion_endpoint(websocket: WebSocket):
    """WebSocketエンドポイント - 議論のリアルタイム通信"""
    discussion_id = None

    try:
        await websocket.accept()
        logger.info("WebSocket接続を受け入れました")

        # 最初のメッセージを受信（議題を含む）
        data = await websocket.receive_json()

        if data.get("type") != "start_discussion":
            await websocket.send_json({
                "type": "error",
                "data": {"message": "最初のメッセージは start_discussion である必要があります"}
            })
            await websocket.close()
            return

        topic = data.get("data", {}).get("topic")
        if not topic:
            await websocket.send_json({
                "type": "error",
                "data": {"message": "議題(topic)が必要です"}
            })
            await websocket.close()
            return

        # OpenAI クライアント初期化
        openai_client = OpenAIResponsesClient(api_key=settings.openai_api_key)
        agent_manager = AgentManager(openai_client)
        facilitator = Facilitator(openai_client, agent_manager)

        # メッセージ送信用コールバック
        async def send_message(message: dict):
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"WebSocketメッセージ送信エラー: {e}")

        # DiscussionEngine 初期化
        discussion_engine = DiscussionEngine(
            facilitator=facilitator,
            agent_manager=agent_manager,
            message_callback=send_message,
        )

        # 議論開始
        logger.info(f"議論開始: {topic}")
        session = await discussion_engine.start_discussion(topic)
        discussion_id = session.id

        logger.info(f"議論完了: {discussion_id}")

    except WebSocketDisconnect:
        logger.info("WebSocket切断されました")
    except Exception as e:
        logger.error(f"WebSocketエラー: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "data": {"message": str(e)}
            })
        except:
            pass
    finally:
        try:
            await websocket.close()
        except:
            pass


@router.get("/api/health")
async def health_check():
    """ヘルスチェック"""
    return {"status": "healthy", "service": "pangaea-kaigi-backend"}
