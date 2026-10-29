from fastapi import Request
from opentelemetry import trace
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import (
    HTTPXClientInstrumentor,
)
from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor

from app import errors, tracing


def install(app):
    tracing.start("allcs-api")
    tracing.setup_logging()

    @app.middleware("http")
    async def request_id(request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception as exc:
            response = errors.server_error(request, exc)
        ctx = trace.get_current_span().get_span_context()
        response.headers["X-Request-ID"] = format(
            ctx.trace_id, "032x"
        )
        return response

    FastAPIInstrumentor.instrument_app(
        app, exclude_spans=["send", "receive"]
    )
    PsycopgInstrumentor().instrument()
    RedisInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()
    CeleryInstrumentor().instrument()
