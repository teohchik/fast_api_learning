"""User, add currency field

Revision ID: a0f30618286b
Revises: 45252fa6d385
Create Date: 2026-02-14 16:09:14.237019

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a0f30618286b"
down_revision: Union[str, Sequence[str], None] = "45252fa6d385"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column("currency", sa.String(length=10), server_default="€", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("users", "currency")
