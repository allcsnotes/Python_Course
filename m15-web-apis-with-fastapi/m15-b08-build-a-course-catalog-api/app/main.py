from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app import domain, errors
from app.routers import courses

app = FastAPI(title="allcsvideos catalog")
app.include_router(courses.router)

app.add_exception_handler(domain.CourseNotFound, errors.not_found)
app.add_exception_handler(domain.DuplicateTitle, errors.duplicate)
app.add_exception_handler(RequestValidationError, errors.bad_input)
