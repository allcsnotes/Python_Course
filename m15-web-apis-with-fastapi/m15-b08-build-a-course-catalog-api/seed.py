import httpx

COURSES = [
    ("Python Basics", 499, "beginner"),
    ("SQL in Two Weeks", 399, "beginner"),
    ("Git and GitHub", 299, "beginner"),
    ("Docker for Developers", 599, "intermediate"),
    ("FastAPI in Practice", 699, "intermediate"),
    ("Async Python", 799, "advanced"),
    ("Python Performance", 899, "advanced"),
    ("Linux Essentials", 349, "beginner"),
]

with httpx.Client(base_url="http://localhost:8658") as client:
    for title, price, level in COURSES:
        body = {"title": title, "price": price, "level": level}
        response = client.post("/courses", json=body)
        print(response.status_code, response.json()["title"])
