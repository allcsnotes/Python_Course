import time
from concurrent.futures import ThreadPoolExecutor
from pages import fetch

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=8) as pool:
    for title in pool.map(fetch, range(1, 9)):
        print(title)
print(f"{time.perf_counter() - start:.2f} s")
