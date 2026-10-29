from dataclasses import dataclass, field


class CourseFullError(Exception):
    pass


@dataclass
class Course:
    title: str
    seats: int
    students: list[str] = field(default_factory=list)

    def enroll(self, name):
        if name in self.students:
            raise ValueError(f"{name} is already enrolled")
        if len(self.students) >= self.seats:
            raise CourseFullError(f"{self.title} is full")
        self.students.append(name)

    def seats_left(self):
        return self.seats - len(self.students)
