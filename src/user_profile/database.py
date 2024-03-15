from src.user_profile.models import UserProfileModel
from src.dao import SQLAlchemyDAO


class UserDAO(SQLAlchemyDAO):
    model = UserProfileModel