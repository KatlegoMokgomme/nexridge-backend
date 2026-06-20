from app.models.user import User
from app.core.security import create_access_token


def login_user(db, username: str, password: str):

    # find user (supports username OR email style systems)
    user = db.query(User).filter(
        (User.username == username) | (User.email == username)
    ).first()

    if not user:
        return None

    # plain password check (TEMP DEV VERSION)
    # later we upgrade to bcrypt
    if user.password != password:
        return None

    token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }