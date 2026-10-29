from collections import Counter
from concurrent.futures import ThreadPoolExecutor

import httpx

URL = "http://localhost:8659/courses/1/enrollments"


def enroll(_):
    return httpx.post(URL, json={"student_id": 1}).status_code


with ThreadPoolExecutor(5) as pool:
    codes = list(pool.map(enroll, range(5)))
print(sorted(Counter(codes).items()))
