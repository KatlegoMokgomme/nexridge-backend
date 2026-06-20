from pydantic import BaseModel
from typing import Optional


# ------------------------
# CREATE TICKET SCHEMA
# ------------------------
class TicketCreate(BaseModel):
    title: str
    description: str
    priority: Optional[str] = "low"


# ------------------------
# RESPONSE SCHEMA
# ------------------------
class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    created_by: str
    assigned_to: Optional[str]

    class Config:
        from_attributes = True