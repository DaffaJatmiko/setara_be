"""Initial migration

Revision ID: 4571bedc38f1
Revises: 
Create Date: 2024-12-21 00:46:46.622995

"""
import random
from typing import Sequence, Union

from alembic import op
from geoalchemy2 import Geometry
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4571bedc38f1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Koordinat area daratan Lampung yang aman (area diperluas tapi tetap di darat)
SAFE_AREAS = [
    # Lampung Tengah dan Timur (termasuk Metro, Sukadana, dst)
    {
        'lat_min': -5.25,
        'lat_max': -4.70,
        'long_min': 105.10,
        'long_max': 105.65
    },
    # Lampung Utara dan Way Kanan (termasuk Kotabumi, Blambangan Umpu)
    {
        'lat_min': -4.85,
        'lat_max': -4.20,
        'long_min': 104.45,
        'long_max': 105.10
    },
    # Lampung Barat (termasuk Liwa dan sekitarnya)
    {
        'lat_min': -5.15,
        'lat_max': -4.80,
        'long_min': 104.0,
        'long_max': 104.45
    },
    # Lampung Selatan bagian daratan (menghindari teluk)
    {
        'lat_min': -5.65,
        'lat_max': -5.25,
        'long_min': 104.85,
        'long_max': 105.45
    },
    # Pringsewu dan Tanggamus daratan
    {
        'lat_min': -5.45,
        'lat_max': -5.10,
        'long_min': 104.45,
        'long_max': 104.95
    }
]

def generate_random_point():
    """Generate random point within safe areas of Lampung province"""
    # Pilih random area
    area = random.choice(SAFE_AREAS)
    
    # Generate koordinat dalam area yang dipilih
    lat = random.uniform(area['lat_min'], area['lat_max'])
    long = random.uniform(area['long_min'], area['long_max'])
    
    return f'POINT({long} {lat})'

def upgrade() -> None:
    # Membuat data seed
    mitra_table = sa.table(
        'mitra',
        sa.Column('id', sa.Integer()),
        sa.Column('nama', sa.String()),
        sa.Column('lokasi', Geometry('POINT', srid=4326))
    )
    
    seed_data = []
    for i in range(1, 101):
        seed_data.append({
            'id': i,
            'nama': f'Mitra Coffee {i}',
            'lokasi': generate_random_point()
        })
    
    # Insert data
    op.bulk_insert(mitra_table, seed_data)

def downgrade() -> None:
    op.drop_table('mitra')