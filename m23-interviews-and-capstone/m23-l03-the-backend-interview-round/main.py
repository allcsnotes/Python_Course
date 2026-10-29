import hashlib
import json
import time

from fastapi import Depends, FastAPI, Header, HTTPException, Response
from fastapi.responses import JSONResponse
from prometheus_client import (
    CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest,
)
from starlette.requests import Request

import cache
from auth import current_student
from db import pool
from worker import send_certificate

app = FastAPI()
REQUESTS = Counter("http_requests_total", "Requests", ["route", "status"])
SECONDS = Histogram("http_request_seconds", "Latency", ["route"])
ENROLLED = Counter("enrollments_created_total", "New enrollments")
CERTS = Counter("certificates_queued_total", "Certificate jobs queued")


@app.middleware("http")
async def measure(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    route = request.scope.get("route")
    path = route.path if route else "unmatched"
    SECONDS.labels(path).observe(time.perf_counter() - start)
    REQUESTS.labels(path, str(response.status_code)).inc()
    return response


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/health/ready")
def ready():
    with pool.connection() as db:
        db.execute("SELECT 1")
    return {"status": "ready"}


def stored_answer(db, student_id, key, request_hash):
    row = db.execute(
        "SELECT request_hash, status_code, body"
        " FROM idempotency_keys"
        " WHERE student_id = %s AND key = %s",
        (student_id, key),
    ).fetchone()
    if row and row["request_hash"] != request_hash:
        raise HTTPException(422, "key reused")
    return row


def new_enrollment(db, student_id, course_id):
    row = db.execute(
        "INSERT INTO enrollments (student_id, course_id)"
        " VALUES (%s, %s)"
        " ON CONFLICT (student_id, course_id) DO NOTHING"
        " RETURNING id",
        (student_id, course_id),
    ).fetchone()
    if row is None:
        raise HTTPException(409, "already enrolled")
    return row["id"]


@app.post("/courses/{course_id}/enrollments")
def enroll(
    course_id: int,
    student_id: int = Depends(current_student),
    idempotency_key: str | None = Header(default=None),
):
    request_hash = hashlib.sha256(
        f"POST enroll {course_id}".encode()
    ).hexdigest()
    with pool.connection() as db:
        if idempotency_key:
            old = stored_answer(
                db, student_id, idempotency_key, request_hash
            )
            if old:
                return JSONResponse(
                    old["body"],
                    old["status_code"],
                    headers={"Idempotent-Replayed": "true"},
                )
        found = db.execute(
            "SELECT 1 FROM courses WHERE id = %s", (course_id,)
        ).fetchone()
        if not found:
            raise HTTPException(404, "course not found")
        body = {
            "id": new_enrollment(db, student_id, course_id),
            "course_id": course_id,
        }
        if idempotency_key:
            db.execute(
                "INSERT INTO idempotency_keys"
                " VALUES (%s, %s, %s, 201, %s, now())",
                (student_id, idempotency_key, request_hash,
                 json.dumps(body)),
            )
    ENROLLED.inc()
    return JSONResponse(body, 201)


@app.get("/me/enrollments")
def my_enrollments(
    limit: int = 2, after: int = 0, student_id: int = Depends(current_student)
):
    with pool.connection() as db:
        rows = db.execute(
            "SELECT id, course_id FROM enrollments"
            " WHERE student_id = %s AND id > %s ORDER BY id LIMIT %s",
            (student_id, after, limit + 1),
        ).fetchall()
    items = rows[:limit]
    more = len(rows) > limit
    return {"items": items, "next_after": items[-1]["id"] if more else None}


def own_enrollment(db, enrollment_id, student_id):
    row = db.execute(
        "SELECT id, course_id FROM enrollments WHERE id = %s AND student_id = %s",
        (enrollment_id, student_id),
    ).fetchone()
    if row is None:
        raise HTTPException(404, "enrollment not found")
    return row


def load_progress(db, enrollment):
    total = db.execute(
        "SELECT count(*) AS n FROM lessons WHERE course_id = %s", (enrollment["course_id"],)
    ).fetchone()["n"]
    done = db.execute(
        "SELECT count(*) AS n FROM lesson_progress WHERE enrollment_id = %s",
        (enrollment["id"],),
    ).fetchone()["n"]
    return {"done": done, "total": total, "percent": round(100 * done / total)}


@app.put("/enrollments/{enrollment_id}/lessons/{lesson_id}")
def complete_lesson(
    enrollment_id: int, lesson_id: int, student_id: int = Depends(current_student)
):
    cert_id = None
    with pool.connection() as db:
        enrollment = own_enrollment(db, enrollment_id, student_id)
        db.execute(
            "INSERT INTO lesson_progress (enrollment_id, lesson_id) VALUES (%s, %s)"
            " ON CONFLICT DO NOTHING",
            (enrollment_id, lesson_id),
        )
        progress = load_progress(db, enrollment)
        if progress["done"] == progress["total"]:
            row = db.execute(
                "INSERT INTO certificates (enrollment_id) VALUES (%s)"
                " ON CONFLICT (enrollment_id) DO NOTHING RETURNING id",
                (enrollment_id,),
            ).fetchone()
            cert_id = row["id"] if row else None
    if cert_id:
        CERTS.inc()
        try:
            send_certificate.delay(cert_id)
        except Exception:
            pass  # the row stays pending; the sweeper will queue it
    return {**progress, "certificate": "queued" if cert_id else None}


@app.get("/enrollments/{enrollment_id}/progress")
def progress(enrollment_id: int, student_id: int = Depends(current_student)):
    with pool.connection() as db:
        enrollment = own_enrollment(db, enrollment_id, student_id)
        return load_progress(db, enrollment)


def load_popular():
    with pool.connection() as db:
        return db.execute(
            "SELECT course_id, count(*) AS students FROM enrollments"
            " GROUP BY course_id ORDER BY students DESC, course_id LIMIT 3"
        ).fetchall()


@app.get("/courses/popular")
def popular(response: Response):
    value, state = cache.cached("popular", load_popular)
    response.headers["X-Cache"] = state
    return value
