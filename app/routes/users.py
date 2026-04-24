from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel
from app.database import get_db
from app.models import User
from app.auth import get_current_user

router = APIRouter()

class ProfileUpdate(BaseModel):
    username: str | None = None
    avatar: str | None = None

@router.get("/me")
async def get_my_profile(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(current_user.get("sub"))
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "phone": user.phone,
        "username": user.username,
        "avatar": user.avatar,
        "online": user.online,
        "last_seen": user.last_seen.isoformat() if user.last_seen else None
    }

@router.post("/me")
@router.put("/me")
async def update_profile(
    data: ProfileUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(current_user.get("sub"))
    
    update_data = {}
    if data.username:
        update_data["username"] = data.username
    if data.avatar:
        update_data["avatar"] = data.avatar
    
    if update_data:
        await db.execute(
            update(User)
            .where(User.id == user_id)
            .values(**update_data)
        )
        await db.commit()
    
    return {"message": "Profile updated"}

@router.get("/{user_id}/status")
async def get_user_status(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "online": user.online,
        "last_seen": user.last_seen.isoformat() if user.last_seen else None
    }