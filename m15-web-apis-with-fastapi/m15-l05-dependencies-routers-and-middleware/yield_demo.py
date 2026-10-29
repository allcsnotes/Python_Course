from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


def get_session():
    print("open session")
    try:
        yield "SESSION"
    finally:
        print("close session")


@app.get("/ping")
def ping(session: str = Depends(get_session)):
    print("handling with", session)
    return {"ok": True}


@app.get("/boom")
def boom(session: str = Depends(get_session)):
    print("about to fail")
    raise RuntimeError("oops")


client = TestClient(app, raise_server_exceptions=False)
print(client.get("/ping").status_code)
print(client.get("/boom").status_code)
