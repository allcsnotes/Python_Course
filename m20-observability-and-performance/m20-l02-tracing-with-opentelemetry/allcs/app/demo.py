# routes that exist only for the lesson (not part of the real API)
import os
import time

from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import get_session
from app.settings import get_settings

router = APIRouter(tags=["demo"])


@router.get("/version")
def version():
    return {"version": get_settings().app_version, "pid": os.getpid()}


@router.get("/whoami")
def whoami(request: Request):
    return {
        "client": request.client.host,
        "x_forwarded_for": request.headers.get("x-forwarded-for"),
    }


@router.get("/slow")
def slow(seconds: float = 1):
    time.sleep(seconds)
    return {"slept": seconds, "pid": os.getpid()}


@router.get("/dbslow")
def dbslow(session: Session = Depends(get_session)):
    session.execute(text("select pg_sleep(2)"))
    return {"pid": os.getpid()}


@router.get("/spin")
def spin():
    total = sum(n * n for n in range(16_000_000))
    return {"total": total, "pid": os.getpid()}


@router.get("/boom")
def boom():
    return 1 / 0
