from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.core.database import get_db
from app.models.user import User
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------------
# REGISTER (FIXED)
# ------------------------
@router.post("/register")
def register(payload: dict, db: Session = Depends(get_db)):

    user_exists = db.query(User).filter(
        User.username == payload["username"]
    ).first()

    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = pwd_context.hash(payload["password"])

    user = User(
        username=payload["username"],
        email=payload["email"],
        password=hashed
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created"}


# ------------------------
# LOGIN (FIXED)
# ------------------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }