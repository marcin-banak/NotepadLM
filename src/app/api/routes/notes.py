"""Note routes."""

from fastapi import APIRouter, Depends, HTTPException, status

from ...core.domain.entities.user import User
from ...core.domain.value_objects.ids import NoteId
from ...core.services.notes.create_note import CreateNoteUseCase
from ...core.services.notes.delete_note import DeleteNoteUseCase
from ...api.schemas.notes import CreateNoteRequest, NoteResponse
from ...api.dependencies import get_current_user
from ...infrastructure.bootstrap import (
    get_create_note_use_case,
    get_delete_note_use_case,
)

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteResponse)
def create_note(
    request: CreateNoteRequest,
    current_user: User = Depends(get_current_user),
    create_use_case: CreateNoteUseCase = Depends(get_create_note_use_case),
):
    """Create a new note."""
    try:
        note = create_use_case.execute(
            user_id=current_user.id,
            title=request.title,
            content=request.content,
        )
        
        return NoteResponse(
            id=str(note.id),
            user_id=str(note.user_id),
            group_id=str(note.group_id) if note.group_id else None,
            title=note.title,
            content=note.content,
            created_at=note.created_at,
            updated_at=note.updated_at,
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: str,
    current_user: User = Depends(get_current_user),
    delete_use_case: DeleteNoteUseCase = Depends(get_delete_note_use_case),
):
    """Delete a note."""
    try:
        delete_use_case.execute(
            note_id=NoteId(note_id),
            user_id=current_user.id,
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

