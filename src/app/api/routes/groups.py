"""Group routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("")
async def list_groups():
    """List groups - to be implemented."""
    return {"message": "Groups endpoint - to be implemented"}


@router.get("/{group_id}")
async def get_group(group_id: int):
    """Get a specific group - to be implemented."""
    return {"message": f"Get group {group_id} - to be implemented"}

