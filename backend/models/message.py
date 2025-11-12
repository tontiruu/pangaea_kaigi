"""メッセージモデル定義"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class MessageType(str, Enum):
    """メッセージタイプ"""
    SYSTEM = "system"
    OPINION = "opinion"
    VOTE = "vote"
    PERSUASION = "persuasion"
    RESPONSE = "response"
    CONCLUSION = "conclusion"


class Message(BaseModel):
    """メッセージモデル"""
    id: str = Field(..., description="メッセージID")
    agent_id: str = Field(..., description="発言したAgentのID")
    agent_name: str = Field(..., description="発言したAgentの名前")
    content: str = Field(..., description="メッセージ内容")
    message_type: MessageType = Field(..., description="メッセージタイプ")
    timestamp: datetime = Field(default_factory=datetime.now, description="送信時刻")


class Opinion(BaseModel):
    """意見モデル"""
    id: str = Field(..., description="意見ID")
    agent_id: str = Field(..., description="意見を述べたAgentのID")
    agent_name: str = Field(..., description="意見を述べたAgentの名前")
    content: str = Field(..., description="意見内容")
    votes: int = Field(default=0, description="獲得票数")
