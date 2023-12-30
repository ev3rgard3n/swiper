from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.auth.models import AuthModels
from src.dao import SQLAlchemyDAO
from src.database import async_session_maker


class AuthDAO(SQLAlchemyDAO):
    model = AuthModels

    async def get_user_data(self, **filter_by):
        async with async_session_maker() as session:

            stmt = select(
                self.model.id,
                self.model.login,
                self.model.email,
                self.model.is_delete,
                self.model.is_superuser,
                self.model.is_verified_email,
                self.model.is_verified,
                self.model.created_at,
            ).filter_by(**filter_by)
            res = await session.execute(stmt)

            return res.all()