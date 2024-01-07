from fastapi import HTTPException


class InvalidUserRegistrationLogin(HTTPException):
    """Пользователь с таким логином существует"""

    def __init__(self) -> None:
        super().__init__(status_code=401, detail="InvalidUserRegistrationLogin")


class InvalidUserRegistrationEmail(HTTPException):
    """Пользователь с такой почтой существует"""

    def __init__(self) -> None:
        super().__init__(status_code=401, detail="InvalidUserRegistrationEmail")


class InvalidUserLogin(HTTPException):
    """Пользователь с таким логином не существует"""

    def __init__(self) -> None:
        super().__init__(status_code=401, detail="InvalidUserLogin")


class InvalidUserPassword(HTTPException):
    """Пользователь указал не верный пароль"""

    def __init__(self) -> None:
        super().__init__(status_code=401, detail="InvalidUserPassword")


class InvalidUserDoesNotExist(HTTPException):
    """Пользователь не существует"""

    def __init__(self) -> None:
        super().__init__(status_code=401, detail="InvalidUserDoesNotExist")
        
class InvalidResetCode(HTTPException):
    """Неверный код или срок действия кода истек"""

    def __init__(self) -> None:
        super().__init__(status_code=401, detail="InvalidResetCode")
