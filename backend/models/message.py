"""Message model definitions"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class MessageType(str, Enum):
    """Message type"""
    SYSTEM = "system"
    OPINION = "opinion"
    VOTE = "vote"
    PERSUASION = "persuasion"
    RESPONSE = "response"
    CONCLUSION = "conclusion"


class Message(BaseModel):
    """Message model"""
    id: str = Field(..., description="Message ID")
    agent_id: str = Field(..., description="ID of the agent who spoke")
    agent_name: str = Field(..., description="Name of the agent who spoke")
    content: str = Field(..., description="Message content")
    message_type: MessageType = Field(..., description="Message type")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp sent")


class Opinion(BaseModel):
    """Opinion model"""
    id: str = Field(..., description="Opinion ID")
    agent_id: str = Field(..., description="ID of the agent who gave the opinion")
    agent_name: str = Field(..., description="Name of the agent who gave the opinion")
    content: str = Field(..., description="Opinion content")
    votes: int = Field(default=0, description="Number of votes received")
