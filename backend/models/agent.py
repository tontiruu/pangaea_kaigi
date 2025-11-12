"""Agent モデル定義"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class AgentRole(str, Enum):
    """Agent の役割"""
    FACILITATOR = "facilitator"
    PARTICIPANT = "participant"


class Agent(BaseModel):
    """Agent モデル"""
    id: str = Field(..., description="Agent の一意なID")
    name: str = Field(..., description="Agent の名前")
    role: AgentRole = Field(..., description="Agent の役割")
    perspective: str = Field(..., description="Agent の観点・専門性")
    response_id: Optional[str] = Field(None, description="OpenAI response_id チェーン")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "agent_001",
                "name": "財務担当",
                "role": "participant",
                "perspective": "財務的な観点から、コスト効率と収益性を重視して意見を述べる",
                "response_id": None
            }
        }
