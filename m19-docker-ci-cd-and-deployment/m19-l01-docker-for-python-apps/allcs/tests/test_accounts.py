import time

from argon2 import PasswordHasher
from sqlalchemy import select

from app.models import Student
from app.tokens import make_access_token

SIGNUP = {
    "name": "Lukas",
    "email": "lukas@example.com",
    "password": "lukas-demo-pw",
}


def test_sign_up_never_returns_the_password_or_hash(client):
    r = client.post("/students", json=SIGNUP)
    assert r.status_code == 201
    assert "password" not in r.text
    assert r.json()["role"] == "student"


def test_the_password_is_stored_as_an_argon2_hash(client, session):
    client.post("/students", json=SIGNUP)
    stored = session.scalars(select(Student)).one().password_hash
    assert stored.startswith("$argon2id$")
    assert SIGNUP["password"] not in stored


def test_the_same_email_twice_is_409(client):
    client.post("/students", json=SIGNUP)
    r = client.post("/students", json=SIGNUP)
    assert r.status_code == 409
    assert r.json()["error"]["code"] == "duplicate_email"


def test_login_gives_both_tokens(make_user, login):
    r = login(make_user("Lukas"))
    assert r.status_code == 200
    keys = {"access_token", "refresh_token", "token_type"}
    assert set(r.json()) == keys


def test_wrong_password_and_unknown_email_look_the_same(
    client, make_user, login
):
    wrong = login(make_user("Lukas"), "not-the-password")
    form = {"username": "nobody@example.com", "password": "whatever-1"}
    ghost = client.post("/auth/login", data=form)
    assert wrong.status_code == ghost.status_code == 401
    assert wrong.json() == ghost.json()


def test_an_old_student_without_a_password_cannot_log_in(
    make_user, login
):
    old = make_user("Priya", password=None)
    assert login(old).status_code == 401


def test_login_upgrades_an_old_hash(make_user, login, session):
    weak = PasswordHasher(time_cost=1, memory_cost=8192)
    lukas = make_user("Lukas")
    lukas.password_hash = weak.hash("demo-password-1")
    before = lukas.password_hash
    assert login(lukas).status_code == 200
    assert lukas.password_hash != before
    assert "m=65536,t=3" in lukas.password_hash


def test_no_token_is_401(client):
    r = client.get("/me")
    assert r.status_code == 401
    assert r.headers["www-authenticate"] == "Bearer"


def test_a_changed_token_is_401(client, make_user, headers):
    token = headers(make_user("Lukas"))["Authorization"]
    bad = token[:-3] + ("AAA" if token[-3:] != "AAA" else "BBB")
    r = client.get("/me", headers={"Authorization": bad})
    assert r.status_code == 401


def test_an_expired_token_is_401(client, make_user):
    lukas = make_user("Lukas")
    long_ago = int(time.time()) - 3600
    token = make_access_token(lukas.id, now=long_ago)
    r = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401
    assert r.json()["error"]["message"] == "Token expired"


def test_a_refresh_token_is_not_an_access_token(
    client, make_user, login
):
    refresh = login(make_user("Lukas")).json()["refresh_token"]
    r = client.get("/me", headers={"Authorization": f"Bearer {refresh}"})
    assert r.status_code == 401


def test_refresh_gives_new_tokens_and_the_old_one_dies(
    client, make_user, login
):
    old = login(make_user("Lukas")).json()["refresh_token"]
    first = client.post("/auth/refresh", json={"refresh_token": old})
    again = client.post("/auth/refresh", json={"refresh_token": old})
    assert first.status_code == 200
    assert first.json()["refresh_token"] != old
    assert again.status_code == 401


def test_logout_revokes_the_refresh_token(client, make_user, login):
    refresh = login(make_user("Lukas")).json()["refresh_token"]
    body = {"refresh_token": refresh}
    assert client.post("/auth/logout", json=body).status_code == 204
    assert client.post("/auth/refresh", json=body).status_code == 401
