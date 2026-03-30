from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User, Chat, ChatParticipant, Message
from app.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.get("/{chat_id}")
async def get_messages(
    chat_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить историю сообщений"""
    user_id = int(current_user.get("sub"))
    
    # Проверяем, является ли пользователь участником чата
    participant = await db.execute(
        select(ChatParticipant)
        .where(
            ChatParticipant.chat_id == chat_id,
            ChatParticipant.user_id == user_id
        )
    )
    if not participant.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Not a participant")
    
    result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at.desc())
        .limit(50)
    )
    messages = result.scalars().all()
    
    return [{
        "id": msg.id,
        "chat_id": msg.chat_id,
        "sender_id": msg.sender_id,
        "type": msg.type,
        "content": msg.content,
        "created_at": msg.created_at.isoformat(),
        "status": msg.status
    } for msg in messages]

@router.post("/")
async def send_message(
    chat_id: int,
    content: str,
    type: str = "text",
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Отправить сообщение"""
    user_id = int(current_user.get("sub"))
    
    # Проверяем, является ли пользователь участником чата
    participant = await db.execute(
        select(ChatParticipant)
        .where(
            ChatParticipant.chat_id == chat_id,
            ChatParticipant.user_id == user_id
        )
    )
    if not participant.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Not a participant")
    
    message = Message(
        chat_id=chat_id,
        sender_id=user_id,
        type=type,
        content=content,
        created_at=datetime.utcnow()
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    
    return {
        "id": message.id,
        "chat_id": message.chat_id,
        "sender_id": message.sender_id,
        "type": message.type,
        "content": message.content,
        "created_at": message.created_at.isoformat(),
        "status": message.status
    }