import logging
import time
import uuid

from fastapi import FastAPI, Request

from app import health
from app.logs import configure_logging, request_id
from app.metrics import LATENCY, REQUESTS
from app.routers import admin, auth, learn, search
from app.settings import get_settings

configure_logging(get_settings().log_level)
log = logging.getLogger("copilot.api")
app = FastAPI(title="Course Copilot-lite")
for module in (health, auth, search, learn, admin):
    app.include_router(module.router)


@app.middleware("http")
async def observe(request: Request, call_next):
    rid = (
        request.headers.get("x-request-id")
        or uuid.uuid4().hex[:12]
    )
    request_id.set(rid)
    started = time.perf_counter()
    response = await call_next(request)
    seconds = time.perf_counter() - started
    route = getattr(
        request.scope.get("route"), "path", "other"
    )
    REQUESTS.labels(
        request.method, route, response.status_code
    ).inc()
    LATENCY.labels(route).observe(seconds)
    response.headers["X-Request-ID"] = rid
    log.info(
        "request",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "ms": round(seconds * 1000, 1),
        },
    )
    return response
