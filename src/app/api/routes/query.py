"""Query routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/query", tags=["query"])


@router.post("")
async def query():
    """Query endpoint - to be implemented."""
    return {"message": "Query endpoint - to be implemented"}

