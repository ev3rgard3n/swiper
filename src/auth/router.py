from fastapi import APIRouter, Depends, Response
from loguru import logger

from src.auth.scheme import AuthRegistration, AuthLogin, AuthorizedUser
from src.auth.service import AuthService, TokenCRUD
from src.auth.utils import convert_user_data_to_dict
from src.auth.database import AuthDAO


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/registration/")
async def registration(user_data: AuthRegistration):

    db = AuthDAO()
    auth_service = AuthService(db)
    data = await auth_service.create_user(user_data=user_data, db=db)

    return {"msg": "ok", "code": 0, "data": data}


@router.post("/login/")
async def login(response: Response, user_data: AuthLogin) -> AuthorizedUser:
    db = AuthDAO()
    auth_service = AuthService(db)
    token_crud = TokenCRUD()

    data = await auth_service.user_authorization(user_data=user_data)
    tokens = await token_crud.create_tokens(data=data, response=response)
    data = await convert_user_data_to_dict(data)

    return AuthorizedUser(user_data=data, tokens=tokens)
