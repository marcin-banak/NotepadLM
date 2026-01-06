"""Application dependencies."""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.infrastructure.bootstrap import SessionLocal
from app.infrastructure.database.repository import AppRepository
from app.core.domain.repositories.repository import INoteRepository
from app.core.services.user_service import UserService
from app.core.services.note_service import NoteService
from app.core.services.auth_service import decode_access_token
from app.core.domain.entities.user import UserDB

# Security scheme
security = HTTPBearer()


def get_repository() -> INoteRepository:
    """Get repository instance."""
    return AppRepository(SessionLocal)


def get_user_service(repository: Annotated[INoteRepository, Depends(get_repository)]) -> UserService:
    """Get user service instance."""
    return UserService(repository)


def get_note_service(repository: Annotated[INoteRepository, Depends(get_repository)]) -> NoteService:
    """Get note service instance."""
    return NoteService(repository)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> UserDB:
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = user_service.get_user_by_id(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

