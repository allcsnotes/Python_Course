import hashlib
import logging
import secrets
import time
from collections import defaultdict, deque
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import cache
from app.db import get_session
from app.deps import get_current_user, oauth2_scheme
from app.models import RefreshToken, Student
from app.security import (
    DUMMY_HASH,
    hash_password,
    needs_rehash,
    verify_password,
)
from app.tokens import make_access_token, seconds_left

router = APIRouter(prefix="/auth", tags=["auth"])
REFRESH_DAYS = 7
log = logging.getLogger("allcs.auth")
FAILED = defaultdict(deque)


def count_failure(email):
    now = time.monotonic()
    times = FAILED[email]
    times.append(now)
    while now - times[0] > 60:
        times.popleft()
    return len(times)


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
    query = select(Student).where(Student.email == form.username)
    student = session.scalars(query).first()
    stored = student.password_hash if student else None
    ok = verify_password(stored or DUMMY_HASH, form.password)
    if stored is None or not ok:
        count = count_failure(form.username)
        log.warning(
            "login failed for %s (%d in the last minute)",
            form.username,
            count,
        )
        raise HTTPException(401, "Wrong email or password")
    FAILED.pop(form.username, None)
    log.info("login ok for student %d", student.id)
    if needs_rehash(stored):
        student.password_hash = hash_password(form.password)
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


@router.post("/revoke", status_code=204)
def revoke(
    token: str = Depends(oauth2_scheme),
    user: Student = Depends(get_current_user),
):
    key = cache.blocked_key(token)
    cache.r.set(key, user.id, ex=seconds_left(token))
