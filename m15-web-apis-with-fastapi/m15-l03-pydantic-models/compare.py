import json

from pydantic import ValidationError

from kinds import CourseData, CourseDict, CourseModel

raw = json.loads('{"title": "Pydantic", "price": "free"}')

as_dict: CourseDict = raw
print("TypedDict:", as_dict["price"])

as_data = CourseData(**raw)
print("dataclass:", as_data.price)

try:
    CourseModel(**raw)
except ValidationError as err:
    print("BaseModel:", err.error_count(), "error")
