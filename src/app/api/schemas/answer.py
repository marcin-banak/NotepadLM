"""Answer schemas."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class AskRequest(BaseModel):
    """Ask request schema."""
    query: str
    k: Optional[int] = 10


class ReferenceInfo(BaseModel):
    """Reference information schema."""
    note_id: int
    chunk_id: int
    chunk_text: str


class AskResponse(BaseModel):
    """Ask response schema."""
    answer_id: int
    title: str
    answer_text: str
    references: Dict[str, Dict[str, Any]]


class AnswerResponse(BaseModel):
    """Full answer response schema."""
    id: int
    user_id: int
    question: str
    answer_text: str
    title: str
    references: Dict[str, Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

