from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sample import STUDENT

app = FastAPI()


class StudentRow(BaseModel):
    id: int
    name: str
    email: str
    password_hash: str


@app.get("/students/2", response_model=StudentRow)
def read_student():
    return STUDENT


print(TestClient(app).get("/students/2").json())
