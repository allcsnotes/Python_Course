# Q33 - def or async def for an endpoint? Measured against a real server.
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import httpx

PORT = 23743
server = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "Q33_server:app", "--port", str(PORT), "--log-level", "error"]
)
try:
    for _ in range(50):             # wait until the server answers
        try:
            httpx.get(f"http://127.0.0.1:{PORT}/async-correct")
            break
        except httpx.ConnectError:
            time.sleep(0.1)

    def burst(path):
        start = time.perf_counter()
        with ThreadPoolExecutor(10) as pool:
            list(pool.map(lambda _: httpx.get(f"http://127.0.0.1:{PORT}{path}"), range(10)))
        return time.perf_counter() - start

    for path in ("/sync-sleep", "/async-blocking", "/async-correct"):
        print(f"10 parallel requests to {path:<16}{burst(path):.2f}s")
finally:
    server.terminate()
    server.wait()
