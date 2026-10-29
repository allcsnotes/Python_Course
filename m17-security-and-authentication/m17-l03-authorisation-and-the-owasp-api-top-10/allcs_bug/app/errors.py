from fastapi.responses import JSONResponse


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
