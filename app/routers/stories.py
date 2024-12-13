from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_user_stories(session_id: str = None):
    # Lógica para obtener historias de usuario basadas en session_id
    return {"message": "Historias de usuario"}
