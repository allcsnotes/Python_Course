import os

import jwt

SECRET = os.environ["SECRET_KEY"]
ALG = "HS256"
payload = {"sub": 1}
token = jwt.encode(payload, SECRET, algorithm=ALG)
jwt.decode(token, SECRET, algorithms=[ALG])
