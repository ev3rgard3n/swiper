from typing import Optional
from pydantic import BaseModel, EmailStr, SecretStr


class AuthRegistration(BaseModel):
    login: str
    # password: SecretStr
    password: str
    email:  EmailStr