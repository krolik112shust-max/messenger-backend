from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import Chat, ChatParticipant, Message
from app.auth import get_current_user

router = APIRouter()

@router.get("/")
async def get_chats(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить список чатов пользователя с последним сообщением"""
    user_id = int(current_user.get("sub"))
    
    # Получаем все чаты пользователя
    result = await db.execute(
        select(Chat)
        .join(ChatParticipant)
        .where(ChatParticipant.user_id == user_id)
    )
    chats = result.scalars().all()
    
    # Для каждого чата получаем последнее сообщение
    chats_list = []
    for chat in chats:
        # Получаем последнее сообщение
        msg_result = await db.execute(
            select(Message)
            .where(Message.chat_id == chat.id)
            .order_by(Message.created_at.desc())
            .limit(1)
        )
        last_msg = msg_result.scalar_one_or_none()
        
        chats_list.append({
            "id": chat.id,
            "name": chat.name or "Чат",
            "type": chat.type,
            "last_message": {
                "content": last_msg.content if last_msg else None,
                "created_at": last_msg.created_at.isoformat() if last_msg else None
            } if last_msg else None
        })
    
    return chats_list

@router.post("/")
async def create_chat(
    user_ids: list[int],
    name: str = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Создать новый чат"""
    current_user_id = int(current_user.get("sub"))
    all_user_ids = list(set(user_ids + [current_user_id]))
    
    chat = Chat(type="private" if len(all_user_ids) == 2 else "group", name=name)
    db.add(chat)
    await db.flush()
    
    for uid in all_user_ids:
        participant = ChatParticipant(chat_id=chat.id, user_id=uid)
        db.add(participant)
    
    await db.commit()
    await db.refresh(chat)
    
    return {"id": chat.id, "type": chat.type, "name": chat.name}