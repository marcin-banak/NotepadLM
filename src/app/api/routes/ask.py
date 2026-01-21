"""Ask routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.api.schemas.answer import AskRequest, AskResponse, AnswerResponse
from app.api.schemas.note import NoteResponse
from typing import List
from app.core.services.answer_service import AnswerService
from app.core.services.note_service import NoteService
from app.core.domain.database import UserDB
from app.dependencies import get_current_user, get_answer_service, get_note_service

router = APIRouter(prefix="/ask", tags=["ask"])


@router.post("", response_model=AskResponse)
async def ask(
    ask_request: AskRequest,
    current_user: Annotated[UserDB, Depends(get_current_user)],
    answer_service: Annotated[AnswerService, Depends(get_answer_service)]
):
    """Ask a question and get an LLM-generated answer based on user's notes.
    
    Returns an answer with citations to source notes.
    """
    if not ask_request.query or not ask_request.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty"
        )
    
    # Generate answer
    answer = answer_service.generate_answer(
        query=ask_request.query.strip(),
        user_id=current_user.id,
        k=ask_request.k or 10
    )
    
    return AskResponse(
        answer_id=answer.id,
        title=answer.title,
        answer_text=answer.answer_text,
        references=answer.references
    )


@router.get("/answer/{answer_id}", response_model=AnswerResponse)
async def get_answer(
    answer_id: int,
    current_user: Annotated[UserDB, Depends(get_current_user)],
    answer_service: Annotated[AnswerService, Depends(get_answer_service)]
):
    """Get a specific answer by ID."""
    answer = answer_service.get_answer(answer_id, current_user.id)
    
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    
    return AnswerResponse(
        id=answer.id,
        user_id=answer.user_id,
        question=answer.question,
        answer_text=answer.answer_text,
        title=answer.title,
        references=answer.references,
        created_at=answer.created_at,
        updated_at=answer.updated_at
    )


@router.get("/answers", response_model=List[AnswerResponse])
async def get_user_answers(
    current_user: Annotated[UserDB, Depends(get_current_user)],
    answer_service: Annotated[AnswerService, Depends(get_answer_service)]
):
    """Get all answers for the current user."""
    answers = answer_service.get_answers_by_user(current_user.id)
    
    return [
        AnswerResponse(
            id=answer.id,
            user_id=answer.user_id,
            question=answer.question,
            answer_text=answer.answer_text,
            title=answer.title,
            references=answer.references,
            created_at=answer.created_at,
            updated_at=answer.updated_at
        )
        for answer in answers
    ]


@router.delete("/answer/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(
    answer_id: int,
    current_user: Annotated[UserDB, Depends(get_current_user)],
    answer_service: Annotated[AnswerService, Depends(get_answer_service)]
):
    """Delete an answer."""
    success = answer_service.delete_answer(answer_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found or access denied"
        )
    return None


@router.post("/answer/{answer_id}/convert-to-note", response_model=NoteResponse)
async def convert_answer_to_note(
    answer_id: int,
    current_user: Annotated[UserDB, Depends(get_current_user)],
    answer_service: Annotated[AnswerService, Depends(get_answer_service)],
    note_service: Annotated[NoteService, Depends(get_note_service)]
):
    """Convert an answer to a note and delete the answer."""
    note_id = answer_service.convert_answer_to_note(answer_id, current_user.id)
    
    if note_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found, access denied, or conversion failed"
        )
    
    # Get the created note
    note = note_service.get_note(note_id, current_user.id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve created note"
        )
    
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        user_id=note.user_id,
        group_id=note.group_id,
        references=note.references,
        created_at=note.created_at,
        updated_at=note.updated_at
    )

