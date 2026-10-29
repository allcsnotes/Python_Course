import httpx

import servers


def fetch_thumbnail(url):
    r = httpx.get(url, timeout=3)
    return r.text[:50]


logo = "http://localhost:8174/logo.png"
notes = "http://localhost:8274/admin/notes"
servers.start()
print(fetch_thumbnail(logo))
print(fetch_thumbnail(notes))
