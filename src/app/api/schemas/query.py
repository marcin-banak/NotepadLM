"""Query schemas."""

from pydantic import BaseModel


class QueryRequest(BaseModel):
    """Query request."""
    
    query: str
    k: int = 5


class QueryResponse(BaseModel):
    """Query response."""
    
    response: str

