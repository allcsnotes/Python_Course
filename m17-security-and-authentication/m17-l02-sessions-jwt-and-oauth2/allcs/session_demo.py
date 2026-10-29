import secrets

from fastapi import Cookie, FastAPI, HTTPException, Response
from fastapi.testclient import TestClient

app = FastAPI()
SESSIONS = {}


@app.post("/login")
def login(name: str, response: Response):
    session_id = secrets.token_urlsafe(16)
    SESSIONS[session_id] = name
    response.set_cookie("sid", session_id, httponly=True)
    return {"hello": name}


@app.get("/me")
def me(sid: str | None = Cookie(None)):
    name = SESSIONS.get(sid)
    if name is None:
        raise HTTPException(401, "Please log in")
    return {"you_are": name}


lukas = TestClient(app)
priya = TestClient(app)
r = lukas.post("/login", params={"name": "Lukas"})
print(r.headers["set-cookie"])
priya.post("/login", params={"name": "Priya"})
print(lukas.get("/me").json())
SESSIONS.clear()
print(lukas.get("/me").status_code)
