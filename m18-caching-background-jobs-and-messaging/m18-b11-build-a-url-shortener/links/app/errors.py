from fastapi import HTTPException
from fastapi.responses import JSONResponse

CODES = {
    404: "not_found",
    410: "expired",
    429: "too_many_requests",
}


def error(status, code, message, **more):
    body = {
        "error": {"code": code, "message": message, **more}
    }
    return JSONResponse(body, status_code=status)


def bad_input(request, exc):
    fields = [
        {"field": e["loc"][-1], "problem": e["msg"]}
        for e in exc.errors()
    ]
    return error(
        422, "invalid_input", "Wrong input", fields=fields
    )


def http_error(request, exc):
    code = CODES.get(exc.status_code, "error")
    response = error(exc.status_code, code, exc.detail)
    response.headers.update(exc.headers or {})
    return response


def fail(status, message, headers=None):
    raise HTTPException(status, message, headers=headers)
