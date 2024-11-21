"""change params email&password

Revision ID: d961d5a897c7
Revises: ec2648c45289
Create Date: 2024-09-25 18:54:14.561150

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa


revision: str = "d961d5a897c7"
down_revision: Union[str, None] = "ec2648c45289"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])
    op.create_unique_constraint(None, "users", ["hashed_password"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
    op.drop_constraint(None, "users", type_="unique")
