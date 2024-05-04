from loguru import logger
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.user_profile.schemes import UpdateModel, UserProfileModel
from src.user_profile.services import DatabaseManager
from src.database import get_async_session as asession
from src.auth.schemes import RequestToResponse, ServerResponse




router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/user_profile/", response_model=UserProfileModel)
async def get_user_profile(
    user_id: str,
    db: AsyncSession = Depends(asession)
):

    db_manager = DatabaseManager(db)
    user_manager = db_manager.userCRUD

    user_data = await user_manager.get_user_profile(user_id=user_id)

    return user_data


@router.patch("/update/user_profile/")
async def get_user_profile(
    user_id : str,
    user_data: UpdateModel,
    db: AsyncSession = Depends(asession)
) :

    db_manager = DatabaseManager(db)
    user_manager = db_manager.userCRUD

    user_data = await user_manager.update_user_profile(user_id=user_id, user_data=user_data)

    await db_manager.commit()
    return user_data