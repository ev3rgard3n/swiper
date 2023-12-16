from typing import AsyncGenerator

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import DATABASE_URL


class Base(DeclarativeBase):
    ...


async_engine = create_async_engine(url=DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session