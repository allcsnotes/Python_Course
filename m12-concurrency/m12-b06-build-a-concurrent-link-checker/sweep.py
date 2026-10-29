import time

import aio
import threaded
from core import LINKS

print("workers  threads  async")
for workers in [1, 2, 4, 8, 12]:
    times = []
    for run in (threaded.run, aio.run):
        began = time.perf_counter()
        run(LINKS, workers)
        times.append(time.perf_counter() - began)
    print(f"{workers:>7}  {times[0]:>6.1f}s  {times[1]:>4.1f}s")
