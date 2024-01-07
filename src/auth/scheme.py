from datetime import datetime
from typing import Any
from pydantic import BaseModel, EmailStr, UUID4


class AuthLogin(BaseModel):
    login: str
    password: str


class AuthRegistration(AuthLogin):
    email: EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str


class UserData(BaseModel):
    id: UUID4
    login: str
    email: EmailStr
    is_delete: bool
    is_superuser: bool
    is_verified_email: bool
    is_verified: bool
    created_at: datetime


class AuthorizedUser(BaseModel):
    user_data: UserData
    tokens: Token


class ServerResponse(BaseModel):
    msg: str
    code: int = 0
    data: dict | None = None


class RequestToResponse(BaseModel):
    detail: ServerResponse


class ResetPassword(BaseModel):
    email: EmailStr
    password: str
    code: str
