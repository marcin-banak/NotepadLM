"""Group routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ...core.domain.entities.user import User
from ...core.domain.value_objects.ids import GroupId
from ...core.domain.repositories.group_repository import IGroupRepository
from ...api.schemas.groups import GroupResponse
from ...api.dependencies import get_current_user
from ...infrastructure.bootstrap import get_group_repository

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("", response_model=List[GroupResponse])
def list_groups(
    current_user: User = Depends(get_current_user),
    group_repository: IGroupRepository = Depends(get_group_repository),
):
    """List all groups for the current user."""
    groups = group_repository.find_by_user_id(current_user.id)
    
    return [
        GroupResponse(
            id=str(group.id),
            user_id=str(group.user_id),
            summary=group.summary,
            created_at=group.created_at,
            updated_at=group.updated_at,
        )
        for group in groups
    ]


@router.get("/{group_id}", response_model=GroupResponse)
def get_group(
    group_id: str,
    current_user: User = Depends(get_current_user),
    group_repository: IGroupRepository = Depends(get_group_repository),
):
    """Get a specific group."""
    group = group_repository.find_by_id(GroupId(group_id))
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )
    
    if group.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    
    return GroupResponse(
        id=str(group.id),
        user_id=str(group.user_id),
        summary=group.summary,
        created_at=group.created_at,
        updated_at=group.updated_at,
    )

