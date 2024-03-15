from sqlalchemy import select, insert, delete, update, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.interfaces import AbstactDAO


class SQLAlchemyDAO(AbstactDAO):
    model = None

    @classmethod
    async def find_all(cls, db: AsyncSession, **filter_by):
        stmt = select(cls.model).filter_by(**filter_by)
        res = await db.execute(stmt)

        return res.scalars().all()

    @classmethod
    async def find_one_or_none(cls, db: AsyncSession, **filter_by):
        stmt = select(cls.model).filter_by(**filter_by)
        res = await db.execute(stmt)

        return res.scalar_one_or_none()

    @classmethod
    async def add_one(cls, db: AsyncSession, **values):
        stmt = insert(cls.model).values(**values).returning(cls.model)
        res = await db.execute(stmt)

        return res.scalars().all()

    @classmethod
    async def update_one(cls, db: AsyncSession, filters: dict, **values):
        stmt = (
            update(cls.model)
            .filter(
                text(
                    " AND ".join(f"{key} = '{value}'" for key, value in filters.items())
                )
            )
            .values(**values)
            .returning(cls.model)
        )
        res = await db.execute(stmt)

        return res.scalars().one()

    @classmethod
    async def delete_one(cls, db: AsyncSession, **filter_by):
        stmt = delete(cls.model).filter_by(**filter_by)
        res = await db.execute(stmt)

        return res
