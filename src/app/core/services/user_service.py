"""User service for user registration and authentication."""

from typing import Optional
from app.core.domain.database import UserDB
from app.core.domain.database import INoteRepository
from app.core.services.auth_service import hash_password, verify_password, create_access_token


class UserService:
    """Service for user-related operations."""
    
    def __init__(self, repository: INoteRepository):
        self.repository = repository
    
    def register_user(self, username: str, password: str) -> int:
        """Register a new user."""
        # Check if user already exists
        existing_user = self.repository.get_user_by_name(username)
        if existing_user:
            raise ValueError("Username already exists")
        
        # Hash password and create user
        password_hash = hash_password(password)
        user_db = UserDB(id=None, name=username, password_hash=password_hash)
        user_id = self.repository.create_user(user_db)
        return user_id
    
    def authenticate_user(self, username: str, password: str) -> Optional[str]:
        """Authenticate a user and return JWT token if successful."""
        user = self.repository.get_user_by_name(username)
        if not user:
            return None
        
        if not verify_password(password, user.password_hash):
            return None
        
        # Create access token
        token_data = {"sub": str(user.id), "username": user.name}
        access_token = create_access_token(data=token_data)
        return access_token
    
    def get_user_by_id(self, user_id: int) -> Optional[UserDB]:
        """Get user by ID."""
        return self.repository.get_user(user_id)
    
    def get_user_by_name(self, username: str) -> Optional[UserDB]:
        """Get user by username."""
        return self.repository.get_user_by_name(username)

