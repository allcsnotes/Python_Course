import time

import jwt

from app.settings import get_settings

settings = get_settings()
SECRET = settings.secret_key.get_secret_value()
ALGORITHM = "HS256"
ACCESS_SECONDS = settings.access_seconds


def make_access_token(student_id, now=None):
    now = int(time.time() if now is None else now)
    payload = {
        "sub": str(student_id),
        "iat": now,
        "exp": now + ACCESS_SECONDS,
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def read_access_token(token):
    payload = jwt.decode(
        token, SECRET, algorithms=[ALGORITHM]
    )
    return int(payload["sub"])
