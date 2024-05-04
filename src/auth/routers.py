from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, Response
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from src.auth.schemes import (
    AuthRegistration,
    AuthLogin,
    AuthorizedUser,
    RequestToResponse,
    ResetPassword,
    ServerResponse,
    Token,
)
from src.auth.services import DatabaseManager
from src.auth.utils import convert_user_data_to_dict
from src.auth.email_service import send_confirm_email, send_confirm_reset_password
from src.database import get_async_session as asession


router = APIRouter(prefix="/auth", tags=["Auth"])
cookie_type = Annotated[str | None, Cookie()]


@router.post("/registration/", status_code=201)
async def registration(
    user_data: AuthRegistration,
    db: AsyncSession = Depends(asession),
):
    try:

        db_manager = DatabaseManager(db)
        auth_service = db_manager.auth_service
        user_profile = db_manager.user_profile

        data = await auth_service.create_user(user_data=user_data)
        _ = await user_profile.create_base_user_profile(user_data=data)
        await db_manager.commit()

        send_confirm_email.delay(user_id=data.id, email_receiver=data.email)

        return data

    except Exception as error:
        logger.opt(exception=error).critical("Error in registraion")
        await db_manager.rollback()
        return error


@router.post("/login/")
async def login(
    response: Response,
    user_data: AuthLogin,
    db: AsyncSession = Depends(asession),
) -> AuthorizedUser:
    db_manager = DatabaseManager(db)
    auth_service = db_manager.auth_service
    token_crud = db_manager.token_crud

    data = await auth_service.user_authorization(user_data=user_data)
    tokens = await token_crud.create_tokens(data=data, response=response)
    data = await convert_user_data_to_dict(user_data=data)

    return AuthorizedUser(user_data=data, tokens=tokens)


@router.post("/login/with_token/")
async def login_with_token(
    response: Response,
    access_token: cookie_type = None,
    db: AsyncSession = Depends(asession),
) -> AuthorizedUser:

    db_manager = DatabaseManager(db)
    auth_service = db_manager.auth_service
    token_crud = db_manager.token_crud

    user_data_jwt = await token_crud._decode_token(token=access_token)
    user_data = await auth_service.authorization_with_token(user_data=user_data_jwt)
    tokens = await token_crud.create_tokens(data=user_data, response=response)
    user_data = await convert_user_data_to_dict(user_data=user_data)

    return AuthorizedUser(user_data=user_data, tokens=tokens)


@router.patch("/refresh_token/")
async def refresh_token(
    response: Response,
    refresh_token: cookie_type = None,
    db: AsyncSession = Depends(asession),
) -> Token:

    db_manager = DatabaseManager(db)
    auth_service = db_manager.auth_service
    token_crud = db_manager.token_crud

    user_data_jwt = await token_crud._decode_token(token=refresh_token)
    user_data = await auth_service.get_user_data(id=user_data_jwt["user_id"])
    tokens = await token_crud.create_tokens(data=user_data, response=response)

    return tokens


@router.post("/logout/", status_code=205)
async def logout(
    response: Response, db: AsyncSession = Depends(asession)
) -> RequestToResponse:

    db_manager = DatabaseManager(db)
    token_crud = db_manager.token_crud

    await token_crud.logout(response=response)

    return RequestToResponse(detail=ServerResponse(msg="Logout success"))


@router.delete("/deactivate/account")
async def deactivate_account(
    response: Response,
    access_token: cookie_type = None,
    db: AsyncSession = Depends(asession),
) -> RequestToResponse:

    db_manager = DatabaseManager(db)
    auth_service = db_manager.auth_service
    token_crud = db_manager.token_crud

    user_data = await token_crud._decode_token(token=access_token)
    await auth_service.deactivate_account(user_data=user_data)
    await logout(response=response)

    return RequestToResponse(detail=ServerResponse(msg="Account is deactivated"))


@router.get("/verify_email/")
async def verify_email(
    user_id: str, db: AsyncSession = Depends(asession)
) -> RequestToResponse:

    db_manager = DatabaseManager(db)
    auth_service = db_manager.auth_service

    await auth_service.verify_email(user_id=user_id)

    return RequestToResponse(detail=ServerResponse(msg="The email is confirmed"))


@router.post("/reset_password/request/")
async def request_reset_password(
    email: EmailStr,
    db: AsyncSession = Depends(asession),
) -> RequestToResponse:
    try:

        db_manager = DatabaseManager(db)
        auth_service = db_manager.auth_service
        reset_password = db_manager.reset_password

        user_data = await auth_service.get_user_data(email=email)

        reset_code = await reset_password.request_reset_password(
            id=user_data.id, email=email
        )

        await db_manager.commit()
        send_confirm_reset_password.delay(reset_code=reset_code, email_receiver=email)
        return RequestToResponse(
            detail=ServerResponse(msg="A password reset code has been sent")
        )
    except Exception as error:
        logger.opt(exception=error).critical("Error in request reset password")
        await db_manager.rollback()
        return error


@router.post("/reset_password/confirm/")
async def confirm_reset_password(
    email: EmailStr,
    code: str,
    db: AsyncSession = Depends(asession),
) -> RequestToResponse:
    try:
        db_manager = DatabaseManager(db)
        reset_password = db_manager.reset_password

        await reset_password.confirm_reset_password(email=email, reset_code=code)

        await db_manager.commit()
        return RequestToResponse(
            detail=ServerResponse(msg="The entered code is correct")
        )

    except Exception as error:
        logger.opt(exception=error).critical("Error in reset_password (confirm)")
        await db_manager.rollback()
        return error


@router.patch("/reset_password/refresh_code/")
async def refresh_reset_password(
    email: EmailStr,
    db: AsyncSession = Depends(asession),
) -> RequestToResponse:
    try:
        db_manager = DatabaseManager(db)
        reset_password = db_manager.reset_password

        reset_code = await reset_password._refresh_reset_code(email=email)
        await db_manager.commit()

        send_confirm_reset_password.delay(reset_code=reset_code, email_receiver=email)
        return RequestToResponse(detail=ServerResponse(msg="The code has been updated"))

    except Exception as error:
        logger.opt(exception=error).critical("Error in reset_password (confirm)")
        await db_manager.rollback()
        return error


@router.patch("/reset_password/")
async def request_reset_password(
    user_data: ResetPassword,
    db: AsyncSession = Depends(asession),
) -> RequestToResponse:
    try:
        db_manager = DatabaseManager(db)
        auth_service = db_manager.auth_service
        reset_password = db_manager.reset_password

        await reset_password.confirm_reset_password(
            email=user_data.email, reset_code=user_data.code
        )
        await auth_service.change_password(
            email=user_data.email, password=user_data.password
        )

        await reset_password._delete_entry(user_data=user_data)
        await db_manager.commit()
        return RequestToResponse(detail=ServerResponse(msg="A password is reset"))

    except Exception as error:
        logger.opt(exception=error).critical("Error in reset_password (confirm)")
        await db_manager.rollback()
        return error
