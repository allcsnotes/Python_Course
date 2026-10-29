import time
from concurrent.futures import ThreadPoolExecutor
from pages import fetch

for workers in (1, 2, 4, 8, 16):
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(fetch, range(1, 9)))
    elapsed = time.perf_counter() - start
    print(f"workers={workers}: {elapsed:.2f} s")
