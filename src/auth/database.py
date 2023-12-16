from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import AuthModels
from src.dao import SQLAlchemyDAO


class AuthDAO(SQLAlchemyDAO):
    model = AuthModels