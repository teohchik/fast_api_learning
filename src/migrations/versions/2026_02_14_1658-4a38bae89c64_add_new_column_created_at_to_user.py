"""add new column created_at to User

Revision ID: 4a38bae89c64
Revises: a0f30618286b
Create Date: 2026-02-14 16:58:27.183584

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4a38bae89c64"
down_revision: Union[str, Sequence[str], None] = "a0f30618286b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "created_at")
