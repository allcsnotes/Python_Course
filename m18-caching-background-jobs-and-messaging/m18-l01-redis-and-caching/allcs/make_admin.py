from sqlalchemy.orm import Session

from app.db import engine
from app.models import Student
from app.security import hash_password

with Session(engine) as session:
    session.add(
        Student(
            name="Asha",
            email="asha@example.com",
            role="admin",
            password_hash=hash_password("asha-demo-pw"),
        )
    )
    session.commit()
print("admin created: asha@example.com")
