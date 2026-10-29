from pydantic import BaseModel


class StudentIn(BaseModel):
    name: str
    email: str
    password: str


class StudentOut(BaseModel):
    id: int
    name: str
    email: str
