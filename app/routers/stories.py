from fastapi import APIRouter, Query
from app.services import get_user_stories

router = APIRouter()

@router.get("/")
async def get_stories(session_id: str = Query(None)):
    stories = await get_user_stories(session_id)
    return stories