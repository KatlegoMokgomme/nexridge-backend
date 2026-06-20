from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.ticket import Ticket

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# -------------------------------------------------
# BASIC TEST ROUTE (CONFIRM AUTH WORKS)
# -------------------------------------------------
@router.get("/")
def dashboard_home(user=Depends(get_current_user)):
    return {
        "message": "Dashboard API is working",
        "user_id": user.get("sub")
    }


# -------------------------------------------------
# ANALYTICS ENDPOINT (USED BY FRONTEND)
# -------------------------------------------------
@router.get("/analytics")
def get_dashboard_analytics(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Total tickets
    total_tickets = db.query(Ticket).count()

    # Open tickets
    open_tickets = db.query(Ticket).filter(Ticket.status == "open").count()

    # Closed tickets
    closed_tickets = db.query(Ticket).filter(Ticket.status == "closed").count()

    # In progress tickets
    in_progress = db.query(Ticket).filter(Ticket.status == "in_progress").count()

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "closed_tickets": closed_tickets,
        "in_progress": in_progress,
        "user": user.get("sub")
    }