"""API route definitions"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from typing import List
from api.websocket import manager
from services.openai_client import OpenAIResponsesClient
from services.agent_manager import AgentManager
from services.facilitator import Facilitator
from services.discussion_engine import DiscussionEngine
from services.context_retriever import ContextRetriever
from config import settings
import logging
import asyncio

logger = logging.getLogger(__name__)

router = APIRouter()


class StartDiscussionRequest(BaseModel):
    """Start discussion request"""
    topic: str


class ContextRetrievalRequest(BaseModel):
    """Context retrieval request"""
    topic: str
    keywords: List[str] = []


@router.post("/api/discussions/start")
async def start_discussion_endpoint(request: StartDiscussionRequest):
    """Start discussion endpoint (HTTP-based)"""
    try:
        # TODO: Implementation
        return {"message": "Starting discussion", "topic": request.topic}
    except Exception as e:
        logger.error(f"Discussion start error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/ws/discussion")
async def websocket_discussion_endpoint(websocket: WebSocket):
    """WebSocket endpoint - Real-time discussion communication"""
    discussion_id = None

    try:
        await websocket.accept()
        logger.info("WebSocket connection accepted")

        # Receive first message (including topic)
        data = await websocket.receive_json()

        if data.get("type") != "start_discussion":
            await websocket.send_json({
                "type": "error",
                "data": {"message": "First message must be start_discussion"}
            })
            await websocket.close()
            return

        topic = data.get("data", {}).get("topic")
        if not topic:
            await websocket.send_json({
                "type": "error",
                "data": {"message": "Topic is required"}
            })
            await websocket.close()
            return

        # Initialize OpenAI client
        openai_client = OpenAIResponsesClient(api_key=settings.openai_api_key)
        agent_manager = AgentManager(openai_client)
        facilitator = Facilitator(openai_client, agent_manager)

        # Message sending callback
        async def send_message(message: dict):
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"WebSocket message send error: {e}")

        # Initialize DiscussionEngine
        discussion_engine = DiscussionEngine(
            facilitator=facilitator,
            agent_manager=agent_manager,
            message_callback=send_message,
        )

        # Start discussion
        logger.info(f"Starting discussion: {topic}")
        session = await discussion_engine.start_discussion(topic)
        discussion_id = session.id

        logger.info(f"Discussion completed: {discussion_id}")

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
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


@router.post("/api/context/retrieve")
async def retrieve_context_endpoint(request: ContextRetrievalRequest):
    """
    Context retrieval endpoint (for testing)

    Retrieves background knowledge related to discussion topics from Notion/Slack/Atlassian.
    Currently returns mock data.
    """
    try:
        # Initialize ContextRetriever (mock mode)
        retriever = ContextRetriever(use_mock=True)

        # Automatically extract keywords if not specified
        keywords = request.keywords
        if not keywords:
            # Simple keyword extraction
            keywords = [word.strip() for word in request.topic.split() if len(word.strip()) > 2][:5]

        # Retrieve background knowledge
        context_items = await retriever.retrieve_context(request.topic, keywords)

        # Format response
        return {
            "topic": request.topic,
            "keywords": keywords,
            "count": len(context_items),
            "contexts": [
                {
                    "source": item.source,
                    "title": item.title,
                    "content": item.content,
                    "url": item.url,
                    "metadata": item.metadata,
                }
                for item in context_items
            ]
        }

    except Exception as e:
        logger.error(f"Context retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/context/sources")
async def get_context_sources():
    """
    Get information about available context sources
    """
    return {
        "sources": [
            {
                "name": "notion",
                "enabled": bool(settings.notion_token),
                "description": "Search related documents from Notion"
            },
            {
                "name": "slack",
                "enabled": bool(settings.slack_bot_token),
                "description": "Search past discussions from Slack"
            },
            {
                "name": "atlassian",
                "enabled": bool(settings.atlassian_api_token),
                "description": "Search information from Jira and Confluence"
            }
        ],
        "dedalus_configured": bool(settings.dedalus_api_key),
        "context_retrieval_enabled": settings.enable_context_retrieval
    }


@router.get("/api/health")
async def health_check():
    """Health check"""
    return {"status": "healthy", "service": "pangaea-kaigi-backend"}
