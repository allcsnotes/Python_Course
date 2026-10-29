import sys
import time

import httpx

url, count = sys.argv[1], int(sys.argv[2])
ok, failed, seen = 0, 0, {}
for _ in range(count):
    try:
        reply = httpx.get(url + "/version", timeout=1)
        reply.raise_for_status()
        version = reply.json()["version"]
        seen[version] = seen.get(version, 0) + 1
        ok += 1
    except httpx.HTTPError:
        failed += 1
    time.sleep(0.1)
print("ok", ok, "failed", failed, "versions", seen)
