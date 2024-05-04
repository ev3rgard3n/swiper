from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.user_profile.database import UserDAO
from src.user_profile.schemes import UpdateModel


class UserCRUD:
    def __init__(self, db) -> None:
        self.db = db

    async def get_user_profile(self, **filter_by) :
        return await UserDAO.find_one_or_none(self.db, **filter_by)
    
    async def create_base_user_profile(self, user_data) -> None:
        try:
            user_id = user_data.id
            username = user_data.login
            logger.info(13333)
            await UserDAO.add_one(
                self.db, 
                username=username,
                user_id=user_id,
            )
            logger.info(333333)
        except Exception as e:
            logger.opt(exception=e).error('Error in create_base_user_profile')

    async def update_user_profile(self, user_id:str, user_data: UpdateModel): 
        filter_dict = {"user_id":user_id}
        return await UserDAO.update_one(self.db, filter_dict, user_data)


class DatabaseManager:
    def __init__(self, db: AsyncSession) -> None:
        self.userCRUD = UserCRUD(db)


    async def commit(self):
        await self.db.commit()
