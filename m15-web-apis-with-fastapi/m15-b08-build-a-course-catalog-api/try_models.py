from pydantic import ValidationError

from app.models import CourseIn

course = CourseIn(title="Python Basics", price=499)
print(course)

try:
    CourseIn(title="Py", price=-5, level="expert")
except ValidationError as err:
    print(err.error_count(), "problems")
