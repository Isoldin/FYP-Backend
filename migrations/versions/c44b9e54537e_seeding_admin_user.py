"""Seeding admin user

Revision ID: c44b9e54537e
Revises: ed931423e045
Create Date: 2025-01-08 03:49:52.771347

"""
from typing import Sequence, Union
from seed import create_admin, delete_admin

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c44b9e54537e'
down_revision: Union[str, None] = 'ed931423e045'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    create_admin()


def downgrade() -> None:
    delete_admin()
