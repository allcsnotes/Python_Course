def register(client, **extra):
    body = {
        "email": "lukas@example.com",
        "name": "Lukas",
        "password": "a-long-password",
        **extra,
    }
    return client.post("/auth/register", json=body)


def test_register_never_returns_the_password(client):
    response = register(client)
    assert response.status_code == 201
    assert "password" not in response.text
    assert response.json()["role"] == "student"


def test_same_email_twice_is_409(client):
    register(client)
    assert register(client).status_code == 409


def test_short_password_is_422(client):
    assert (
        register(client, password="short").status_code
        == 422
    )


def login(client, password):
    form = {
        "username": "lukas@example.com",
        "password": password,
    }
    return client.post("/auth/login", data=form)


def test_login_gives_a_token_that_opens_me(client):
    register(client)
    token = login(client, "a-long-password").json()[
        "access_token"
    ]
    me = client.get(
        "/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert me.json()["email"] == "lukas@example.com"


def test_wrong_password_and_unknown_email_look_the_same(
    client,
):
    register(client)
    wrong = login(client, "not-the-password")
    form = {
        "username": "nobody@example.com",
        "password": "x",
    }
    unknown = client.post("/auth/login", data=form)
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.json() == unknown.json()


def test_no_token_and_bad_token_are_401(client):
    assert client.get("/me").status_code == 401
    bad = {"Authorization": "Bearer nonsense"}
    assert client.get("/me", headers=bad).status_code == 401


def test_students_cannot_edit_lessons(
    client, auth, add_lesson
):
    lesson_id = add_lesson(
        "M01-L01", "Hello", "Some notes here."
    )
    response = client.put(
        f"/admin/lessons/{lesson_id}",
        json={"notes": "A brand new set of notes."},
        headers=auth("Lukas", "student"),
    )
    assert response.status_code == 403
