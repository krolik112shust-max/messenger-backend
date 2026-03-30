from fastapi import APIRouter, Depends
from app.auth import get_current_user

router = APIRouter()

@router.post("/")
async def upload_file(payload: dict = Depends(get_current_user)):
    """Загрузка файлов (временно заглушка)"""
    return {"message": "Upload endpoint будет добавлен позже"}