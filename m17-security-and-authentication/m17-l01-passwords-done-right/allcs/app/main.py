from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app import domain, errors
from app.routers import courses, enrollments, students

app = FastAPI(title="allcsvideos backend")
app.include_router(courses.router)
app.include_router(students.router)
app.include_router(enrollments.router)

app.add_exception_handler(domain.NotFound, errors.not_found)
app.add_exception_handler(domain.Conflict, errors.conflict)
app.add_exception_handler(RequestValidationError, errors.bad_input)
