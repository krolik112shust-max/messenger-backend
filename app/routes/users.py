from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User
from app.auth import get_current_user

router = APIRouter()

@router.get("/me")
async def get_my_profile(payload: dict = Depends(get_current_user)):
    """Получить профиль текущего пользователя"""
    return {
        "user_id": payload.get("sub"),
        "message": "Профиль пользователя"
    }

@router.get("/search/{phone}")
async def search_user_by_phone(
    phone: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Поиск пользователя по номеру телефона"""
    print(f"Поиск пользователя по номеру: {phone}")  # Отладка
    
    result = await db.execute(
        select(User).where(User.phone == phone)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        print(f"Пользователь с номером {phone} не найден")
        raise HTTPException(status_code=404, detail="User not found")
    
    print(f"Найден пользователь: id={user.id}, phone={user.phone}")
    
    return {
        "id": user.id,
        "phone": user.phone,
        "username": user.username,
        "avatar": user.avatar
    }