import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -----------------------------------

# DATABASE URL (Render or Local)

# -----------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

# Safety fallback for local development ONLY

if not DATABASE_URL:
DATABASE_URL = "sqlite:///./nexridge.db"

# -----------------------------------

# SQLALCHEMY ENGINE

# -----------------------------------

engine = create_engine(
DATABASE_URL,
pool_pre_ping=True,
echo=False
)

# -----------------------------------

# SESSION FACTORY

# -----------------------------------

SessionLocal = sessionmaker(
autocommit=False,
autoflush=False,
bind=engine
)

# -----------------------------------

# BASE MODEL

# -----------------------------------

Base = declarative_base()

# -----------------------------------

# DEPENDENCY (FOR FASTAPI ROUTES)

# -----------------------------------

def get_db():
db = SessionLocal()
try:
yield db
finally:
db.close()
