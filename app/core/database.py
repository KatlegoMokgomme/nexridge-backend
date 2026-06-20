from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------------
# DATABASE URL
# ------------------------
# Replace this with your real PostgreSQL credentials
# Change 'username' to 'postgres' (or your custom PostgreSQL username)
DATABASE_URL = "postgresql://postgres:KM183@localhost:5432/NexridgeTech"


# ------------------------
# ENGINE
# ------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # prevents stale DB connections
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
# BASE CLASS (MODELS INHERIT THIS)
# ------------------------
Base = declarative_base()


# ------------------------
# DEPENDENCY (FASTAPI DB SESSION)
# ------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()