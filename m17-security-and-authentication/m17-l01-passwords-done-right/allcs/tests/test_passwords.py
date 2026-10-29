import pytest
from sqlalchemy import select

from app.models import Student
from app.security import hash_password, verify_password

BODY = {
    "name": "Lukas",
    "email": "lukas@example.com",
    "password": "Monsoon-Chai-Lamp-84",
}


def test_sign_up_never_returns_the_password(client):
    r = client.post("/students", json=BODY)
    assert r.status_code == 201
    assert "password" not in r.text
    assert "argon2" not in r.text


def test_the_database_keeps_only_a_hash(client, session):
    client.post("/students", json=BODY)
    row = session.scalars(select(Student)).one()
    assert row.password_hash.startswith("$argon2id$")
    assert "Monsoon" not in row.password_hash


def test_verify_password():
    stored = hash_password("Monsoon-Chai-Lamp-84")
    assert verify_password(stored, "Monsoon-Chai-Lamp-84")
    assert not verify_password(stored, "monsoon-chai-lamp-84")


@pytest.mark.parametrize(
    "password",
    ["short", "x" * 200],
    ids=["too_short", "too_long"],
)
def test_bad_passwords_are_422(client, password):
    r = client.post("/students", json={**BODY, "password": password})
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "invalid_input"
