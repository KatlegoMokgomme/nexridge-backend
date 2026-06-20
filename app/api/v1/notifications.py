from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
# Import your authentication dependency (we saw this in your dashboard file)
from app.core.deps import require_role
from app.services.notifications_service import get_notifications

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/")
def list_notifications(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    # This matches the dictionary structure defined in your deps.py
    return get_notifications(db=db, user_id=current_user["user_id"])