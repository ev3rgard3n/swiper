from fastapi import HTTPException


class InvalidUserLogin(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="InvalidUserLogin")


class InvalidUserPassword(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="InvalidUserPassword")