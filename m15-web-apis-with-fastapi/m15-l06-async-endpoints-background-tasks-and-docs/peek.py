import httpx

spec = httpx.get("http://localhost:8156/openapi.json").json()
print(spec["info"]["title"], spec["info"]["version"])
for path, methods in spec["paths"].items():
    for method, op in methods.items():
        print(method.upper(), path, "-", op["summary"])
print(list(spec["components"]["schemas"]))
