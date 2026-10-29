from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
current_user = None


@app.post("/login")
def login(name: str):
    global current_user
    current_user = name
    return {"hello": name}


@app.get("/me")
def me():
    return {"you_are": current_user}


lukas = TestClient(app)
priya = TestClient(app)
lukas.post("/login", params={"name": "Lukas"})
priya.post("/login", params={"name": "Priya"})
print(lukas.get("/me").json())
