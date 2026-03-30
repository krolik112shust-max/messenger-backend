from fastapi import FastAPI
from app.routes import auth, users, chats, messages, upload

app = FastAPI(title="Messenger API", version="1.0.0")

app.include_router(auth.router, prefix="/auth", tags=["Авторизация"])
app.include_router(users.router, prefix="/users", tags=["Пользователи"])
app.include_router(chats.router, prefix="/chats", tags=["Чаты"])
app.include_router(messages.router, prefix="/messages", tags=["Сообщения"])
app.include_router(upload.router, prefix="/upload", tags=["Загрузка файлов"])

@app.get("/")
async def root():
    return {"message": "Messenger API работает!"}