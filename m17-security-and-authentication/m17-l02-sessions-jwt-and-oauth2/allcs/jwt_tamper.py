import json
import os
import time
from base64 import urlsafe_b64encode as b64

import jwt

SECRET = os.environ["SECRET_KEY"]
good = jwt.encode(
    {"sub": "1", "exp": int(time.time()) + 900},
    SECRET,
    algorithm="HS256",
)
first = jwt.decode(good, SECRET, algorithms=["HS256"])
print(first["sub"])
head, body, signature = good.split(".")
fake = {"sub": "2", "exp": 9999999999}
raw = json.dumps(fake).encode()
fake_body = b64(raw).decode().rstrip("=")
forged = ".".join([head, fake_body, signature])
try:
    jwt.decode(forged, SECRET, algorithms=["HS256"])
except jwt.InvalidTokenError as err:
    print(type(err).__name__, "-", err)
