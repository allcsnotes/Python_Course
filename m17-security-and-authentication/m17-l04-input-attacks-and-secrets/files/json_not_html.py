from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/api/course")
def course_json():
    return {"description": "Nice! <script>alert(1)</script>"}


client = TestClient(app)
r = client.get("/api/course")
print(r.headers["content-type"])
print(r.text)
