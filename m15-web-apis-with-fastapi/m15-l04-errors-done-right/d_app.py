from fastapi import FastAPI
from fastapi.responses import JSONResponse

import domain

app = FastAPI()


@app.exception_handler(domain.CourseNotFound)
def not_found(request, exc):
    body = {"detail": f"Course {exc} not found"}
    return JSONResponse(body, status_code=404)


@app.exception_handler(domain.AlreadyEnrolled)
def already(request, exc):
    body = {"detail": f"{exc} is already enrolled"}
    return JSONResponse(body, status_code=409)


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    return domain.find_course(course_id)


@app.post("/enrol/{student}/{course_id}")
def enrol(student: str, course_id: int):
    return domain.enrol(student, course_id)
