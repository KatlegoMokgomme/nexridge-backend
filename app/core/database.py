import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# ------------------------
# DATABASE URL (PRODUCTION SAFE)
# ------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

# If Render doesn't provide it yet → fallback to SQLite
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./nexridge.db"

# Fix for Render PostgreSQL (important)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://")

# ------------------------
# ENGINE
# ------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Disconnect protection
    echo=False           # Set to True if you want to see SQL queries in logs
)

# ------------------------
# SESSION
# ------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ------------------------
# BASE MODEL (SQLAlchemy 2.0+ Style)
# ------------------------
class Base(DeclarativeBase):
    """
    Subclass this Base to define your database models.
    Provides better type-hinting and IDE auto-complete than declarative_base().
    """
    pass

# ------------------------
# DEPENDENCY (FASTAPI)
# ------------------------
def get_db():
    """
    FastAPI dependency injection to yield a database session per request
    and ensure it is closed properly afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()