from pydantic import BaseModel, UUID4, validate_arguments


class UpdateModel(BaseModel):
    username: str | None = None
    profile_bio: str | None = None
    profile_photo: str | None = None

    @validate_arguments
    def __init__(self, **data):
        super().__init__(**data)

    class Config:
        validate_assignment = True
        exclude_none = True

class UserProfileModel(BaseModel):
    user_id: UUID4
    external_id: UUID4
    username: str
    profile_bio: str | None
    profile_photo: str | None