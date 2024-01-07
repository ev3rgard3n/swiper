from typing import AsyncGenerator

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import DATABASE_URL


class Base(DeclarativeBase):
    ...
    # repr_cols_num = 3
    # repr_cols = tuple()
    
    # def __repr__(self):
    #     """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
    #     cols = []
    #     for idx, col in enumerate(self.__table__.columns.keys()):
    #         if col in self.repr_cols or idx < self.repr_cols_num:
    #             cols.append(f"{col}={getattr(self, col)}")

    #     return f"<{self.__class__.__name__} {', '.join(cols)}>"


async_engine = create_async_engine(url=DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session