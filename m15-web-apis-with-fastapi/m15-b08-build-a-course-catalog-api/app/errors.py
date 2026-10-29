from fastapi.responses import JSONResponse


def error(status, code, message, **more):
    body = {"error": {"code": code, "message": message, **more}}
    return JSONResponse(body, status_code=status)


def not_found(request, exc):
    return error(404, "course_not_found", f"Course {exc} not found")


def duplicate(request, exc):
    return error(409, "duplicate_title", f"{exc} already exists")


def bad_input(request, exc):
    fields = [
        {"field": e["loc"][-1], "problem": e["msg"]}
        for e in exc.errors()
    ]
    return error(422, "invalid_input", "Wrong input", fields=fields)
