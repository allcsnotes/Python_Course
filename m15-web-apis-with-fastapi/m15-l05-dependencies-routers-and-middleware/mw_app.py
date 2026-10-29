import logging
import time

from fastapi import FastAPI, Request

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("catalog")
app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time"] = f"{ms:.0f}ms"
    log.info(
        "%s %s -> %d in %.0f ms",
        request.method,
        request.url.path,
        response.status_code,
        ms,
    )
    return response


@app.get("/courses")
def list_courses():
    return [{"id": 1, "title": "Python Basics"}]


@app.get("/slow")
def slow():
    time.sleep(0.3)
    return {"slept": 0.3}
