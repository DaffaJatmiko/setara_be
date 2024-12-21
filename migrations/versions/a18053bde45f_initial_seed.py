"""Initial seed

Revision ID: a18053bde45f
Revises: 4571bedc38f1
Create Date: 2024-12-21 00:48:26.398633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a18053bde45f'
down_revision: Union[str, None] = '4571bedc38f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     # === Seed data Users ===
    op.bulk_insert(
        sa.table(
            'users',
            sa.Column('id', sa.Integer),
            sa.Column('username', sa.String),
            sa.Column('email', sa.String),
            sa.Column('full_name', sa.String),
            sa.Column('hashed_password', sa.String),
            sa.Column('is_active', sa.Boolean),
            sa.Column('is_superuser', sa.Boolean),
        ),
        [
            {
                "username": "admin",
                "email": "admin@setara.com",
                "full_name": "Administrator",
                "hashed_password": "$2b$12$Y7tFH3F4coOViHuh5iUGH.3M1hcOxXZtPteg1hfkXE4VLthzmc3Cm",
                "is_active": True,
                "is_superuser": True,
            },
        ],
    )


def downgrade() -> None:
    pass