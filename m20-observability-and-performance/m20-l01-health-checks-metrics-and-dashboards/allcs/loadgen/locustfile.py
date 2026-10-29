import json
import random

from locust import HttpUser, between, task

TOKENS = json.load(open("/mnt/locust/tokens.json"))


class Student(HttpUser):
    wait_time = between(0.3, 1.0)

    @task(10)
    def list_courses(self):
        self.client.get("/courses")

    @task(6)
    def one_course(self):
        n = random.randint(1, 40)
        self.client.get(f"/courses/{n}", name="/courses/[id]")

    @task(3)
    def enroll(self):
        n = random.randint(1, 40)
        token = random.choice(TOKENS)
        self.client.post(
            f"/courses/{n}/enrollments",
            headers={"Authorization": f"Bearer {token}"},
            name="/courses/[id]/enrollments",
        )

    @task(1)
    def slow_report(self):
        self.client.get("/slow?seconds=0.4")
