from fastapi.exceptions import RequestValidationError

from api import app, error
from store import courses


@app.get("/courses")
def list_courses(limit: int = 10):
    return list(courses.values())[:limit]


@app.exception_handler(RequestValidationError)
def bad_input(request, exc):
    fields = [
        {"field": e["loc"][-1], "problem": e["msg"]}
        for e in exc.errors()
    ]
    return error(422, "invalid_input", "Wrong input",
                 fields=fields)
