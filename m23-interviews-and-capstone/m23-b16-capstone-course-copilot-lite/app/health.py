from fastapi import APIRouter, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    generate_latest,
)
from sqlalchemy import text

from app.cache import redis
from app.db import engine

router = APIRouter()


@router.get("/health/live")
def live():
    return {"status": "alive"}


@router.get("/health/ready")
def ready(response: Response):
    checks = {}
    try:
        with engine.connect() as conn:
            conn.execute(text("select 1"))
        checks["postgres"] = "ok"
    except Exception:
        checks["postgres"] = "down"
    try:
        redis.ping()
        checks["redis"] = "ok"
    except Exception:
        checks["redis"] = "down"
    up = "down" not in checks.values()
    if not up:
        response.status_code = 503
    return {
        "status": "ready" if up else "not ready",
        **checks,
    }


@router.get("/metrics")
def metrics():
    return Response(
        generate_latest(), media_type=CONTENT_TYPE_LATEST
    )
