from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    # ------------------------
    # PRIMARY KEY
    # ------------------------
    id = Column(Integer, primary_key=True, index=True)

    # ------------------------
    # BASIC TICKET INFO
    # ------------------------
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)

    priority = Column(String, default="low")   # low | medium | high
    status = Column(String, default="open")     # open | in_progress | closed

    # ------------------------
    # USERS
    # ------------------------
    created_by = Column(String, index=True, nullable=False)
    assigned_to = Column(String, nullable=True)

    # ------------------------
    # TIMESTAMPS
    # ------------------------
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    resolved_at = Column(DateTime, nullable=True)

    # ------------------------
    # SLA TRACKING
    # ------------------------
    sla_hours = Column(Integer, default=24)

    # ------------------------
    # OPTIONAL FIELDS (FUTURE-PROOFING)
    # ------------------------
    category = Column(String, nullable=True)
    source = Column(String, nullable=True)  # e.g. email, web, api