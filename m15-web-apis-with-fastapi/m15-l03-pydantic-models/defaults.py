from pydantic import BaseModel


class Course(BaseModel):
    title: str
    tags: list[str] = []
    note: str | None = None


a = Course(title="Python")
b = Course(title="Pydantic")
a.tags.append("new")
print(a.tags, b.tags)
print(b.note)
