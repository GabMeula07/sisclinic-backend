"""empty message

Revision ID: bed211e5a434
Revises: f1c73afe70ce
Create Date: 2025-01-25 15:38:03.696999

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bed211e5a434'
down_revision: Union[str, None] = 'f1c73afe70ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule', sa.Column('scheduler_id', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'schedule', ['scheduler_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'schedule', type_='unique')
    op.drop_column('schedule', 'scheduler_id')
    # ### end Alembic commands ###
