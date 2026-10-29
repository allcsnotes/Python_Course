import os
import time

import jwt

SECRET = os.environ["SECRET_KEY"]
payload = {"sub": "1", "exp": int(time.time()) + 2}
token = jwt.encode(payload, SECRET, algorithm="HS256")
first = jwt.decode(token, SECRET, algorithms=["HS256"])
print("now:", first["sub"])
time.sleep(3)
try:
    jwt.decode(token, SECRET, algorithms=["HS256"])
except jwt.InvalidTokenError as err:
    print(type(err).__name__, "-", err)
