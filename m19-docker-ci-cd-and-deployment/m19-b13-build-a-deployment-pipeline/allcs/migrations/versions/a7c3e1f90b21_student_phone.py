"""student phone

Revision ID: a7c3e1f90b21
Revises: d1a467cf69aa
Create Date: 2026-10-27 18:20:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a7c3e1f90b21"
down_revision: str | Sequence[str] | None = "d1a467cf69aa"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "students",
        sa.Column(
            "phone",
            sa.String(20),
            nullable=False,
            server_default="",
        ),
    )


def downgrade() -> None:
    op.drop_column("students", "phone")
