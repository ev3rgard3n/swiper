from datetime import datetime, timedelta

from fastapi import Response

from sqlalchemy.engine.row import Row as sqlalchemyRow
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt
from jose.exceptions import JWSError, JWTError

from loguru import logger


from src.auth.schemes import AuthRegistration, AuthLogin, Token
from src.auth.config import (
    ALGORITHM,
    SECRET_KEY,
    ACCESST_EXPIRE_MINUTES,
    REFRESHT_EXPIRE_DAYS,
)
from src.auth.database import AuthDAO, ResetPasswordDAO
from src.auth import exceptions
from src.auth.utils import *


class AuthService:
    def __init__(self, db):
        self.db = db

    async def get_user_data(self, **filter_by) -> sqlalchemyRow:
        try:
            logger.info("Запрос user_data")
            user_data = await AuthDAO.get_user_data(self.db, **filter_by)
            return user_data[0]
        except IndexError:
            raise exceptions.InvalidUserDoesNotExist

    async def get_hashed_password(self, login: str) -> str:
        hashed_password = await AuthDAO.find_one_or_none(self.db, login=login)
        return hashed_password.hashed_password

    async def validate_data(self, **data):
        return await AuthDAO.find_one_or_none(self.db, **data)

    async def create_user(self, *, user_data: AuthRegistration) -> str:
        login = user_data.login
        email = user_data.email

        if await self.validate_data(login=login) is not None:
            raise exceptions.InvalidUserRegistrationLogin

        if await self.validate_data(email=email) is not None:
            raise exceptions.InvalidUserRegistrationEmail

        hashed_password = await hashing_password(user_data.password)
        data = await AuthDAO.add_one(
            self.db, login=login, hashed_password=hashed_password, email=email
        )

        await self.db.commit()
        return data[0]

    @staticmethod
    async def validate_password(password: str, hashed_password: str) -> bool:
        if not await verify_password(password, hashed_password):
            raise exceptions.InvalidUserPassword
        return True

    async def change_password(self, email: str, password: str) -> None:
        logger.info("Запрос на изменение пароля")

        hashed_password = await hashing_password(password)
        filters = {"email": email}

        await AuthDAO.update_one(self.db, filters, hashed_password=hashed_password)
        await self.db.commit()

    async def user_authorization(self, *, user_data: AuthLogin) -> sqlalchemyRow:
        login = user_data.login
        password = user_data.password

        if await self.validate_data(login=login) is None:
            raise exceptions.InvalidUserLogin

        hashed_password = await self.get_hashed_password(login)

        await self.validate_password(password, hashed_password)
        user_data = await self.get_user_data(login=login)

        return user_data

    async def authorization_with_token(self, user_data: dict) -> sqlalchemyRow:
        logger.info("Автризация через токен")

        login = user_data["user_login"]
        user_data = await self.get_user_data(login=login)

        return user_data

    async def verify_email(self, user_id: str) -> None:
        logger.debug(f"Верефикация почты пользователя: {user_id}")

        filters = {"id": user_id}
        await AuthDAO.update_one(self.db, filters, is_verified_email=True)
        await self.db.commit()

    async def deactivate_account(self, user_data: dict) -> None:
        logger.info("Деактивация аккаунта")

        login = user_data["user_login"]

        filters = {"login": login}
        await AuthDAO.update_one(
            self.db, filters, is_delete=True, deactivate_at=datetime.utcnow()
        )
        await self.db.commit()


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
    async def logout(cls, response: Response) -> None:
        logger.info("Запрос на logout")
        await cls._delete_cookie(response=response)

    @classmethod
    async def _create_access_token(cls, **kwargs) -> str:
        """ **kwargs:  user_login и is_admin """
        try:

            logger.info("Создаю access_token")

            to_encode = {
                "iss": "AuthServer",
                "sub": "Auth",
            }
            expire = datetime.utcnow() + timedelta(minutes=int(ACCESST_EXPIRE_MINUTES))

            to_encode.update(exp=expire, **kwargs)
            encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
            return encode_jwt

        except (JWTError, JWSError) as e:
            logger.opt(exception=e).critical("Error in create access token")
            raise exceptions.ExceptionInTheCreationToken

    @classmethod
    async def _create_refresh_token(cls, user_id: str) -> str:
        try:
            logger.info("Создаю refresh_token")

            to_encode = to_encode = {
                "iss": "AuthServer",
                "sub": "Auth",
            }
            expire = datetime.utcnow() + timedelta(days=int(REFRESHT_EXPIRE_DAYS))

            to_encode.update(exp=expire, user_id=user_id)
            encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

            return encode_jwt
        except (JWTError, JWSError) as e:
            logger.opt(exception=e).critical("Error in create access token")
            raise exceptions.ExceptionInTheCreationToken

    @staticmethod
    async def _decode_token(token: str) -> dict:
        try:
            logger.info("Декодирую jwt")

            decode_jwt = jwt.decode(token, SECRET_KEY, ALGORITHM)
            return decode_jwt
        except (JWTError, JWSError) as e:
            logger.opt(exception=e).critical("Error in decode token")
            raise exceptions.ExceptionInTheDecodeToken

    @classmethod
    async def _set_token_in_cookie(
        cls, response: Response, access_token: str, refresh_token: str
    ) -> None:
        logger.info("Установка куки")

        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=ACCESST_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=True
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=REFRESHT_EXPIRE_DAYS * 60 * 24 * 30,
            httponly=True,
            secure=True
        )

    @classmethod
    async def _delete_cookie(cls, response: Response) -> None:
        logger.info("Удаление куков")

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.delete_cookie("session")


class ResetPasswordCRUD:
    def __init__(self, db) -> None:
        self.db = db

    async def request_reset_password(self, id: str, email: str) -> str:
        logger.info("Запрос на сброс пароля")

        reset_code = await self.__create_reset_code()
        await ResetPasswordDAO.add_one(
            self.db, id=id, reset_code=reset_code, email=email
        )
        await self.db.commit()
        return reset_code

    async def confirm_reset_password(self, email: str, reset_code: str) -> None:
        logger.info("Проверка введеного кода")

        data = await self._get_data_from_db(email=email)

        if data.created_at + timedelta(minutes=30) < datetime.utcnow():
            logger.error("Время дейсвия кода истекло")
            raise exceptions.InvalidResetCode

        if reset_code != data.reset_code:
            logger.error("Не верный код")
            raise exceptions.InvalidResetCode

    async def _get_data_from_db(self, **filter_by) -> str:
        return await ResetPasswordDAO.find_one_or_none(self.db, **filter_by)

    async def __create_reset_code(self) -> str:
        return await generate_random_numbers()

    async def _refresh_reset_code(self, email: str) -> str:
        logger.info("Обновление кода")

        reset_code = await self.__create_reset_code()
        filters = {"email": email}

        await ResetPasswordDAO.update_one(
            self.db, filters, reset_code=reset_code, created_at=datetime.utcnow()
        )
        await self.db.commit()

        return reset_code

    async def _delete_entry(self, user_data) -> None:
        email = user_data.email
        code = user_data.code
        await ResetPasswordDAO.delete_one(self.db, email=email, reset_code=code)
        await self.db.commit()


class DatabaseManager:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.reset_password = ResetPasswordCRUD(db)
        self.auth_service = AuthService(db)
        self.token_crud = TokenCRUD()

    async def commit(self):
        await self.db.commit()
