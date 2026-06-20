from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_role

from app.schemas.ticket import TicketCreate
from app.services.ticket_service import (
    create_ticket,
    get_all_tickets,
    assign_ticket
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])


# ------------------------
# CREATE TICKET
# ------------------------
@router.post("/")
def create_new_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return create_ticket(db, ticket, user["user_id"])


# ------------------------
# GET ALL TICKETS (ADMIN ONLY)
# ------------------------
@router.get("/")
def list_tickets(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return get_all_tickets(db)


# ------------------------
# ASSIGN TICKET (ADMIN ONLY)
# ------------------------
@router.put("/{ticket_id}/assign")
def assign_ticket_route(
    ticket_id: int,
    technician_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    result = assign_ticket(db, ticket_id, technician_id)

    if not result:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {
        "message": "Ticket assigned successfully",
        "ticket": result
    }