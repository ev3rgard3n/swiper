from fastapi import APIRouter, Depends, Response
from loguru import logger

from src.auth.scheme import AuthRegistration, AuthLogin, AuthorizedUser, Token
from src.auth.service import AuthService, TokenCRUD
from src.auth.utils import convert_user_data_to_dict
from src.auth.database import AuthDAO


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/registration/", status_code=201)
async def registration(user_data: AuthRegistration):
    db = AuthDAO()
    auth_service = AuthService(db)
    data = await auth_service.create_user(user_data=user_data)

    return {"msg": "ok", "code": 0, "data": data}


@router.post("/login/")
async def login(response: Response, user_data: AuthLogin) -> AuthorizedUser:
    db = AuthDAO()
    auth_service = AuthService(db)
    token_crud = TokenCRUD()

    data = await auth_service.user_authorization(user_data=user_data)
    tokens = await token_crud.create_tokens(data=data, response=response)
    data = await convert_user_data_to_dict(user_data=data)

    return AuthorizedUser(user_data=data, tokens=tokens)


@router.post("/login/with_token/")
async def login_with_token(response: Response, access_token: str) -> AuthorizedUser:
    db = AuthDAO()
    auth_service = AuthService(db)
    token_crud = TokenCRUD()

    user_data_jwt = await token_crud._decode_token(token=access_token)
    user_data = await auth_service.authorization_with_token(user_data=user_data_jwt)
    tokens = await token_crud.create_tokens(data=user_data, response=response)
    user_data = await convert_user_data_to_dict(user_data=user_data)

    return AuthorizedUser(user_data=user_data, tokens=tokens)


@router.patch("/refresh_token/")
async def login_with_token(response: Response, refresh_token: str) -> Token:
    db = AuthDAO()
    auth_service = AuthService(db)
    token_crud = TokenCRUD()

    user_data_jwt = await token_crud._decode_token(token=refresh_token)
    user_data = await auth_service.get_user_data(id=user_data_jwt["user_id"])
    tokens = await token_crud.create_tokens(data=user_data, response=response)

    return tokens


@router.post("/logout/", status_code=205)
async def logout(response: Response):
    token_crud = TokenCRUD()
    return await token_crud.logout(response=response)
