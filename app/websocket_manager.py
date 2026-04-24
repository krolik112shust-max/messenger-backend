from fastapi import WebSocket
from typing import Dict, Set
from datetime import datetime
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
        await self.set_user_online(user_id, True)

    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        asyncio.create_task(self.set_user_online(user_id, False))

    async def set_user_online(self, user_id: int, online: bool):
        from app.database import AsyncSessionLocal
        from app.models import User
        from sqlalchemy import update
        
        async with AsyncSessionLocal() as db:
            await db.execute(
                update(User)
                .where(User.id == user_id)
                .values(online=online, last_seen=datetime.utcnow())
            )
            await db.commit()

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            for conn in self.active_connections[user_id]:
                try:
                    await conn.send_json(message)
                except:
                    pass

manager = ConnectionManager()