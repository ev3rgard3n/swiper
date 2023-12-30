from sqlalchemy import select, insert, delete, update

from src.database import async_session_maker
from src.interfaces import AbstactDAO


class SQLAlchemyDAO(AbstactDAO):
    model = None

    async def find_all(self,  **filter_by):
        async with async_session_maker() as session:

            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)

            return res.all()

    async def find_one_or_none(self, **filter_by):
        async with async_session_maker() as session:

            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)

            return res.scalar_one_or_none()

    async def add_one(self, **values):
        async with async_session_maker() as session:

            stmt = insert(self.model).values(**values).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()

            return res.scalar_one()

    async def update_one():
        pass

    async def delete_one():
        pass
