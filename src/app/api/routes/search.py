"""Search routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
async def search():
    """Search endpoint - to be implemented."""
    return {"message": "Search endpoint - to be implemented"}

