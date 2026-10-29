import time

for run in range(5):
    start = time.perf_counter()
    sum(range(100000))
    elapsed = time.perf_counter() - start
    print(f"run {run + 1}: {elapsed * 1000:.3f} ms")
