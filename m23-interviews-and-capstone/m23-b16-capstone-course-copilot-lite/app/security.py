import time

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.settings import get_settings

hasher = PasswordHasher()
DUMMY = hasher.hash("not a real password")
ALGORITHM = "HS256"


def hash_password(password):
    return hasher.hash(password)


def check_password(stored, password):
    try:
        return hasher.verify(stored, password)
    except VerifyMismatchError:
        return False


def make_token(user_id, role):
    settings = get_settings()
    now = int(time.time())
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": now,
        "exp": now + settings.access_minutes * 60,
    }
    key = settings.secret_key.get_secret_value()
    return jwt.encode(payload, key, algorithm=ALGORITHM)


def read_token(token):
    key = get_settings().secret_key.get_secret_value()
    payload = jwt.decode(token, key, algorithms=[ALGORITHM])
    return int(payload["sub"])
