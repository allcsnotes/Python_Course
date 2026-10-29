import os
from datetime import datetime, timedelta, timezone

import jwt

SECRET = os.environ["JWT_SECRET"]


def make_token(student_id, minutes=15):
    expires = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    claims = {"sub": str(student_id), "exp": expires}
    return jwt.encode(claims, SECRET, algorithm="HS256")


def read_access_token(token):
    claims = jwt.decode(token, SECRET, algorithms=["HS256"])
    return int(claims["sub"])
