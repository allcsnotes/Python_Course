import time
from concurrent.futures import ProcessPoolExecutor


def count(n):
    while n > 0:
        n -= 1


def run(workers, n):
    start = time.perf_counter()
    with ProcessPoolExecutor(workers) as pool:
        list(pool.map(count, [n] * workers))
    return time.perf_counter() - start


if __name__ == "__main__":
    print(f"one process:    {run(1, 300_000_000):.2f} s")
    print(f"four processes: {run(4, 75_000_000):.2f} s")
