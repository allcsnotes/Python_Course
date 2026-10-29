# Gotcha 10 - the GIL (the same code as lesson one of this module)
import sys
import time
from concurrent.futures import ThreadPoolExecutor


def count(n):
    while n:
        n -= 1


def timed(workers, total=120_000_000):
    start = time.perf_counter()
    with ThreadPoolExecutor(workers) as pool:
        for _ in range(workers):
            pool.submit(count, total // workers)
    return time.perf_counter() - start


print("GIL on:", sys._is_gil_enabled())
print(f"1 worker:  {timed(1):.2f} s")
print(f"4 workers: {timed(4):.2f} s")
