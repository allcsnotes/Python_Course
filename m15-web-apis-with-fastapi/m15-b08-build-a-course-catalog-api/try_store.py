from app.models import CourseIn
from app.store import CourseStore

store = CourseStore()
store.create(CourseIn(title="Python Basics", price=499))
store.create(CourseIn(title="SQL in Two Weeks", price=399))
print(len(store.find_all()))
print(store.get(2).title)
