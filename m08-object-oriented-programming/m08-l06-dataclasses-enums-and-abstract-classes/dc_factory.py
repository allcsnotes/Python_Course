from dataclasses import dataclass, field


@dataclass
class Course:
    title: str
    lessons: list = field(default_factory=list)


python = Course("Python")
sql = Course("SQL")
python.lessons.append("Variables")
print(python)
print(sql)
