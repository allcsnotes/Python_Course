from api import app, error
import db


@app.get("/courses/{course_id}/students")
def students(course_id: int):
    db.connect()
    return []


@app.exception_handler(Exception)
def crash(request, exc):
    return error(500, "server_error", str(exc))
