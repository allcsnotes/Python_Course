from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError

from app import auth, domain, errors, google
from app.deps import get_current_user
from app.models import Student
from app.schemas import StudentOut
from app.routers import courses, enrollments, students

app = FastAPI(title="allcsvideos backend")
app.include_router(courses.router)
app.include_router(students.router)
app.include_router(enrollments.router)
app.include_router(auth.router)
app.include_router(google.router)

app.add_exception_handler(domain.NotFound, errors.not_found)
app.add_exception_handler(domain.Conflict, errors.conflict)
app.add_exception_handler(RequestValidationError, errors.bad_input)


@app.get("/me", response_model=StudentOut)
def me(user: Student = Depends(get_current_user)):
    return user
