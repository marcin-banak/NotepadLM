"""Query routes."""

from fastapi import APIRouter, Depends
from typing import Annotated
from app.api.schemas.note import QueryRequest, QueryResponse, QueryResult, NoteResponse
from app.core.services.note_service import NoteService
from app.core.domain.database import UserDB
from app.dependencies import get_note_service, get_current_user

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
async def query(
    query_request: QueryRequest,
    current_user: Annotated[UserDB, Depends(get_current_user)],
    note_service: Annotated[NoteService, Depends(get_note_service)]
):
    """Query for relevant notes with chunk markers.
    
    Returns notes that contain chunks relevant to the query, along with
    markers indicating where the relevant chunk appears in each note.
    """
    # Query for relevant notes with chunk markers
    results = note_service.query_relevant_notes(
        query=query_request.query,
        user_id=current_user.id,
        k=query_request.k,
        threshold=query_request.threshold
    )
    
    # Convert to response format
    query_results = []
    for result in results:
        note = result["note"]
        query_results.append(QueryResult(
            note=NoteResponse(
                id=note.id,
                title=note.title,
                content=note.content,
                user_id=note.user_id,
                group_id=note.group_id,
                created_at=note.created_at,
                updated_at=note.updated_at
            ),
            chunk_text=result["chunk_text"],
            chunk_start=result["chunk_start"],
            chunk_end=result["chunk_end"],
            relevance_score=result["relevance_score"]
        ))
    
    return QueryResponse(results=query_results)

