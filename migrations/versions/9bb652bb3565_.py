"""empty message

Revision ID: 9bb652bb3565
Revises: cac75fcf46c7
Create Date: 2025-01-05 13:46:30.512133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9bb652bb3565'
down_revision: Union[str, None] = 'cac75fcf46c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_adm', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('professional_record',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('birth', sa.Date(), nullable=False),
    sa.Column('cpf', sa.String(), nullable=False),
    sa.Column('occupation', sa.String(), nullable=False),
    sa.Column('specialization', sa.String(), nullable=False),
    sa.Column('number_record', sa.String(), nullable=False),
    sa.Column('street', sa.String(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('not_number', sa.Boolean(), nullable=True),
    sa.Column('neighborhood', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('cep', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schedule',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_scheduled', sa.Date(), nullable=False),
    sa.Column('time_scheduled', sa.String(), nullable=False),
    sa.Column('room', sa.String(), nullable=False),
    sa.Column('type_scheduled', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('schedule')
    op.drop_table('professional_record')
    op.drop_table('user')
    # ### end Alembic commands ###
