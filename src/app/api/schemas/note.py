"""Note schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class NoteCreate(BaseModel):
    """Note creation request schema."""
    title: str
    content: str
    group_id: Optional[int] = None


class NoteUpdate(BaseModel):
    """Note update request schema."""
    title: Optional[str] = None
    content: Optional[str] = None
    group_id: Optional[int] = None


class NoteResponse(BaseModel):
    """Note response schema."""
    id: int
    title: str
    content: str
    user_id: int
    group_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

