import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from pages import fetch

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=8) as pool:
    futures = {pool.submit(fetch, n): n for n in range(1, 9)}
    for future in as_completed(futures):
        gone = time.perf_counter() - start
        n = futures[future]
        print(f"{gone:.1f} s  course {n}: {future.result()}")
