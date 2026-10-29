from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as HTTPErr

import domain

app = FastAPI()


def error(status, code, message, **more):
    body = {"code": code, "message": message, **more}
    return JSONResponse({"error": body}, status_code=status)


@app.exception_handler(domain.CourseNotFound)
def not_found(request, exc):
    message = f"Course {exc} not found"
    return error(404, "course_not_found", message)


@app.exception_handler(domain.AlreadyEnrolled)
def already(request, exc):
    message = f"{exc} is already enrolled"
    return error(409, "already_enrolled", message)


@app.exception_handler(HTTPErr)
def http_error(request, exc):
    status = exc.status_code
    return error(status, "http_error",
                 str(exc.detail))


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    return domain.find_course(course_id)


@app.post("/enrol/{student}/{course_id}")
def enrol(student: str, course_id: int):
    return domain.enrol(student, course_id)
