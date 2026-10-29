import httpx

BASE = "http://localhost:8659"
COURSES = [
    ("Python Basics", 499, "beginner"),
    ("SQL in Two Weeks", 599, "beginner"),
    ("Git and GitHub", 299, "beginner"),
    ("Docker for Developers", 899, "intermediate"),
    ("FastAPI in Practice", 999, "intermediate"),
    ("Async Python", 1299, "advanced"),
]
LESSONS = ["Welcome", "Setup", "First steps"]

for title, price, level in COURSES:
    body = {"title": title, "price": price, "level": level}
    course = httpx.post(f"{BASE}/courses", json=body).json()
    for i, name in enumerate(LESSONS, start=1):
        lesson = {"title": name, "position": i}
        url = f"{BASE}/courses/{course['id']}/lessons"
        httpx.post(url, json=lesson)
    print(course["id"], title)
