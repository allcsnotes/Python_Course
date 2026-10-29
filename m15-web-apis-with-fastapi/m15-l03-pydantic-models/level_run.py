from pydantic import ValidationError

from levels import Course

print(Course(title="Python", price=1499))
print(Course(title="Python", price=1499, level="advanced"))

try:
    Course(title="Python", price=1499, level="expert")
except ValidationError as err:
    print(err.errors()[0]["msg"])
