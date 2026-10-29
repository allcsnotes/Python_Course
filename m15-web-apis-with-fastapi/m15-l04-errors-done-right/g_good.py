import logging
import uuid

from api import app, error
import db

log = logging.getLogger(__name__)


@app.get("/courses/{course_id}/students")
def students(course_id: int):
    db.connect()
    return []


@app.exception_handler(Exception)
def crash(request, exc):
    error_id = uuid.uuid4().hex[:8]
    log.error("error %s", error_id, exc_info=exc)
    return error(500, "server_error", "Something went wrong",
                 error_id=error_id)
