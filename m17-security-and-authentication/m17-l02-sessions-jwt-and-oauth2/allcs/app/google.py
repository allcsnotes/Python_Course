import os
import secrets
from urllib.parse import urlencode

import httpx
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import issue_pair
from app.db import get_session
from app.models import Student

router = APIRouter(prefix="/auth/google", tags=["auth"])
GOOGLE = os.environ.get("GOOGLE_URL", "http://localhost:8272")
CLIENT_ID = "allcs-demo-client"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
CALLBACK = "http://localhost:8172/auth/google/callback"
STATES = set()


@router.get("/login")
def google_login():
    state = secrets.token_urlsafe(16)
    STATES.add(state)
    query = urlencode(
        {
            "client_id": CLIENT_ID,
            "redirect_uri": CALLBACK,
            "response_type": "code",
            "scope": "openid email",
            "state": state,
        }
    )
    return RedirectResponse(f"{GOOGLE}/authorize?{query}")


@router.get("/callback")
def google_callback(
    code: str,
    state: str,
    session: Session = Depends(get_session),
):
    if state not in STATES:
        raise HTTPException(400, "Unknown state")
    STATES.discard(state)
    reply = httpx.post(
        f"{GOOGLE}/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": CALLBACK,
        },
    ).json()
    key = httpx.get(f"{GOOGLE}/public-key").text
    claims = jwt.decode(
        reply["id_token"],
        key,
        algorithms=["RS256"],
        audience=CLIENT_ID,
    )
    email = claims["email"]
    query = select(Student).where(Student.email == email)
    student = session.scalars(query).first()
    if student is None:
        raise HTTPException(404, "No student with this email")
    return issue_pair(session, student)
