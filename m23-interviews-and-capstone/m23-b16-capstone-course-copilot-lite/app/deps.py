import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import User
from app.security import read_token

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


def current_user(
    token: str = Depends(oauth2),
    session: Session = Depends(get_session),
):
    try:
        user_id = read_token(token)
    except jwt.PyJWTError:
        raise HTTPException(401, "invalid token") from None
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(401, "unknown user")
    return user


def require_admin(user: User = Depends(current_user)):
    if user.role != "admin":
        raise HTTPException(403, "admins only")
    return user
