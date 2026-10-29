from concurrent.futures import ThreadPoolExecutor
from pages import fetch

with ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(fetch, n) for n in (1, 13, 3)]
    for future in futures:
        try:
            print(future.result())
        except ValueError as error:
            print("failed:", error)
