from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import AuthModels, ResetPasswordModel
from src.dao import SQLAlchemyDAO


class AuthDAO(SQLAlchemyDAO):
    model = AuthModels

    @classmethod
    async def get_user_data(cls, db: AsyncSession, **filter_by):
        stmt = select(
            cls.model.id,
            cls.model.login,
            cls.model.email,
            cls.model.is_delete,
            cls.model.is_superuser,
            cls.model.is_verified_email,
            cls.model.is_verified,
            cls.model.created_at,
        ).filter_by(**filter_by)
        res = await db.execute(stmt)

        return res.all()


class ResetPasswordDAO(SQLAlchemyDAO):
    model = ResetPasswordModel
