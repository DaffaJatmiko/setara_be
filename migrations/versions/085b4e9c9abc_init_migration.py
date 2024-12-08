"""init migration

Revision ID: 085b4e9c9abc
Revises: 
Create Date: 2024-12-07 02:03:16.780396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '085b4e9c9abc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    
    # Seed data Users dengan ON CONFLICT
    conn.execute(
        sa.text("""
        INSERT INTO users (id, username, email, full_name, hashed_password, is_active, is_superuser)
        VALUES (1, 'admin', 'admin@setara.com', 'Administrator', 
                '$2b$12$Y7tFH3F4coOViHuh5iUGH.3M1hcOxXZtPteg1hfkXE4VLthzmc3Cm', 
                true, true)
        ON CONFLICT (email) DO NOTHING;
        """)
    )

    # Seed data Programs - Sekarang tanpa ON CONFLICT
    op.bulk_insert(
        sa.table(
            'programs',
            sa.Column('title', sa.String),
            sa.Column('description', sa.Text),
        ),
        [
            {"title": "Program 1", "description": "Deskripsi Program 1"},
            {"title": "Program 2", "description": "Deskripsi Program 2"},
        ],
    )
    
    # Seed data for 'gudang' table using raw SQL
    conn.execute(
        sa.text("""
        INSERT INTO gudang (id, nama, lokasi)
        VALUES
            (1, 'Gudang Tanggamus', ST_SetSRID(ST_Point(104.7361360716594, -5.429258476955538), 4326)),
            (2, 'Gudang Ulubelu', ST_SetSRID(ST_Point(104.55891666666667, -5.309888888888889), 4326));
        """)
    )

    # Seed data for 'lahan' table using raw SQL
    conn.execute(
        sa.text("""
        INSERT INTO lahan (id, nama, area)
        VALUES
            (
                1,
                'Lahan Tanggamus',
                ST_SetSRID(
                    ST_GeomFromText(
                        'POLYGON((104.7680361135901 -5.437179125887677, 104.7683950686601 -5.449472128968384, 104.7711599630123 -5.455660144705754, 104.7772876335648 -5.456818090727343, 104.7680361135901 -5.437179125887677))'
                    ),
                    4326
                )
            ),
            (
                2,
                'Lahan Liwa',
                ST_SetSRID(
                    ST_GeomFromText(
                        'POLYGON((104.1233958963398 -5.055201853881433, 104.125026690811 -5.053709286101618, 104.1253000322696 -5.052366092372457, 104.1233958963398 -5.055201853881433))'
                    ),
                    4326
                )
            );
        """)
    )
def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('full_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=True),
    sa.Column('is_superuser', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    sa.UniqueConstraint('username', name='users_username_key')
    )
    op.create_table('gudang',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nama', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('lokasi', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry', nullable=False, _spatial_index_reflected=True), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='gudang_pkey')
    )
    op.create_index('ix_gudang_id', 'gudang', ['id'], unique=False)
    op.create_index('idx_gudang_lokasi', 'gudang', ['lokasi'], unique=False, postgresql_using='gist')
    op.create_table('programs',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='programs_pkey')
    )
    op.create_index('ix_programs_id', 'programs', ['id'], unique=False)
    op.create_table('lahan',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nama', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('area', geoalchemy2.types.Geometry(geometry_type='POLYGON', srid=4326, from_text='ST_GeomFromEWKT', name='geometry', nullable=False, _spatial_index_reflected=True), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='lahan_pkey')
    )
    op.create_index('ix_lahan_id', 'lahan', ['id'], unique=False)
    op.create_index('idx_lahan_area', 'lahan', ['area'], unique=False, postgresql_using='gist')
    op.create_table('spatial_ref_sys',
    sa.Column('srid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('auth_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('auth_srid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('srtext', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.Column('proj4text', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.CheckConstraint('srid > 0 AND srid <= 998999', name='spatial_ref_sys_srid_check'),
    sa.PrimaryKeyConstraint('srid', name='spatial_ref_sys_pkey')
    )
    # ### end Alembic commands ###
