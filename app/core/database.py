import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

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
    pool_pre_ping=True,
    echo=False
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
# BASE MODEL
# ------------------------
Base = declarative_base()

# ------------------------
# DEPENDENCY (FASTAPI)
# ------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()