from types import SimpleNamespace

from app import worker
from app.models import Course
from app.routers import reports


def test_task_is_a_plain_function(monkeypatch):
    monkeypatch.setattr(worker.time, "sleep", lambda s: None)
    email = "lukas@example.com"
    answer = worker.send_welcome_email(email, "Python")
    assert answer == "sent: Python"


def test_enrol_queues_the_email(
    client, session, make_user, headers, sent
):
    lukas = make_user("Lukas")
    course = Course(title="Python Basics", price=999, level="beginner")
    session.add(course)
    session.flush()
    url = f"/courses/{course.id}/enrollments"
    reply = client.post(url, headers=headers(lukas))
    assert reply.status_code == 201
    assert sent == [("lukas@example.com", "Python Basics")]


def test_report_answers_202_with_a_job_id(
    client, make_user, headers, monkeypatch
):
    asha = make_user("Asha", role="admin")
    fake = SimpleNamespace(id="job-1")
    monkeypatch.setattr(reports.build_report, "delay", lambda: fake)
    reply = client.post("/reports/enrollments", headers=headers(asha))
    assert reply.status_code == 202
    assert reply.json()["job_id"] == "job-1"


def test_students_cannot_start_a_report(client, make_user, headers):
    lukas = make_user("Lukas")
    reply = client.post("/reports/enrollments", headers=headers(lukas))
    assert reply.status_code == 403


def test_retries_until_the_mail_service_works(monkeypatch):
    calls = []

    def flaky(email, course):
        calls.append(email)
        if len(calls) < 3:
            raise ConnectionError("mail service is down")

    monkeypatch.setattr(worker, "talk_to_mail_service", flaky)
    args = ("lukas@example.com", "Python")
    result = worker.send_welcome_email.apply(args=args)
    assert result.get() == "sent: Python"
    assert len(calls) == 3
