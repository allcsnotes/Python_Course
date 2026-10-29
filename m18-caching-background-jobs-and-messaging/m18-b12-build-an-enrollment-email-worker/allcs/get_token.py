import sys

import httpx

form = {"username": sys.argv[1], "password": sys.argv[2]}
r = httpx.post("http://localhost:8692/auth/login", data=form)
print(r.json()[sys.argv[3]])
