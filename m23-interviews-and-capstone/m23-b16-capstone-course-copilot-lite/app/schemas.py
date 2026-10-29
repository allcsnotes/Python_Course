from pydantic import BaseModel, Field


class Register(BaseModel):
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+$")
    name: str = Field(min_length=2, max_length=60)
    password: str = Field(min_length=10)


class UserOut(BaseModel):
    id: int
    email: str
    name: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Hit(BaseModel):
    lesson_id: int
    code: str
    title: str
    snippet: str
    rank: float


class SearchOut(BaseModel):
    query: str
    cache: str
    results: list[Hit]


class LessonEdit(BaseModel):
    notes: str = Field(min_length=20)


class NoteIn(BaseModel):
    lesson_id: int
    body: str = Field(min_length=1, max_length=500)


class NoteOut(BaseModel):
    id: int
    lesson_id: int
    body: str


class ProgressOut(BaseModel):
    done: int
    total: int
    percent: int
