import os
import time

import jwt

SECRET = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_SECONDS = int(os.environ.get("ACCESS_SECONDS", "900"))


def make_access_token(student_id, now=None):
    now = int(time.time() if now is None else now)
    payload = {
        "sub": str(student_id),
        "iat": now,
        "exp": now + ACCESS_SECONDS,
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def read_access_token(token):
    payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    return int(payload["sub"])
