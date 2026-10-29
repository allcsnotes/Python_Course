import httpx

r = httpx.get("http://localhost:22280/courses?page=1")
body = r.text.split("<main>")[1]
print(r.status_code)
print(body.split("</div>")[0] + "</div>")
