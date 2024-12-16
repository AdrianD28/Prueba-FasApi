from fastapi import APIRouter
from app.services import generate_tests

router = APIRouter()

@router.get("/")
async def get_tests(story_id: str):
    tests = await generate_tests(story_id)
    return tests