import bcrypt

from loguru import logger

from src.auth.database import AuthDAO


async def hashing_password(password: str) -> str:
    logger.info("Хеширование пароля")
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


async def verify_password(password: str, hashed_password: str) -> bool:
    logger.info("Проверка пароля")
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


async def validate_data(db: AuthDAO, **data) -> bool:
    return await db.find_one_or_none(**data)


async def convert_user_data_to_dict(user_data) -> dict:
    user_data_dict = {
        "id": user_data.id,
        "login": user_data.login,
        "email": user_data.email,
        "is_delete": user_data.is_delete,
        "is_superuser": user_data.is_superuser,
        "is_verified_email": user_data.is_verified_email,
        "is_verified": user_data.is_verified,
        "created_at": user_data.created_at,
    }
    return user_data_dict
