"""Application dependencies."""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.infrastructure.bootstrap import database_repository, vector_store, clusterizer, llm
from app.core.domain.database import INoteRepository
from app.core.domain.vectorstore import IVectorStore
from app.core.domain.clusterization import IClusterizer
from app.core.services.user_service import UserService
from app.core.services.note_service import NoteService
from app.core.services.answer_service import AnswerService
from app.core.services.auth_service import decode_access_token
from app.core.domain.database import UserDB

# Security scheme
security = HTTPBearer()


def get_repository() -> INoteRepository:
    """Get repository instance."""
    return database_repository


def get_user_service(repository: Annotated[INoteRepository, Depends(get_repository)]) -> UserService:
    """Get user service instance."""
    return UserService(repository)


def get_vector_store() -> IVectorStore:
    """Get vector store instance."""
    return vector_store


def get_clusterizer() -> IClusterizer:
    """Get clusterizer instance."""
    return clusterizer


def get_note_service(
    repository: Annotated[INoteRepository, Depends(get_repository)],
    vector_store: Annotated[IVectorStore, Depends(get_vector_store)],
    clusterizer: Annotated[IClusterizer, Depends(get_clusterizer)]
) -> NoteService:
    """Get note service instance."""
    return NoteService(repository, vector_store, clusterizer)


def get_answer_service(
    repository: Annotated[INoteRepository, Depends(get_repository)],
    vector_store: Annotated[IVectorStore, Depends(get_vector_store)],
    note_service: Annotated[NoteService, Depends(get_note_service)]
) -> AnswerService:
    """Get answer service instance."""
    return AnswerService(repository, vector_store, llm, note_service)

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

