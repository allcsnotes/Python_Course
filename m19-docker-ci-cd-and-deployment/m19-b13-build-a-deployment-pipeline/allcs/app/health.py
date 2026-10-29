import redis as redis_lib
from fastapi import APIRouter, Response
from sqlalchemy import text

from app.db import engine
from app.worker import redis

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
def live():
    return {"status": "alive"}


@router.get("/ready")
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
    except redis_lib.RedisError:
        checks["redis"] = "down"
    ready = "down" not in checks.values()
    if not ready:
        response.status_code = 503
    return {
        "status": "ready" if ready else "not ready",
        **checks,
    }
