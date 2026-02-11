"""delete is_admin and add None property

Revision ID: d92e2892dbeb
Revises: b0591bb37bfd
Create Date: 2026-02-11 16:40:49.271543

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d92e2892dbeb"
down_revision: Union[str, Sequence[str], None] = "b0591bb37bfd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("expenses", "description", existing_type=sa.VARCHAR(), nullable=True)
    op.drop_column("users", "is_admin")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "is_admin",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.alter_column("expenses", "description", existing_type=sa.VARCHAR(), nullable=False)
