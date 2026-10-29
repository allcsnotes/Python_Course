import httpx

print(issubclass(httpx.ConnectError, httpx.HTTPError))
print(issubclass(httpx.ReadTimeout, httpx.TimeoutException))
print(issubclass(httpx.HTTPStatusError, httpx.HTTPError))
