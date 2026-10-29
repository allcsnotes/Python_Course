import json

from app.worker import DEAD, redis, send_welcome_email

JOB = {
    "student_id": 1,
    "course_id": 1,
    "name": "Lukas",
    "email": "lukas@example.com",
    "title": "Python Basics",
}


def make_course(client, headers, make_user):
    meera = make_user("Meera", "instructor")
    body = {"title": "Python Basics", "price": 499}
    r = client.post(
        "/courses", json=body, headers=headers(meera)
    )
    return r.json()["id"]


def test_enrolling_sends_one_welcome_email(
    client, make_user, headers, mailbox
):
    lukas = make_user("Lukas")
    course_id = make_course(client, headers, make_user)
    url = f"/courses/{course_id}/enrollments"
    r = client.post(url, headers=headers(lukas))
    assert r.status_code == 201
    assert len(mailbox.sent) == 1
    mail = mailbox.sent[0]
    assert mail["To"] == "lukas@example.com"
    assert mail["Subject"] == "Welcome to Python Basics"


def test_a_second_enrollment_sends_no_second_email(
    client, make_user, headers, mailbox
):
    lukas = make_user("Lukas")
    course_id = make_course(client, headers, make_user)
    url = f"/courses/{course_id}/enrollments"
    client.post(url, headers=headers(lukas))
    r = client.post(url, headers=headers(lukas))
    assert r.status_code == 409
    assert len(mailbox.sent) == 1


def test_enrolling_works_when_the_mail_server_is_down(
    client, make_user, headers, mailbox
):
    mailbox.failures = 99
    lukas = make_user("Lukas")
    course_id = make_course(client, headers, make_user)
    url = f"/courses/{course_id}/enrollments"
    r = client.post(url, headers=headers(lukas))
    assert r.status_code == 201
    assert mailbox.sent == []


def test_a_task_that_fails_twice_still_sends(mailbox):
    mailbox.failures = 2
    send_welcome_email.delay(**JOB)
    assert mailbox.attempts == 3
    assert len(mailbox.sent) == 1
    assert redis.llen(DEAD) == 0


def test_a_task_gives_up_after_three_retries(mailbox):
    mailbox.failures = 99
    send_welcome_email.delay(**JOB)
    assert mailbox.attempts == 4
    assert mailbox.sent == []
    assert redis.llen(DEAD) == 1
    item = json.loads(redis.lindex(DEAD, 0))
    assert item["kwargs"] == JOB


def test_the_same_job_twice_sends_one_email(mailbox):
    send_welcome_email.delay(**JOB)
    send_welcome_email.delay(**JOB)
    assert len(mailbox.sent) == 1


def test_dead_letters_are_for_admins_only(
    client, make_user, headers
):
    lukas = make_user("Lukas")
    assert (
        client.get("/admin/dead-letters").status_code == 401
    )
    r = client.get(
        "/admin/dead-letters", headers=headers(lukas)
    )
    assert r.status_code == 403


def test_an_admin_lists_the_dead_letters(
    client, make_user, headers, mailbox
):
    asha = make_user("Asha", "admin")
    mailbox.failures = 99
    send_welcome_email.delay(**JOB)
    r = client.get(
        "/admin/dead-letters", headers=headers(asha)
    )
    assert r.status_code == 200
    assert [item["kwargs"] for item in r.json()] == [JOB]


def test_replaying_sends_the_email_and_empties_the_list(
    client, make_user, headers, mailbox
):
    asha = make_user("Asha", "admin")
    mailbox.failures = 99
    send_welcome_email.delay(**JOB)
    mailbox.failures = 0
    r = client.post(
        "/admin/dead-letters/replay", headers=headers(asha)
    )
    assert r.json() == {"replayed": 1}
    assert len(mailbox.sent) == 1
    assert redis.llen(DEAD) == 0
