"""Add seed data

Revision ID: 18da25a1d49f
Revises: 085b4e9c9abc
Create Date: 2024-12-07 02:10:44.043554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18da25a1d49f'
down_revision: Union[str, None] = '085b4e9c9abc'
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

    # === Seed data Programs ===
    op.bulk_insert(
        sa.table(
            'programs',
            sa.Column('id', sa.Integer),
            sa.Column('title', sa.String),
            sa.Column('description', sa.Text),
        ),
        [
            {"title": "Program 1", "description": "Deskripsi Program 1"},
            {"title": "Program 2", "description": "Deskripsi Program 2"},
        ],
    )

    # Seed data untuk tabel lain (Gudang dan Lahan) menggunakan raw SQL
    conn = op.get_bind()
    conn.execute(
        sa.text("""
        INSERT INTO gudang (nama, lokasi)
        VALUES
            ('Gudang Tanggamus', ST_SetSRID(ST_Point(104.7361360716594, -5.429258476955538), 4326)),
            ('Gudang Ulubelu', ST_SetSRID(ST_Point(104.55891666666667, -5.309888888888889), 4326));
        """)
    )

    conn.execute(
        sa.text("""
        INSERT INTO lahan (nama, area)
        VALUES
            (
                'Lahan Tanggamus',
                ST_SetSRID(
                    ST_Polygon(
                        '((104.7680361135901 -5.437179125887677, 104.7683950686601 -5.449472128968384, 104.7711599630123 -5.455660144705754, 104.7772876335648 -5.456818090727343, 104.7680361135901 -5.437179125887677))'
                    ),
                    4326
                )
            ),
            (
                'Lahan Liwa',
                ST_SetSRID(
                    ST_Polygon(
                        '((104.1233958963398 -5.055201853881433, 104.125026690811 -5.053709286101618, 104.1253000322696 -5.052366092372457, 104.1233958963398 -5.055201853881433))'
                    ),
                    4326
                )
            );
        """)
    )


def downgrade() -> None:
    pass
