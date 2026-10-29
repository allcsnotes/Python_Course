"""enrollment timestamps, amount and refunds

Revision ID: a7c3e91d5b20
Revises: d1a467cf69aa
Create Date: 2026-10-28 09:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "a7c3e91d5b20"
down_revision: Union[str, Sequence[str], None] = "d1a467cf69aa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("enrollments", sa.Column("enrolled_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False))
    op.add_column("enrollments", sa.Column("amount", sa.Integer(), server_default="0", nullable=False))
    op.add_column("enrollments", sa.Column("refunded_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("enrollments", "refunded_at")
    op.drop_column("enrollments", "amount")
    op.drop_column("enrollments", "enrolled_at")
