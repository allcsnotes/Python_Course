from app.domain import CourseNotFound, DuplicateTitle
from app.models import Course, CourseIn, Level


class CourseStore:
    def __init__(self) -> None:
        self.courses: dict[int, Course] = {}
        self.next_id = 1

    def find_all(self, level: Level | None = None) -> list[Course]:
        found = list(self.courses.values())
        if level is not None:
            found = [c for c in found if c.level == level]
        return found

    def get(self, course_id: int) -> Course:
        if course_id not in self.courses:
            raise CourseNotFound(course_id)
        return self.courses[course_id]

    def check_title(self, title: str, own_id: int = 0) -> None:
        for course in self.courses.values():
            same = course.title.lower() == title.lower()
            if same and course.id != own_id:
                raise DuplicateTitle(title)

    def create(self, data: CourseIn) -> Course:
        self.check_title(data.title)
        course = Course(id=self.next_id, **data.model_dump())
        self.courses[course.id] = course
        self.next_id += 1
        return course

    def replace(self, course_id: int, data: CourseIn) -> Course:
        self.get(course_id)
        self.check_title(data.title, course_id)
        course = Course(id=course_id, **data.model_dump())
        self.courses[course_id] = course
        return course

    def delete(self, course_id: int) -> None:
        self.get(course_id)
        del self.courses[course_id]
