import time

from app.models import Student
from app.security import hash_password
from app.tokens import make_access_token


def bearer(token):
    return {"Authorization": f"Bearer {token}"}


def make_student(session):
    student = Student(
        name="Lukas",
        email="lukas@example.com",
        password_hash=hash_password("lukas-demo-password"),
    )
    session.add(student)
    session.flush()
    return student


def test_login_gives_a_token_that_works(client, session):
    make_student(session)
    form = {
        "username": "lukas@example.com",
        "password": "lukas-demo-password",
    }
    reply = client.post("/auth/login", data=form)
    token = reply.json()["access_token"]
    reply = client.get("/me", headers=bearer(token))
    assert reply.status_code == 200
    assert reply.json()["name"] == "Lukas"


def test_wrong_password_is_refused(client, session):
    make_student(session)
    form = {
        "username": "lukas@example.com",
        "password": "nope-nope-nope",
    }
    reply = client.post("/auth/login", data=form)
    assert reply.status_code == 401


def test_tampered_token_is_refused(client, session):
    student = make_student(session)
    token = make_access_token(student.id)
    head, body, signature = token.split(".")
    spoiled = body[:-2] + "xx"
    forged = ".".join([head, spoiled, signature])
    reply = client.get("/me", headers=bearer(forged))
    assert reply.status_code == 401


def test_expired_token_is_refused(client, session):
    student = make_student(session)
    before = time.time() - 3600
    token = make_access_token(student.id, now=before)
    reply = client.get("/me", headers=bearer(token))
    assert reply.json()["detail"] == "Token expired"
