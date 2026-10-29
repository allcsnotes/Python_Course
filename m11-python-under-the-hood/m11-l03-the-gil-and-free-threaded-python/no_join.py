import threading
import time


def count(n):
    while n > 0:
        n -= 1


def run(threads, n):
    start = time.perf_counter()
    workers = [threading.Thread(target=count, args=(n,))
               for _ in range(threads)]
    for w in workers:
        w.start()
    return time.perf_counter() - start


print(f"one thread:   {run(1, 300_000_000):.2f} s")
print(f"four threads: {run(4, 75_000_000):.2f} s")
