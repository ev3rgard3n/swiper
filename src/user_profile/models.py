import uuid
from sqlalchemy import ForeignKey, String, text, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UserProfileModel(Base):
    __tablename__ = "UserProfile"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('Auth.id', ondelete="CASCADE"),
        nullable=False,
    )

    external_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        nullable=False,
        unique=True,
        server_default=text("gen_random_uuid()")
    )

    username: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
    )
    profile_bio: Mapped[str] = mapped_column(
        String(120), nullable=True, unique=False)

    profile_photo: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
        server_default="image/user.png"
    )
