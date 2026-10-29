import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import RefreshToken, Student
from app.security import verify_password
from app.tokens import make_access_token

router = APIRouter(prefix="/auth", tags=["auth"])
REFRESH_DAYS = 7


class RefreshIn(BaseModel):
    refresh_token: str


def digest(token):
    return hashlib.sha256(token.encode()).hexdigest()


def issue_pair(session, student):
    refresh = secrets.token_urlsafe(32)
    expires = datetime.now(UTC) + timedelta(days=REFRESH_DAYS)
    session.add(
        RefreshToken(
            student_id=student.id,
            token_hash=digest(refresh),
            expires_at=expires,
        )
    )
    session.commit()
    return {
        "access_token": make_access_token(student.id),
        "refresh_token": refresh,
        "token_type": "bearer",
    }


def find_refresh(session, token):
    query = select(RefreshToken).where(
        RefreshToken.token_hash == digest(token)
    )
    return session.scalars(query).first()


@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    email = form.username
    query = select(Student).where(Student.email == email)
    student = session.scalars(query).first()
    stored = student.password_hash if student else None
    plain = form.password
    if not stored or not verify_password(stored, plain):
        raise HTTPException(401, "Wrong email or password")
    return issue_pair(session, student)


@router.post("/refresh")
def refresh(
    data: RefreshIn, session: Session = Depends(get_session)
):
    row = find_refresh(session, data.refresh_token)
    if row is None or row.revoked:
        raise HTTPException(401, "Invalid refresh token")
    if row.expires_at < datetime.now(UTC):
        raise HTTPException(401, "Refresh token expired")
    row.revoked = True
    return issue_pair(session, row.student)


@router.post("/logout", status_code=204)
def logout(
    data: RefreshIn, session: Session = Depends(get_session)
):
    row = find_refresh(session, data.refresh_token)
    if row is not None:
        row.revoked = True
        session.commit()
