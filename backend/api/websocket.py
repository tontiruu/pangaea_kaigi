"""WebSocket接続管理"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """WebSocket接続を管理するクラス"""

    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, discussion_id: str):
        """クライアントを接続"""
        await websocket.accept()
        if discussion_id not in self.active_connections:
            self.active_connections[discussion_id] = set()
        self.active_connections[discussion_id].add(websocket)
        logger.info(f"WebSocket接続: {discussion_id}")

    def disconnect(self, websocket: WebSocket, discussion_id: str):
        """クライアントを切断"""
        if discussion_id in self.active_connections:
            self.active_connections[discussion_id].discard(websocket)
            if not self.active_connections[discussion_id]:
                del self.active_connections[discussion_id]
        logger.info(f"WebSocket切断: {discussion_id}")

    async def send_message(self, message: dict, discussion_id: str):
        """特定の議論に参加している全クライアントにメッセージを送信"""
        if discussion_id not in self.active_connections:
            return

        disconnected = set()
        for connection in self.active_connections[discussion_id]:
            try:
                await connection.send_text(json.dumps(message, ensure_ascii=False))
            except Exception as e:
                logger.error(f"メッセージ送信エラー: {e}")
                disconnected.add(connection)

        # 切断されたクライアントを削除
        for connection in disconnected:
            self.disconnect(connection, discussion_id)

    async def broadcast(self, message: dict):
        """全クライアントにメッセージを送信"""
        for discussion_id in list(self.active_connections.keys()):
            await self.send_message(message, discussion_id)


manager = ConnectionManager()
