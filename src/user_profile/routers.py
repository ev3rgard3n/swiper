from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemes import RequestToResponse, ServerResponse
from src.database import get_async_session as asession
from src.user_profile.services import DatabaseManager

from loguru import logger


router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/user_profile/")
async def get_user_profile(
    user_id: str ,
    db: AsyncSession = Depends(asession),
):

    db_manager = DatabaseManager(db)
    user_manager = db_manager.userCRUD

    user_data = await user_manager.get_user_profile(user_id=user_id)

    return user_data


# @router.update("/update/user_profile/")
# async def get_user_profile(
#     db: AsyncSession = Depends(asession),
# ) -> RequestToResponse:

#     db_manager = DatabaseManager(db)
#     auth_service = db_manager.auth_service

#     user_data = await auth_service.create_user(user_data=user_data)


#     return RequestToResponse(detail=ServerResponse())