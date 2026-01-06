"""Authentication routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.api.schemas.auth import UserRegister, UserLogin, TokenResponse
from app.api.schemas.user import UserResponse
from app.core.services.user_service import UserService
from app.dependencies import get_user_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Register a new user."""
    try:
        user_id = user_service.register_user(user_data.username, user_data.password)
        user = user_service.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
        return UserResponse(id=user.id, name=user.name)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Login and get access token."""
    token = user_service.authenticate_user(credentials.username, credentials.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenResponse(access_token=token)

