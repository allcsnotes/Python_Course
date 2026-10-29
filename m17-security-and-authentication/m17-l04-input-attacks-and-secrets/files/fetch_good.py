from urllib.parse import urlparse

import httpx

ALLOWED = {("localhost", 8174)}


def fetch_thumbnail(url):
    u = urlparse(url)
    if u.scheme not in ("http", "https"):
        raise ValueError("only http and https")
    if (u.hostname, u.port) not in ALLOWED:
        raise ValueError(f"host not allowed: {u.hostname}:{u.port}")
    r = httpx.get(url, timeout=3, follow_redirects=False)
    return r.text[:50]
