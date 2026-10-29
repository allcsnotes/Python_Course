import sys
import time
from concurrent.futures import ThreadPoolExecutor

import httpx

url, count = sys.argv[1], int(sys.argv[2])


def one(_):
    return httpx.get(url, timeout=60).status_code


start = time.perf_counter()
with ThreadPoolExecutor(count) as pool:
    codes = set(pool.map(one, range(count)))
seconds = time.perf_counter() - start
print(f"{count} requests in {seconds:.1f} s, codes {sorted(codes)}")
