import logging

from tests.test_accounts import SIGNUP

COURSE = {"title": "Python Basics", "price": 499}


def test_a_student_cannot_create_a_course(client, make_user, headers):
    lukas = make_user("Lukas")
    r = client.post("/courses", json=COURSE, headers=headers(lukas))
    assert r.status_code == 403


def test_an_instructor_creates_a_course_and_owns_it(
    client, make_user, headers
):
    meera = make_user("Meera", "instructor")
    r = client.post("/courses", json=COURSE, headers=headers(meera))
    assert r.status_code == 201
    assert r.json()["owner_id"] == meera.id


def test_instructors_edit_only_their_own_courses(
    client, make_user, headers
):
    meera = make_user("Meera", "instructor")
    other = make_user("Instructor Two", "instructor")
    asha = make_user("Asha", "admin")
    course = client.post(
        "/courses", json=COURSE, headers=headers(meera)
    ).json()
    url = f"/courses/{course['id']}"
    change = {**COURSE, "price": 399}

    def edit(who):
        r = client.put(url, json=change, headers=headers(who))
        return r.status_code

    assert edit(other) == 403
    assert edit(meera) == 200
    assert edit(asha) == 200


def test_deleting_needs_a_login(client, make_user, headers):
    meera = make_user("Meera", "instructor")
    course = client.post(
        "/courses", json=COURSE, headers=headers(meera)
    ).json()
    r = client.delete(f"/courses/{course['id']}")
    assert r.status_code == 401


def test_students_read_only_their_own_enrollments(
    client, make_user, headers
):
    lukas = make_user("Lukas")
    priya = make_user("Priya")
    asha = make_user("Asha", "admin")
    own = f"/students/{lukas.id}/enrollments"
    mine = client.get(own, headers=headers(lukas))
    other = f"/students/{priya.id}/enrollments"
    theirs = client.get(other, headers=headers(lukas))
    ghost = client.get(
        "/students/999999/enrollments", headers=headers(lukas)
    )
    seen = client.get(other, headers=headers(asha))
    assert mine.status_code == 200
    assert theirs.status_code == ghost.status_code == 404
    assert seen.status_code == 200


def test_enrolling_uses_the_token_not_the_body(
    client, make_user, headers
):
    meera = make_user("Meera", "instructor")
    lukas = make_user("Lukas")
    priya = make_user("Priya")
    course = client.post(
        "/courses", json=COURSE, headers=headers(meera)
    ).json()
    r = client.post(
        f"/courses/{course['id']}/enrollments",
        json={"student_id": priya.id},
        headers=headers(lukas),
    )
    assert r.status_code == 201
    assert r.json()["student_id"] == lukas.id


def test_only_an_admin_creates_instructors(client, make_user, headers):
    lukas = make_user("Lukas")
    asha = make_user("Asha", "admin")
    body = {**SIGNUP, "email": "meera@example.com", "role": "instructor"}
    r = client.post("/admin/students", json=body, headers=headers(lukas))
    assert r.status_code == 403
    r = client.post("/admin/students", json=body, headers=headers(asha))
    assert r.status_code == 201
    assert r.json()["role"] == "instructor"


def test_signing_up_cannot_choose_a_role(client):
    r = client.post("/students", json={**SIGNUP, "role": "admin"})
    assert r.status_code == 422
    assert r.json()["error"]["fields"][0]["field"] == "role"


def test_a_course_cannot_be_given_an_owner(client, make_user, headers):
    meera = make_user("Meera", "instructor")
    body = {**COURSE, "owner_id": 1}
    r = client.post("/courses", json=body, headers=headers(meera))
    assert r.status_code == 422
    assert r.json()["error"]["fields"][0]["field"] == "owner_id"


def test_failed_logins_are_logged_without_the_password(
    client, make_user, caplog
):
    make_user("Lukas")
    caplog.set_level(logging.INFO)
    form = {"username": "lukas@example.com", "password": "guess-9-xyz"}
    for _ in range(3):
        client.post("/auth/login", data=form)
    line = "login failed for lukas@example.com (3 in the last minute)"
    assert line in caplog.text
    assert "guess-9-xyz" not in caplog.text


def test_courses_are_public_and_the_list_is_fast(
    client, make_user, headers, queries
):
    meera = make_user("Meera", "instructor")
    for n in range(6):
        body = {**COURSE, "title": f"Course {n}"}
        client.post("/courses", json=body, headers=headers(meera))
    queries.count = 0
    r = client.get("/courses?limit=6")
    assert r.status_code == 200
    assert queries.count <= 3
