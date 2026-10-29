import logging

from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app import domain, errors
from app.deps import get_current_user
from app.models import Student
from app.routers import admin, auth, courses, enrollments, students
from app.schemas import StudentOut

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
)

app = FastAPI(title="allcsvideos backend")
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(students.router)
app.include_router(enrollments.router)
app.add_exception_handler(domain.NotFound, errors.not_found)
app.add_exception_handler(domain.Conflict, errors.conflict)
app.add_exception_handler(RequestValidationError, errors.bad_input)
app.add_exception_handler(HTTPException, errors.http_error)


@app.get("/me", response_model=StudentOut)
def me(user: Student = Depends(get_current_user)):
    return user
