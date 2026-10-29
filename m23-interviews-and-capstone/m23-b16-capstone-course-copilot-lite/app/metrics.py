from prometheus_client import Counter, Histogram

REQUESTS = Counter(
    "copilot_requests_total",
    "Requests by route and status",
    ["method", "route", "status"],
)
LATENCY = Histogram(
    "copilot_request_seconds", "Request time", ["route"]
)
SEARCHES = Counter(
    "copilot_searches_total", "Searches", ["cache"]
)
