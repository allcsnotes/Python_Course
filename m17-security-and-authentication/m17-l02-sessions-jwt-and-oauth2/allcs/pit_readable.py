import base64
import json
import os

import jwt

SECRET = os.environ["SECRET_KEY"]
ALG = "HS256"
payload = {
    "sub": "1",
    "email": "lukas@example.com",
    "password_hash": "$argon2id$v=19$...",
}
token = jwt.encode(payload, SECRET, algorithm=ALG)
body = token.split(".")[1]
padded = body + "=" * (-len(body) % 4)
print(json.loads(base64.urlsafe_b64decode(padded)))
