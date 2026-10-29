import logging

from fastapi.responses import JSONResponse
from opentelemetry import trace


def error(status, code, message, **more):
    body = {"error": {"code": code, "message": message, **more}}
    return JSONResponse(body, status_code=status)


def not_found(request, exc):
    message = f"{exc.kind} {exc.item_id} not found"
    return error(404, "not_found", message)


def conflict(request, exc):
    return error(409, exc.code, exc.message)


def bad_input(request, exc):
    fields = [
        {"field": e["loc"][-1], "problem": e["msg"]}
        for e in exc.errors()
    ]
    return error(422, "invalid_input", "Wrong input", fields=fields)


CODES = {401: "not_authenticated", 403: "forbidden"}


def http_error(request, exc):
    code = CODES.get(exc.status_code, "error")
    response = error(exc.status_code, code, exc.detail)
    response.headers.update(exc.headers or {})
    return response


log = logging.getLogger("allcs.errors")


def server_error(request, exc):
    ctx = trace.get_current_span().get_span_context()
    error_id = format(ctx.trace_id, "032x")
    log.error("error %s", error_id, exc_info=exc)
    return error(
        500, "server_error", "Something went wrong",
        error_id=error_id,
    )
