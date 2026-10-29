from urllib.parse import parse_qs, urlparse

import httpx

APP = "http://localhost:8172"


def show(url):
    query = urlparse(url).query
    for name, value in parse_qs(query).items():
        print("  ", name, "=", value[0])


start = f"{APP}/auth/google/login"
one = httpx.get(start, follow_redirects=False)
print("1.", one.status_code, "to Google")
where = one.headers["location"]
show(where)
two = httpx.get(where, follow_redirects=False)
print("2.", two.status_code, "back to our app")
where = two.headers["location"]
show(where)
three = httpx.get(where)
print("3.", three.status_code, "our own tokens")
print("  ", sorted(three.json()))
