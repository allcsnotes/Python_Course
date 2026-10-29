from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Student
from app.tokens import make_token

hasher = PasswordHasher()
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    query = select(Student).where(Student.email == form.username)
    student = session.scalars(query).first()
    wrong = HTTPException(401, "Wrong email or password")
    if student is None:
        raise wrong
    try:
        hasher.verify(student.password_hash, form.password)
    except VerifyMismatchError:
        raise wrong
    token = make_token(student.id)
    return {"access_token": token, "token_type": "bearer"}
