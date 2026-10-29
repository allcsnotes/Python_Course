import sys

import httpx

BASE = "http://localhost:8204"
who, course = sys.argv[1], int(sys.argv[2])
meera = httpx.post(
    BASE + "/auth/login",
    data={"username": "meera@example.com", "password": "meera-demo-pass"},
).json()["access_token"]
student = httpx.post(
    BASE + "/auth/login",
    data={"username": f"{who}@example.com", "password": f"{who}-demo-pass"},
).json()["access_token"]


def seen():
    reply = httpx.get(
        BASE + "/me/dashboard",
        headers={"Authorization": f"Bearer {meera}"},
    )
    return reply.json()[course - 1]["students"]


print("the dashboard says:", seen(), "students")
reply = httpx.post(
    BASE + f"/courses/{course}/enrollments",
    headers={"Authorization": f"Bearer {student}"},
)
print(f"{who} enrolls:", reply.status_code)
print("the dashboard says:", seen(), "students")
