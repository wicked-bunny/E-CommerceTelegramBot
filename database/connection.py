import os
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# Імпортуйте вашу BaseModel (замініть .models на правильний шлях, якщо треба)
from database.models import BaseModel

# 1. Створення рушія (engine)
engine = create_async_engine(
    url="sqlite+aiosqlite:///DB.db",
    isolation_level="AUTOCOMMIT"
)

# 2. Створення фабрики сесій
session_maker = async_sessionmaker[AsyncSession](engine, expire_on_commit=False)

# 3. Функція ініціалізації моделей
async def init_model(engine=engine):
    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA journal_mode=WAL;"))
        await conn.run_sync(BaseModel.metadata.create_all)
