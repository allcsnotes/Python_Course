from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.deps import current_user
from app.models import User
from app.schemas import Register, Token, UserOut
from app.security import (
    DUMMY,
    check_password,
    hash_password,
    make_token,
)

router = APIRouter(tags=["auth"])


@router.post("/auth/register", status_code=201)
def register(
    body: Register, session: Session = Depends(get_session)
) -> UserOut:
    taken = session.scalar(
        select(User).where(User.email == body.email)
    )
    if taken:
        raise HTTPException(409, "email already registered")
    user = User(
        email=body.email,
        name=body.name,
        password_hash=hash_password(body.password),
    )
    session.add(user)
    session.commit()
    return UserOut.model_validate(
        user, from_attributes=True
    )


@router.post("/auth/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> Token:
    user = session.scalar(
        select(User).where(User.email == form.username)
    )
    stored = user.password_hash if user else DUMMY
    ok = check_password(stored, form.password)
    if user is None or not ok:
        raise HTTPException(401, "wrong email or password")
    return Token(
        access_token=make_token(user.id, user.role)
    )


@router.get("/me")
def me(user: User = Depends(current_user)) -> UserOut:
    return UserOut.model_validate(
        user, from_attributes=True
    )
