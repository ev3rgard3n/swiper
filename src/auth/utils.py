import string
import random
import bcrypt
from random import sample

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.database import AuthDAO


async def hashing_password(password: str) -> str:
    logger.info("Хеширование пароля")
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


async def verify_password(password: str, hashed_password: str) -> bool:
    logger.info("Проверка пароля")
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


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


async def generate_random_numbers(length=6) -> str:
    return "".join(sample("0123456789", length))


# def randomword():
#    letters = string.ascii_lowercase
#    letters_number = string.digits
   
#    return f"user_name{''.join(random.choice(letters + letters_number) for i in range(20))}"