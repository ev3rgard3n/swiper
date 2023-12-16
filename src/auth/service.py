from datetime import datetime, timedelta
from typing import Annotated

from loguru import logger
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt


from src.auth.scheme import AuthRegistration
from src.auth.database import AuthDAO
from src.auth.utils import *



SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def create_user(*, user_data: AuthRegistration, db: AuthDAO):
    login = user_data.login
    email = user_data.email
    hashed_password = await get_hashing_password(user_data.password)
    
    logger.debug(f"login: {login}| email: {email} | hashed_password: {hashed_password}")

    return await db.add_one(login=login, hashed_password=hashed_password, email=email)

