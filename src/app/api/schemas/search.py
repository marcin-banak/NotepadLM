"""Search schemas."""

from pydantic import BaseModel


class SearchRequest(BaseModel):
    """Search request."""
    
    query: str
    k: int = 10


class SearchResult(BaseModel):
    """Search result."""
    
    note_id: str
    similarity_score: float


class SearchResponse(BaseModel):
    """Search response."""
    
    results: list[SearchResult]

