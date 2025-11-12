"""Agent model definitions"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class AgentRole(str, Enum):
    """Agent role"""
    FACILITATOR = "facilitator"
    PARTICIPANT = "participant"


class Agent(BaseModel):
    """Agent model"""
    id: str = Field(..., description="Agent's unique ID")
    name: str = Field(..., description="Agent's name")
    role: AgentRole = Field(..., description="Agent's role")
    perspective: str = Field(..., description="Agent's perspective and expertise")
    response_id: Optional[str] = Field(None, description="OpenAI response_id chain")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "agent_001",
                "name": "Finance Manager",
                "role": "participant",
                "perspective": "Provides opinions from a financial perspective, emphasizing cost efficiency and profitability",
                "response_id": None
            }
        }
