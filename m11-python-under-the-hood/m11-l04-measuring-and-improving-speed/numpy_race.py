import time

import numpy as np

numbers = list(range(1000000))
array = np.arange(1000000)

start = time.perf_counter()
loop_total = 0
for n in numbers:
    loop_total += n * n
loop_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
numpy_total = (array * array).sum()
numpy_ms = (time.perf_counter() - start) * 1000

print(loop_total, numpy_total)
print(f"Python loop: {loop_ms:.1f} ms")
print(f"NumPy:       {numpy_ms:.1f} ms")
print(f"NumPy is {loop_ms / numpy_ms:.0f} times faster")
