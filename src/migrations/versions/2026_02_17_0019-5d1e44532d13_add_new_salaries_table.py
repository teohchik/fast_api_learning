"""add new Salaries table

Revision ID: 5d1e44532d13
Revises: 4a38bae89c64
Create Date: 2026-02-17 00:19:43.622469

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5d1e44532d13"
down_revision: Union[str, Sequence[str], None] = "4a38bae89c64"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "salaries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_salaries_user_id"), "salaries", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_salaries_user_id"), table_name="salaries")
    op.drop_table("salaries")
