import sys

import httpx

base, password, tries = sys.argv[1], sys.argv[2], int(sys.argv[3])
for n in range(1, tries + 1):
    form = {"username": "lukas@example.com", "password": password.format(n=n)}
    reply = httpx.post(base + "/auth/login", data=form)
    print(f"try {n}: {reply.status_code}")
