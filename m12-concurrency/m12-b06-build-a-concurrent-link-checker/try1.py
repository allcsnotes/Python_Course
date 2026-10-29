import time

import httpx

from core import BASE, OPTIONS, from_error, from_response

client = httpx.Client(**OPTIONS)
for path in ["/course/sql", "/old/sql", "/gone/rust-course"]:
    url = BASE + path
    start = time.perf_counter()
    response = client.get(url)
    result = from_response(url, response, start)
    print(result.kind, result.status, result.ms)

url = "http://localhost:8627/up"
start = time.perf_counter()
try:
    client.get(url)
except httpx.HTTPError as error:
    result = from_error(url, error, start)
    print(result.kind, result.status, result.ms)
