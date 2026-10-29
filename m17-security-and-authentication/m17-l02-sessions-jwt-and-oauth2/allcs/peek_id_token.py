import os
from urllib.parse import parse_qs, urlparse

import httpx
import jwt

GOOGLE = "http://localhost:8272"
CLIENT_ID = "allcs-demo-client"
secret = os.environ["GOOGLE_CLIENT_SECRET"]
CALLBACK = "http://localhost:8172/auth/google/callback"
query = {
    "client_id": CLIENT_ID,
    "redirect_uri": CALLBACK,
    "state": "x",
}
step = httpx.get(f"{GOOGLE}/authorize", params=query)
where = step.headers["location"]
code = parse_qs(urlparse(where).query)["code"][0]
reply = httpx.post(
    f"{GOOGLE}/token",
    data={
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": secret,
        "redirect_uri": CALLBACK,
    },
).json()
token = reply["id_token"]
claims = jwt.decode(token, options={"verify_signature": False})
for name, value in claims.items():
    print(name, "=", value)
