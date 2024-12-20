# migrations/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Import model-model Anda
from app.models import user, program, map 
from app.core.database import Base
from app.core.config import settings

# Konfigurasi logging Alembic
config = context.config

# Aktifkan logging jika ada file konfigurasi
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata dari Base SQLAlchemy
target_metadata = Base.metadata

# Konfigurasi koneksi database dari environment
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()