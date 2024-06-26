"""empty message

Revision ID: a9a0754089ee
Revises: 
Create Date: 2024-03-21 14:48:56.848438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9a0754089ee'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Auth',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('login', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('is_delete', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('is_verified_email', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('deactivate_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('id'),
        sa.UniqueConstraint('login')
    )
    op.create_table('ResetPassword',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('reset_code', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_table('UserProfile',
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('external_id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('profile_bio', sa.String(length=120), nullable=True),
        sa.Column('profile_photo', sa.String(), server_default='image/user.png', nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['Auth.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('external_id'),
        sa.UniqueConstraint('external_id'),
        sa.UniqueConstraint('profile_photo'),
        sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('UserProfile')
    op.drop_table('ResetPassword')
    op.drop_table('Auth')
    # ### end Alembic commands ###
