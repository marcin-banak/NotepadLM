"""Note schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CreateNoteRequest(BaseModel):
    """Create note request."""
    
    title: str
    content: str


class NoteResponse(BaseModel):
    """Note response."""
    
    id: str
    user_id: str
    group_id: Optional[str]
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

