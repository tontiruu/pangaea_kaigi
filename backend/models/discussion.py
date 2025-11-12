"""議論セッションモデル定義"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class DiscussionPhase(str, Enum):
    """議論のフェーズ"""
    INITIALIZING = "initializing"
    AGENDA_CREATION = "agenda_creation"
    AGENT_GENERATION = "agent_generation"
    INDEPENDENT_OPINIONS = "independent_opinions"
    VOTING = "voting"
    PERSUASION = "persuasion"
    COMPLETED = "completed"


class AgendaItem(BaseModel):
    """アジェンダアイテム"""
    id: str = Field(..., description="アジェンダID")
    title: str = Field(..., description="アジェンダタイトル")
    description: str = Field(..., description="アジェンダ詳細")
    order: int = Field(..., description="議論順序")
    conclusion: Optional[str] = Field(None, description="結論")


class DiscussionSession(BaseModel):
    """議論セッション"""
    id: str = Field(..., description="セッションID")
    topic: str = Field(..., description="議論する議題")
    agenda: List[AgendaItem] = Field(default_factory=list, description="アジェンダリスト")
    current_agenda_index: int = Field(default=0, description="現在のアジェンダインデックス")
    phase: DiscussionPhase = Field(default=DiscussionPhase.INITIALIZING, description="現在のフェーズ")
    created_at: datetime = Field(default_factory=datetime.now, description="作成日時")
    final_conclusion: Optional[str] = Field(None, description="最終結論")
