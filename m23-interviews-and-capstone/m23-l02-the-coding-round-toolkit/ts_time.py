import time
from two_sum import two_sum, two_sum_slow

nums = list(range(5000))
for f in (two_sum_slow, two_sum):
    times = []
    for _ in range(3):
        t0 = time.perf_counter()
        f(nums, -1)
        times.append(time.perf_counter() - t0)
    print(f.__name__, round(min(times) * 1000, 2), "ms")
