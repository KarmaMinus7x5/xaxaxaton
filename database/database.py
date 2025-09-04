"""
Подключение к базе данных
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config.settings import DATABASE_URL, LOG_LEVEL
from database.models import Base

# Создание асинхронного движка БД
engine = create_async_engine(DATABASE_URL, echo=(LOG_LEVEL.upper()=='DEBUG'))
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Инициализация базы данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)