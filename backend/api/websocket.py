"""WebSocket connection management"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Class to manage WebSocket connections"""

    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, discussion_id: str):
        """Connect client"""
        await websocket.accept()
        if discussion_id not in self.active_connections:
            self.active_connections[discussion_id] = set()
        self.active_connections[discussion_id].add(websocket)
        logger.info(f"WebSocket connected: {discussion_id}")

    def disconnect(self, websocket: WebSocket, discussion_id: str):
        """Disconnect client"""
        if discussion_id in self.active_connections:
            self.active_connections[discussion_id].discard(websocket)
            if not self.active_connections[discussion_id]:
                del self.active_connections[discussion_id]
        logger.info(f"WebSocket disconnected: {discussion_id}")

    async def send_message(self, message: dict, discussion_id: str):
        """Send message to all clients participating in a specific discussion"""
        if discussion_id not in self.active_connections:
            return

        disconnected = set()
        for connection in self.active_connections[discussion_id]:
            try:
                await connection.send_text(json.dumps(message, ensure_ascii=False))
            except Exception as e:
                logger.error(f"Message send error: {e}")
                disconnected.add(connection)

        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection, discussion_id)

    async def broadcast(self, message: dict):
        """Send message to all clients"""
        for discussion_id in list(self.active_connections.keys()):
            await self.send_message(message, discussion_id)


manager = ConnectionManager()
