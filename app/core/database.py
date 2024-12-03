# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from .config import settings

# Buat engine database
engine = create_engine(
    settings.DATABASE_URL, 
    poolclass=NullPool  # Untuk koneksi yang lebih aman
)

# Buat SessionLocal untuk transaksi database
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# Base untuk model ORM
Base = declarative_base()

def get_db():
    """
    Dependency untuk mendapatkan database session
    Akan digunakan di route-route FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()