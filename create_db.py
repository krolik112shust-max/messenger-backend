import asyncio
from app.database import engine
from app.models import Base

async def init_db():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
  print("✅ База данных создана!")

asyncio.run(init_db())
