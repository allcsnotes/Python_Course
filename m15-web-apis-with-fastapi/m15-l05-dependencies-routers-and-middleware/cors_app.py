from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://allcsvideos.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["x-api-key"],
)


@app.get("/courses")
def list_courses():
    return [{"id": 1, "title": "Python Basics"}]
