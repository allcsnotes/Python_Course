import redis
from fastapi import APIRouter, Response
from sqlalchemy import text

from app.cache import r
from app.db import engine

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
        r.ping()
        checks["redis"] = "ok"
    except redis.RedisError:
        checks["redis"] = "down"
    ready = "down" not in checks.values()
    if not ready:
        response.status_code = 503
    return {"status": "ready" if ready else "not ready", **checks}
