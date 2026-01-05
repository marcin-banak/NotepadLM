"""Search routes."""

from fastapi import APIRouter, Depends, HTTPException, status

from ...core.domain.entities.user import User
from ...core.services.query.search_notes import SearchNotesUseCase
from ...api.schemas.search import SearchRequest, SearchResponse, SearchResult
from ...api.dependencies import get_current_user
from ...infrastructure.bootstrap import get_search_notes_use_case

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=SearchResponse)
def search_notes(
    request: SearchRequest,
    current_user: User = Depends(get_current_user),
    search_use_case: SearchNotesUseCase = Depends(get_search_notes_use_case),
):
    """Search notes using semantic similarity."""
    try:
        results = search_use_case.execute(
            user_id=current_user.id,
            query=request.query,
            k=request.k,
        )
        
        return SearchResponse(
            results=[
                SearchResult(
                    note_id=str(result.note_id),
                    similarity_score=result.similarity_score,
                )
                for result in results
            ]
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}",
        )

