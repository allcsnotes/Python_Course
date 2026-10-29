from concurrent.futures import ThreadPoolExecutor

import httpx

URL = "http://localhost:8181/count"
with ThreadPoolExecutor(4) as pool:
    replies = pool.map(lambda _: httpx.get(URL).json(), range(8))
    rows = sorted(replies, key=lambda d: d["shared"])
    for data in rows:
        print(data["pid"], data["local_hits"], data["shared"])
