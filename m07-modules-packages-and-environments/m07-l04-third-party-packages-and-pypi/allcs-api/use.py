from svc import CourseServiceError, fetch_courses

BASE = "http://localhost:8074"
paths = ["/courses", "/missing", "/oops", "/slow"]
for path in paths:
    try:
        courses = fetch_courses(BASE + path)
        print(path, "ok,", len(courses), "courses")
    except CourseServiceError as error:
        print(path, "failed:", error)

try:
    fetch_courses("http://localhost:8099/courses")
except CourseServiceError as error:
    print("port 8099 failed:", error)
