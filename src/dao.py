from abc import ABC, abstractmethod

from sqlalchemy import select, insert, delete, update
# from sqlalchemy.orm import 

from src.database import async_session_maker


class AbstactDAO(ABC):
    @abstractmethod
    async def find_all():
        raise NotImplementedError

    @abstractmethod
    async def find_one():
        raise NotImplementedError

    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        raise NotImplementedError

    @abstractmethod
    async def delete_one():
        raise NotImplementedError


class SQLAlchemyDAO(AbstactDAO):
    model = None

    async def find_all(self,  **filter_by):
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            return res.all()

    async def find_one():
        pass

    async def add_one(self, **values):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**values).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return  res.scalar_one()

    async def update_one():
         pass

    async def delete_one():
        pass
