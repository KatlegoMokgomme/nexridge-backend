from pydantic import BaseModel


# ------------------------
# LOGIN SCHEMA
# ------------------------
class LoginRequest(BaseModel):
    email: str
    password: str