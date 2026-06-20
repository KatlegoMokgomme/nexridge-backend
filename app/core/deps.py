from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return payload


# ---> ADD THIS FUNCTION BELOW <---
def require_role(required_role: str):
    """
    Dependency to restrict access to specific user roles.
    """

    def role_checker(current_user: dict = Depends(get_current_user)):
        # This assumes your token payload looks like {"sub": "...", "role": "admin"}
        # Adjust "role" if your payload uses a different key (like "user_role")
        user_role = current_user.get("role") or current_user.get("user_role")

        if not user_role or user_role != required_role:
            raise HTTPException(
                status_code=403,
                detail="You do not have the required permissions to access this resource"
            )
        return current_user

    return role_checker