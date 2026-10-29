"""student password hash

Revision ID: 24530b3dbf92
Revises: 6d1d3956ce21
Create Date: 2026-10-27 13:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '24530b3dbf92'
down_revision: Union[str, Sequence[str], None] = '6d1d3956ce21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('students', sa.Column('password_hash', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('students', 'password_hash')
