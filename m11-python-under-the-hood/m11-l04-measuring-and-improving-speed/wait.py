import time


def fetch_course():
    time.sleep(0.3)
    return {"title": "Python"}


def handle_request():
    course = fetch_course()
    return course["title"].upper()


for _ in range(3):
    handle_request()
