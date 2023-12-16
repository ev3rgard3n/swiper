from fastapi import APIRouter, Depends

from src.auth.service import *
from src.auth.scheme import AuthRegistration
from src.auth.database import AuthDAO


router = APIRouter(
    prefix="/auth", 
    tags=["Auth"]
)


@router.post("/registration/")
async def registration(user_data: AuthRegistration): 
    db = AuthDAO()

    return await create_user(user_data=user_data, db=db)