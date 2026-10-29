from locust import HttpUser, between, task


class Visitor(HttpUser):
    wait_time = between(0.5, 1.5)

    def on_start(self):
        reply = self.client.post(
            "/auth/login",
            data={
                "username": "meera@example.com",
                "password": "meera-demo-pass",
            },
            name="/auth/login",
        )
        token = reply.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {token}"}

    @task(6)
    def list_courses(self):
        self.client.get("/courses", name="/courses")

    @task(3)
    def one_course(self):
        self.client.get("/courses/12", name="/courses/{id}")

    @task(1)
    def dashboard(self):
        self.client.get(
            "/me/dashboard",
            headers=self.headers,
            name="/me/dashboard",
        )
