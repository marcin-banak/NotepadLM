"""Group routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List
from app.api.schemas.group import GroupResponse, GroupUpdate
from app.api.schemas.note import NoteResponse
from app.core.domain.database import UserDB
from app.core.domain.database import INoteRepository
from app.dependencies import get_repository, get_current_user

router = APIRouter(prefix="/groups", tags=["groups"])


def _group_db_to_response(group_db, repository: INoteRepository) -> GroupResponse:
    """Convert GroupDB to GroupResponse."""
    notes = []
    for note in group_db.notes:
        # Fetch full note details to get created_at and updated_at
        full_note = repository.get_note(note.id)
        if full_note:
            notes.append(
                NoteResponse(
                    id=full_note.id,
                    title=full_note.title,
                    content=full_note.content,
                    user_id=full_note.user_id,
                    group_id=full_note.group_id,
                    created_at=full_note.created_at,
                    updated_at=full_note.updated_at
                )
            )
    return GroupResponse(
        id=group_db.id,
        user_id=group_db.user_id,
        summary=group_db.summary,
        notes=notes
    )


@router.get("", response_model=List[GroupResponse])
async def list_groups(
    current_user: Annotated[UserDB, Depends(get_current_user)],
    repository: Annotated[INoteRepository, Depends(get_repository)]
):
    """List all groups for the current user."""
    groups = repository.get_groups_by_user(current_user.id)
    return [_group_db_to_response(group, repository) for group in groups]


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: int,
    current_user: Annotated[UserDB, Depends(get_current_user)],
    repository: Annotated[INoteRepository, Depends(get_repository)]
):
    """Get a specific group by ID."""
    group = repository.get_group(group_id)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    if group.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    return _group_db_to_response(group, repository)


@router.put("/{group_id}", response_model=GroupResponse)
async def update_group(
    group_id: int,
    group_data: GroupUpdate,
    current_user: Annotated[UserDB, Depends(get_current_user)],
    repository: Annotated[INoteRepository, Depends(get_repository)]
):
    """Update a group."""
    group = repository.get_group(group_id)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    if group.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update the group
    if group_data.summary is not None:
        group.summary = group_data.summary
    
    updated_id = repository.update_group(group)
    if updated_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update group"
        )
    
    updated_group = repository.get_group(updated_id)
    if updated_group is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve updated group"
        )
    
    return _group_db_to_response(updated_group, repository)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: int,
    current_user: Annotated[UserDB, Depends(get_current_user)],
    repository: Annotated[INoteRepository, Depends(get_repository)]
):
    """Delete a group."""
    group = repository.get_group(group_id)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    if group.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    success = repository.delete_group(group_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete group"
        )
    return None

