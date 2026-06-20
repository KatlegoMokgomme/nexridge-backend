from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import login_user

router = APIRouter(prefix="/auth", tags=["Auth"])


# ========================
# LOGIN (OAUTH2 STYLE)
# ========================
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    token = login_user(db, form_data.username, form_data.password)

    if not token:
        return {"error": "Invalid credentials"}

    return token