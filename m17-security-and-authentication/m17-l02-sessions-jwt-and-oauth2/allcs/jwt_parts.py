import base64
import json
import os
import time

import jwt

SECRET = os.environ["SECRET_KEY"]
payload = {"sub": "1", "exp": int(time.time()) + 900}
token = jwt.encode(payload, SECRET, algorithm="HS256")
print(token)
head, body, signature = token.split(".")


def unpack(part):
    padded = part + "=" * (-len(part) % 4)
    data = base64.urlsafe_b64decode(padded)
    return json.loads(data)


print(unpack(head))
print(unpack(body))
print(len(signature), "characters of signature")
