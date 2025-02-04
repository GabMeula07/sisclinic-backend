"""empty message

Revision ID: cb0b347e0981
Revises: b6fd2ec65b85
Create Date: 2025-01-28 08:44:10.481393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb0b347e0981'
down_revision: Union[str, None] = 'b6fd2ec65b85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('schedule_scheduler_id_key', 'schedule', type_='unique')
    op.drop_column('schedule', 'recurrence_weekday')
    op.drop_column('schedule', 'recurrence_time')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule', sa.Column('recurrence_time', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('schedule', sa.Column('recurrence_weekday', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_unique_constraint('schedule_scheduler_id_key', 'schedule', ['scheduler_id'])
    # ### end Alembic commands ###
