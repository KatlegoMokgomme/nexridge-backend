from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


# ========================
# REGISTER USER
# ========================
def create_user(db: Session, user_data):
    user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role=user_data.role or "user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# ========================
# AUTHENTICATE USER
# ========================
def authenticate_user(db: Session, username: str, password: str):
    # username = email (OAuth2 convention)
    user = db.query(User).filter(User.email == username).first()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


# ========================
# LOGIN USER (OAUTH2 FLOW)
# ========================
def login_user(db: Session, username: str, password: str):
    user = authenticate_user(db, username, password)

    if not user:
        return None

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }