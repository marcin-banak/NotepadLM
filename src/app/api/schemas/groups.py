"""Group schemas."""

from datetime import datetime
from pydantic import BaseModel


class GroupResponse(BaseModel):
    """Group response."""
    
    id: str
    user_id: str
    summary: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

