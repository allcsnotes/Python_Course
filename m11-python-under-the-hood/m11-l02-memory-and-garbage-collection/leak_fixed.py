import tracemalloc
from functools import lru_cache


@lru_cache(maxsize=100)
def build_report(request_id):
    return [request_id] * 1000


tracemalloc.start()
for request_id in range(1, 3001):
    build_report(request_id)
    if request_id % 1000 == 0:
        used, peak = tracemalloc.get_traced_memory()
        print(request_id, round(used / 1_000_000, 1), "MB")
