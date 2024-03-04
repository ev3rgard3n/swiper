"""empty message

Revision ID: 550aab7c677f
Revises: e5565ef40453
Create Date: 2024-01-07 17:19:54.224260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '550aab7c677f'
down_revision: Union[str, None] = 'e5565ef40453'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ResetPassword', sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ResetPassword', 'created_at')
    # ### end Alembic commands ###