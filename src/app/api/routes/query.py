"""Query routes (RAG)."""

from fastapi import APIRouter, Depends, HTTPException, status

from ...core.domain.entities.user import User
from ...core.services.query.query_notes import QueryNotesUseCase
from ...api.schemas.query import QueryRequest, QueryResponse
from ...api.dependencies import get_current_user
from ...infrastructure.bootstrap import get_query_notes_use_case

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
def query_notes(
    request: QueryRequest,
    current_user: User = Depends(get_current_user),
    query_use_case: QueryNotesUseCase = Depends(get_query_notes_use_case),
):
    """Query notes using RAG."""
    try:
        response = query_use_case.execute(
            user_id=current_user.id,
            query=request.query,
            k=request.k,
        )
        
        return QueryResponse(response=response)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query failed: {str(e)}",
        )

