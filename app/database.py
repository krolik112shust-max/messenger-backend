from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Получаем URL из настроек и меняем протокол для asyncpg
DATABASE_URL = settings.database_url.replace('postgresql://', 'postgresql+asyncpg://')

# Убираем sslmode из URL, так как asyncpg его не понимает
if "?sslmode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?sslmode=")[0]

# Создаем движок. Если хост содержит neon.tech, включаем SSL через connect_args
connect_args = {}
if "neon.tech" in DATABASE_URL:
    connect_args = {"ssl": "require"}

engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    connect_args=connect_args
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session