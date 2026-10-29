import os

import jwt
from fastapi import Header, HTTPException

SECRET = os.environ.get("JWT_SECRET", "demo-secret-not-real-0123456789abcdef")


def make_token(student_id: int) -> str:
    return jwt.encode({"sub": str(student_id)}, SECRET, "HS256")


def current_student(authorization: str = Header(default="")) -> int:
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(401, "missing token")
    try:
        return int(jwt.decode(token, SECRET, ["HS256"])["sub"])
    except jwt.PyJWTError:
        raise HTTPException(401, "invalid token") from None
