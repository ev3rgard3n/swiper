from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.engine.row import Row as sqlalchemyRow
from jose import JWTError, jwt
from fastapi import Response
from loguru import logger


from src.auth.scheme import AuthRegistration, AuthLogin, Token
from src.auth.config import ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from src.auth.database import AuthDAO
from src.auth import exceptions
from src.auth.utils import *


class AuthService:
    def __init__(self, db: AuthDAO) -> None:
        self.db: AuthDAO = db

    async def get_user_data(self, login: str):
        logger.info("Запрос user_data")
        user_data = await self.db.get_user_data(login=login)
        return user_data[0]

    async def get_hashed_password(self, login: str) -> str:
        hashed_password = await self.db.find_one_or_none(login=login)
        return hashed_password.hashed_password

    async def create_user(self, *, user_data: AuthRegistration) -> str:
        login = user_data.login
        email = user_data.email
        hashed_password = await hashing_password(user_data.password)
        data = await self.db.add_one(login=login, hashed_password=hashed_password, email=email)
        return data

    async def validate_login(self, login: str) -> (bool, int):
        if not await self.db.find_one_or_none(login=login):
            raise exceptions.InvalidUserLogin
        return True

    @staticmethod
    async def validate_password(password: str, hashed_password: str) -> bool:
        if not await verify_password(password, hashed_password):
            raise exceptions.InvalidUserPassword
        return True

    async def user_authorization(self, *, user_data: AuthLogin) -> sqlalchemyRow:
        login = user_data.login
        password = user_data.password

        await self.validate_login(login)

        hashed_password = await self.get_hashed_password(login)

        await self.validate_password(password, hashed_password)
        logger.info("Пользователь прошел проверку пароля")

        user_data = await self.get_user_data(login)
        return user_data


class TokenCRUD:

    @classmethod
    async def create_tokens(cls, data: sqlalchemyRow, response: Response):
        logger.debug("Создаю токены")

        access_token = await cls._create_access_token(data.login)
        refresh_token = await cls._create_refresh_token(data.id)

        await cls._set_token_in_cookie(response=response, access_token=access_token, refresh_token=refresh_token)
        return Token(access_token=access_token, refresh_token=refresh_token)

    @classmethod
    async def _create_access_token(cls, data: str):
        logger.info("Создаю access_token")

        to_encode = {"sub": data}
        expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

        to_encode.update(exp=expire)
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encode_jwt

    @classmethod
    async def _create_refresh_token(cls, data: str):
        logger.info("Создаю refresh_token")

        to_encode = {"sub": str(data)}
        expire = datetime.utcnow() + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))

        to_encode.update(exp=expire)
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encode_jwt

    @classmethod
    async def _set_token_in_cookie(cls, response: Response, access_token: str, refresh_token: str):
        logger.info("Установка куки")

        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES,
            httponly=True
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60,
            httponly=True
        )
