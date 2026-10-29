import time
from jobs import build_report, check_pages


def measure(name, job):
    start = time.perf_counter()
    job()
    wall = time.perf_counter() - start
    print(f"{name}: wall {wall:.2f} s")


measure("build_report", build_report)
measure("check_pages", check_pages)
