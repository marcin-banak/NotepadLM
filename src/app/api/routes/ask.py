"""Ask routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.api.schemas.answer import AskRequest, AskResponse, AnswerResponse
from typing import List
from app.core.services.answer_service import AnswerService
from app.core.domain.database import UserDB
from app.dependencies import get_current_user, get_answer_service

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

