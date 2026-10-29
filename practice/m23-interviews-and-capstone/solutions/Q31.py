# Q31 - FastAPI: pydantic validation, Depends and overriding a dependency in tests
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


class EnrollIn(BaseModel):
    student: str = Field(min_length=2)
    course_id: int = Field(gt=0)


def get_db():
    return {"name": "real database"}


Db = Annotated[dict, Depends(get_db)]


@app.post("/enrollments", status_code=201)
def enroll(body: EnrollIn, db: Db):
    return {"db": db["name"], "student": body.student, "course_id": body.course_id}


client = TestClient(app)

ok = client.post("/enrollments", json={"student": "Asha", "course_id": 1})
print(ok.status_code, ok.json())

bad = client.post("/enrollments", json={"student": "A", "course_id": 0})
print(bad.status_code)
for problem in bad.json()["detail"]:
    print(" ", problem["loc"], "->", problem["msg"])

app.dependency_overrides[get_db] = lambda: {"name": "fake test database"}
print(client.post("/enrollments", json={"student": "Lukas", "course_id": 2}).json())
