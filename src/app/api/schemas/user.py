"""User schemas."""

from pydantic import BaseModel


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    name: str
    
    class Config:
        from_attributes = True

