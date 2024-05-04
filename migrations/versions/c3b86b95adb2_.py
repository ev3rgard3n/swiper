"""empty message

Revision ID: c3b86b95adb2
Revises: a9a0754089ee
Create Date: 2024-04-04 21:00:26.514636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3b86b95adb2'
down_revision: Union[str, None] = 'a9a0754089ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'Auth', ['id'])
    op.create_unique_constraint(None, 'ResetPassword', ['id'])
    op.drop_constraint('UserProfile_profile_photo_key', 'UserProfile', type_='unique')
    op.create_unique_constraint(None, 'UserProfile', ['external_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'UserProfile', type_='unique')
    op.create_unique_constraint('UserProfile_profile_photo_key', 'UserProfile', ['profile_photo'])
    op.drop_constraint(None, 'ResetPassword', type_='unique')
    op.drop_constraint(None, 'Auth', type_='unique')
    # ### end Alembic commands ###