import time

from fastapi import Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
    multiprocess,
)

REQUESTS = Counter(
    "http_requests_total",
    "Requests handled",
    ["method", "route", "status"],
)
IN_FLIGHT = Gauge(
    "http_requests_in_flight",
    "Requests being handled right now",
    multiprocess_mode="livesum",
)
LATENCY = Histogram(
    "http_request_seconds",
    "Time to answer a request",
    ["route"],
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5),
)
ENROLLMENTS = Counter(
    "enrollments_total", "Students enrolled in a course"
)


SKIP = ("/metrics", "/health/live", "/health/ready")


async def measure(request, call_next):
    if request.url.path in SKIP:
        return await call_next(request)
    IN_FLIGHT.inc()
    start = time.perf_counter()
    status = 500
    try:
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        IN_FLIGHT.dec()
        route = request.scope.get("route")
        path = route.path if route else "unmatched"
        REQUESTS.labels(request.method, path, status).inc()
        LATENCY.labels(path).observe(time.perf_counter() - start)


def registry():
    reg = CollectorRegistry()
    multiprocess.MultiProcessCollector(reg)
    return reg


def endpoint(request):
    body = generate_latest(registry())
    return Response(
        body, headers={"Content-Type": CONTENT_TYPE_LATEST}
    )
