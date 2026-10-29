from app.store import CourseStore

STORE = CourseStore()


def get_store() -> CourseStore:
    return STORE
