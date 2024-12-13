from fastapi import APIRouter

router = APIRouter()

@router.get("/tests/playwright")
async def generate_tests():
    return {"message": "Tests generados"}