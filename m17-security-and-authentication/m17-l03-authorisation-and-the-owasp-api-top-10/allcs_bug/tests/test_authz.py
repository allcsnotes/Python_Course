from tests.helpers import login_as


def test_student_cannot_read_anothers_enrollments(client, users):
    url = f"/students/{users['priya'].id}/enrollments"
    r = client.get(url, headers=login_as(users["lukas"]))
    assert r.status_code == 404


def test_student_reads_own_enrollments(client, users):
    url = f"/students/{users['priya'].id}/enrollments"
    r = client.get(url, headers=login_as(users["priya"]))
    assert r.status_code == 200
    assert r.json()[0]["title"] == "Python Basics"


def test_admin_reads_any_enrollments(client, users):
    url = f"/students/{users['priya'].id}/enrollments"
    r = client.get(url, headers=login_as(users["asha"]))
    assert r.status_code == 200


def test_student_cannot_create_a_course(client, users):
    body = {"title": "Sneaky", "price": 100}
    headers = login_as(users["lukas"])
    r = client.post("/courses", json=body, headers=headers)
    assert r.status_code == 403


def test_no_token_means_401(client, users):
    r = client.get("/students/1/enrollments")
    assert r.status_code == 401
