# Q32 - Status codes, and an idempotency key for POST
from fastapi import FastAPI, Header, HTTPException, Response
from fastapi.testclient import TestClient

app = FastAPI()
enrollments = {}                     # id -> record
seen_keys = {}                      # Idempotency-Key -> id


@app.post("/enrollments", status_code=201)
def create(student: str, course_id: int, response: Response,
           idempotency_key: str | None = Header(default=None)):
    if idempotency_key in seen_keys:            # same request again: same answer
        response.status_code = 200
        return enrollments[seen_keys[idempotency_key]]
    for record in enrollments.values():
        if (record["student"], record["course_id"]) == (student, course_id):
            raise HTTPException(409, "already enrolled")
    new_id = len(enrollments) + 1
    enrollments[new_id] = {"id": new_id, "student": student, "course_id": course_id}
    if idempotency_key:
        seen_keys[idempotency_key] = new_id
    return enrollments[new_id]


@app.get("/enrollments/{enrollment_id}")
def read(enrollment_id: int):
    if enrollment_id not in enrollments:
        raise HTTPException(404, "no such enrollment")
    return enrollments[enrollment_id]


client = TestClient(app)
key = {"Idempotency-Key": "abc-123"}
params = {"student": "Asha", "course_id": 1}

print("first  POST :", client.post("/enrollments", params=params, headers=key).status_code)
print("retry  POST :", client.post("/enrollments", params=params, headers=key).status_code)
print("new key POST:", client.post("/enrollments", params=params, headers={"Idempotency-Key": "zzz"}).status_code)
print("GET found   :", client.get("/enrollments/1").status_code)
print("GET missing :", client.get("/enrollments/99").status_code)
print("bad input   :", client.post("/enrollments", params={"student": "Asha", "course_id": "x"}).status_code)
print("enrollments stored:", len(enrollments))
