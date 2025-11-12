"""Discussion session model definitions"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class DiscussionPhase(str, Enum):
    """Discussion phase"""
    INITIALIZING = "initializing"
    AGENDA_CREATION = "agenda_creation"
    AGENT_GENERATION = "agent_generation"
    INDEPENDENT_OPINIONS = "independent_opinions"
    VOTING = "voting"
    PERSUASION = "persuasion"
    COMPLETED = "completed"


class AgendaItem(BaseModel):
    """Agenda item"""
    id: str = Field(..., description="Agenda ID")
    title: str = Field(..., description="Agenda title")
    description: str = Field(..., description="Agenda details")
    order: int = Field(..., description="Discussion order")
    conclusion: Optional[str] = Field(None, description="Conclusion")


class DiscussionSession(BaseModel):
    """Discussion session"""
    id: str = Field(..., description="Session ID")
    topic: str = Field(..., description="Discussion topic")
    agenda: List[AgendaItem] = Field(default_factory=list, description="Agenda list")
    current_agenda_index: int = Field(default=0, description="Current agenda index")
    phase: DiscussionPhase = Field(default=DiscussionPhase.INITIALIZING, description="Current phase")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    final_conclusion: Optional[str] = Field(None, description="Final conclusion")
