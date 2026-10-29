from fastapi import FastAPI
from fastapi.responses import JSONResponse

import domain

app = FastAPI()


@app.exception_handler(domain.CourseNotFound)
def not_found(request, exc):
    body = {"error": f"Course {exc} not found"}
    return JSONResponse(body)


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    return domain.find_course(course_id)
