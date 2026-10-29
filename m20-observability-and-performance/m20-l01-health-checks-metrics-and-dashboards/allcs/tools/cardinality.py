from prometheus_client import CollectorRegistry, Counter
from prometheus_client import generate_latest

ROUTES = ["/courses", "/courses/{id}", "/enrollments"]


def series_count(label_names, combos):
    reg = CollectorRegistry()
    hits = Counter("hits", "Requests", label_names, registry=reg)
    for combo in combos:
        hits.labels(*combo).inc()
    lines = generate_latest(reg).decode().splitlines()
    return sum(x.startswith("hits_total") for x in lines)


few = [(route,) for route in ROUTES]
many = [(r, str(u)) for r in ROUTES for u in range(2000)]
print("label route:       ", series_count(["route"], few))
print("label route + user:", series_count(["route", "user"], many))
