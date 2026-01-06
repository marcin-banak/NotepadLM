"""Note routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List
from app.api.schemas.note import NoteCreate, NoteResponse, NoteUpdate
from app.core.services.note_service import NoteService
from app.core.domain.entities.user import UserDB
from app.dependencies import get_note_service, get_current_user

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreate,
    current_user: Annotated[UserDB, Depends(get_current_user)],
    note_service: Annotated[NoteService, Depends(get_note_service)]
):
    """Create a new note."""
    note_id = note_service.create_note(
        title=note_data.title,
        content=note_data.content,
        user_id=current_user.id,
        group_id=note_data.group_id
    )
    note = note_service.get_note(note_id, current_user.id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create note"
        )
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        user_id=note.user_id,
        group_id=note.group_id,
        created_at=note.created_at,
        updated_at=note.updated_at
    )


@router.get("", response_model=List[NoteResponse])
async def list_notes(
    current_user: Annotated[UserDB, Depends(get_current_user)],
    note_service: Annotated[NoteService, Depends(get_note_service)]
):
    """List all notes for the current user."""
    notes = note_service.get_notes_by_user(current_user.id)
    return [
        NoteResponse(
            id=note.id,
            title=note.title,
            content=note.content,
            user_id=note.user_id,
            group_id=note.group_id,
            created_at=note.created_at,
            updated_at=note.updated_at
        )
        for note in notes
    ]


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    current_user: Annotated[UserDB, Depends(get_current_user)],
    note_service: Annotated[NoteService, Depends(get_note_service)]
):
    """Get a specific note by ID."""
    note = note_service.get_note(note_id, current_user.id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        user_id=note.user_id,
        group_id=note.group_id,
        created_at=note.created_at,
        updated_at=note.updated_at
    )


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    current_user: Annotated[UserDB, Depends(get_current_user)],
    note_service: Annotated[NoteService, Depends(get_note_service)]
):
    """Update a note."""
    updated_id = note_service.update_note(
        note_id=note_id,
        user_id=current_user.id,
        title=note_data.title,
        content=note_data.content,
        group_id=note_data.group_id
    )
    if updated_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found or access denied"
        )
    note = note_service.get_note(updated_id, current_user.id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve updated note"
        )
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        user_id=note.user_id,
        group_id=note.group_id,
        created_at=note.created_at,
        updated_at=note.updated_at
    )


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    current_user: Annotated[UserDB, Depends(get_current_user)],
    note_service: Annotated[NoteService, Depends(get_note_service)]
):
    """Delete a note."""
    success = note_service.delete_note(note_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found or access denied"
        )
    return None

