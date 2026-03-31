from fastapi import FastAPI
from app.routes import auth, users, chats, messages, upload
from app.database import engine
from app.models import Base
import asyncio

app = FastAPI(title="Messenger API", version="1.0.0")

# Создание таблиц при запуске сервера
@app.on_event("startup")
async def startup():
    print("🚀 Запуск сервера...")
    print("📦 Создание таблиц в базе данных...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ База данных и таблицы успешно созданы!")

# Подключаем все роутеры
app.include_router(auth.router, prefix="/auth", tags=["Авторизация"])
app.include_router(users.router, prefix="/users", tags=["Пользователи"])
app.include_router(chats.router, prefix="/chats", tags=["Чаты"])
app.include_router(messages.router, prefix="/messages", tags=["Сообщения"])
app.include_router(upload.router, prefix="/upload", tags=["Загрузка файлов"])

@app.get("/")
async def root():
    return {"message": "Messenger API работает!"}