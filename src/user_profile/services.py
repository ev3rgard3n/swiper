from sqlalchemy.ext.asyncio import AsyncSession

from src.user_profile.database import UserDAO


class UserCRUD:
    def __init__(self, db) -> None:
        self.db = db

    async def get_user_profile(self, **filter_by) :
        return await UserDAO.find_one_or_none(self.db, **filter_by)


class DatabaseManager:
    def __init__(self, db: AsyncSession) -> None:
        self.userCRUD = UserCRUD(db)


    async def commit(self):
        await self.db.commit()
        # await self.db.close()