"""Note schemas."""

from datetime import datetime
from typing import Optional, List, Dict, Any
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
    references: Optional[Dict[str, Dict[str, Any]]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BulkNoteCreate(BaseModel):
    """Bulk note creation request schema."""
    notes: List[NoteCreate]


class BulkNoteResponse(BaseModel):
    """Bulk note creation response schema."""
    created: List[NoteResponse]
    failed: List[dict]


class QueryRequest(BaseModel):
    """Query request schema."""
    query: str
    k: Optional[int] = 10
    threshold: Optional[float] = 0.4


class QueryResult(BaseModel):
    """Query result schema with chunk markers."""
    note: NoteResponse
    chunk_text: str
    chunk_start: int
    chunk_end: int
    relevance_score: float


class QueryResponse(BaseModel):
    """Query response schema."""
    results: List[QueryResult]

