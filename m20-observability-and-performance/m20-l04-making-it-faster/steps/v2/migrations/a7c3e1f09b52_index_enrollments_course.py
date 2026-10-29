"""index enrollments by course

Revision ID: a7c3e1f09b52
Revises: d1a467cf69aa
Create Date: 2026-10-27 21:30:00

"""
from alembic import op

revision = "a7c3e1f09b52"
down_revision = "d1a467cf69aa"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "enrollments_course_id_idx", "enrollments", ["course_id"]
    )


def downgrade() -> None:
    op.drop_index("enrollments_course_id_idx", "enrollments")
