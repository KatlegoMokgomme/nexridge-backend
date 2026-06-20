from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from passlib.context import CryptContext

from app.core.database import get_db
from app.services.auth_service import login_user
from app.models.user import User
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# ------------------------
# PASSWORD HASHING
# ------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ========================
# REGISTER USER
# ========================
@router.post("/register")
def register(user_data: dict, db: Session = Depends(get_db)):

    # check if user exists
    existing_user = db.query(User).filter(
        User.username == user_data["username"]
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # hash password
    hashed_password = pwd_context.hash(user_data["password"])

    new_user = User(
        username=user_data["username"],
        email=user_data["email"],
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully"
    }


# ========================
# LOGIN (OAUTH2 STYLE)
# ========================
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

    # verify password
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # create JWT token
    token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }