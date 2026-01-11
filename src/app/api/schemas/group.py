"""Group schemas."""

from typing import Optional, List
from pydantic import BaseModel
from app.api.schemas.note import NoteResponse


class GroupResponse(BaseModel):
    """Group response schema."""
    id: int
    user_id: int
    summary: Optional[str]
    notes: List[NoteResponse] = []
    
    class Config:
        from_attributes = True


class GroupUpdate(BaseModel):
    """Group update request schema."""
    summary: Optional[str] = None

