import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, text, Column, event
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base
from src.user_profile.models import UserProfileModel


is_bool_params = Annotated[bool, mapped_column(nullable=False, default=False)]
uniq_null_params = Annotated[str, mapped_column(nullable=False, unique=True)]


class AuthModels(Base):
    __tablename__ = "Auth"

    id :Mapped[uuid.UUID] = mapped_column(
        UUID, 
        primary_key=True,
        nullable=False, 
        unique=True,
        server_default=text("gen_random_uuid()")
    )

    login: Mapped[uniq_null_params]
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[uniq_null_params]

    is_delete: Mapped[is_bool_params]
    is_superuser: Mapped[is_bool_params]
    is_verified_email: Mapped[is_bool_params]

    is_verified: Mapped[bool] = mapped_column(
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    deactivate_at: Mapped[datetime | None]


class ResetPasswordModel(Base):
    __tablename__ = "ResetPassword"

    id :Mapped[uuid.UUID] = mapped_column(
        UUID, 
        primary_key=True,
        unique=True,
    )
    email: Mapped[uniq_null_params]
    reset_code: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )