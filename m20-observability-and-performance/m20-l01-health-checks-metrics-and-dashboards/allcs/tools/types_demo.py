from prometheus_client import CollectorRegistry, Counter, Gauge
from prometheus_client import Histogram, generate_latest

reg = CollectorRegistry()
enrolls = Counter("enrollments", "Students enrolled", registry=reg)
online = Gauge("students_online", "Students online", registry=reg)
speed = Histogram("page_seconds", "Page time", registry=reg,
                  buckets=(0.1, 0.5, 1, 5))

enrolls.inc(3)
online.set(42)
online.dec(3)
for seconds in (0.04, 0.3, 2.0):
    speed.observe(seconds)

print(generate_latest(reg).decode())
