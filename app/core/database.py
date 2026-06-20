import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -----------------------------
# DATABASE URL
# -----------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

# fallback ONLY for local dev
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./nexridge.db"

# -----------------------------
# ENGINE
# -----------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# -----------------------------
# SESSION
# -----------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -----------------------------
# BASE MODEL
# -----------------------------
Base = declarative_base()

# -----------------------------
# DB DEPENDENCY
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()