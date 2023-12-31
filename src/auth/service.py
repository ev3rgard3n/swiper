from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, Response, BackgroundTasks
from sqlalchemy.engine.row import Row as sqlalchemyRow
from jose import JWTError, jwt
from loguru import logger


from src.auth.scheme import AuthRegistration, AuthLogin, Token
from src.auth.config import (
    ALGORITHM,
    SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from src.auth.database import AuthDAO
from src.auth import exceptions
from src.auth.utils import *


class AuthService:
    def __init__(self, db: AuthDAO) -> None:
        self.db: AuthDAO = db

    async def get_user_data(self, **user_data):
        try:
            logger.info("Запрос user_data")
            user_data = await self.db.get_user_data(**user_data)
            return user_data[0]
        except IndexError:
            raise exceptions.InvalidUserDoesNotExist

    async def get_hashed_password(self, login: str) -> str:
        hashed_password = await self.db.find_one_or_none(login=login)
        return hashed_password.hashed_password

    async def create_user(self, *, user_data: AuthRegistration) -> str:
        login = user_data.login
        email = user_data.email

        if await validate_data(self.db, login=login) is not None:
            raise exceptions.InvalidUserRegistrationLogin

        if await validate_data(self.db, email=email) is not None:
            raise exceptions.InvalidUserRegistrationEmail

        hashed_password = await hashing_password(user_data.password)
        data = await self.db.add_one(
            login=login, hashed_password=hashed_password, email=email
        )
        return data

    @staticmethod
    async def validate_password(password: str, hashed_password: str) -> bool:
        if not await verify_password(password, hashed_password):
            raise exceptions.InvalidUserPassword
        return True

    async def user_authorization(self, *, user_data: AuthLogin) -> sqlalchemyRow:
        login = user_data.login
        password = user_data.password

        if await validate_data(self.db, login=login) is None:
            raise exceptions.InvalidUserLogin

        hashed_password = await self.get_hashed_password(login)

        await self.validate_password(password, hashed_password)
        logger.info("Пользователь прошел проверку пароля")

        user_data = await self.get_user_data(login=login)
        return user_data

    async def authorization_with_token(self, user_data: dict):
        logger.info("Автризация через токен")

        user_data = await self.get_user_data(login=user_data["user_login"])
        return user_data


class TokenCRUD:
    @classmethod
    async def create_tokens(cls, data: sqlalchemyRow, response: Response):
        logger.debug("Создаю токены")

        access_token = await cls._create_access_token(
            user_login=data.login, is_admin=data.is_superuser
        )
        refresh_token = await cls._create_refresh_token(str(data.id))

        await cls._set_token_in_cookie(
            response=response, access_token=access_token, refresh_token=refresh_token
        )
        return Token(access_token=access_token, refresh_token=refresh_token)

    @classmethod
    async def logout(cls, response: Response):
        logger.info("Запрос на logout")
        await cls._delete_cookie(response=response)
        return {"detail": "Success"}

    @classmethod
    async def _create_access_token(cls, **kwargs):
        logger.info("Создаю access_token")

        to_encode = {
            "iss": "AuthServer",
            "sub": "Auth",
        }
        expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

        to_encode.update(exp=expire, **kwargs)
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
        return encode_jwt

    @classmethod
    async def _create_refresh_token(cls, data: str):
        logger.info("Создаю refresh_token")

        to_encode = to_encode = {
            "iss": "AuthServer",
            "sub": "Auth",
        }
        expire = datetime.utcnow() + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))

        to_encode.update(exp=expire, user_id=data)
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
        return encode_jwt

    @staticmethod
    async def _decode_token(token: str) -> dict:
        logger.info("Декодирую jwt")

        decode_jwt = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return decode_jwt

    @classmethod
    async def _set_token_in_cookie(
        cls, response: Response, access_token: str, refresh_token: str
    ) -> None:
        logger.info("Установка куки")

        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES,
            httponly=True,
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60,
            httponly=True,
        )

    @classmethod
    async def _delete_cookie(cls, response: Response) -> None:
        logger.info("Удаление куков")
        
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.delete_cookie("session")
