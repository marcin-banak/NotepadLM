"""Authentication schemas."""

from pydantic import BaseModel


class UserRegister(BaseModel):
    """User registration request schema."""
    username: str
    password: str


class UserLogin(BaseModel):
    """User login request schema."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"

