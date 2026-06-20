from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from app.core.security import oauth2_scheme, SECRET_KEY, ALGORITHM


# ========================
# GET CURRENT USER
# ========================
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("sub")
        role: str = payload.get("role", "user")  # default safe fallback

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user id"
            )

        return {
            "user_id": user_id,
            "role": role
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


# ========================
# ROLE CHECK (ADMIN ONLY)
# ========================
def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        if user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: {required_role} role required"
            )
        return user

    return role_checker