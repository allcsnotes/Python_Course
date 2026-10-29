from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import engine
from app.security import hash_password

with Session(engine) as s:
    for name in ("meera", "lukas", "priya"):
        s.execute(
            text("update students set password_hash = :h where email = :e"),
            {"h": hash_password(f"{name}-demo-pass"), "e": f"{name}@example.com"},
        )
    s.commit()
print("passwords set")
