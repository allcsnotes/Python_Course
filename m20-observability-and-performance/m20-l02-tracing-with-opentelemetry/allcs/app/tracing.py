import logging

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def start(service):
    """Say who we are, and where the spans go."""
    provider = TracerProvider(
        resource=Resource.create({"service.name": service})
    )
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter())
    )
    trace.set_tracer_provider(provider)


class TraceIdFilter(logging.Filter):
    """Put the current trace ID on every log record."""

    def filter(self, record):
        ctx = trace.get_current_span().get_span_context()
        record.trace_id = (
            format(ctx.trace_id, "032x") if ctx.is_valid else "-"
        )
        return True


def setup_logging():
    handler = logging.StreamHandler()
    handler.addFilter(TraceIdFilter())
    handler.setFormatter(
        logging.Formatter(
            "%(levelname)s %(name)s [%(trace_id)s] %(message)s"
        )
    )
    logging.basicConfig(
        level=logging.INFO, handlers=[handler], force=True
    )
