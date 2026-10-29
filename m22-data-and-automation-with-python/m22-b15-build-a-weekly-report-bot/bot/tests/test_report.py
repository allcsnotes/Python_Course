from datetime import date

import httpx
import pytest

from weekly_report import job
from weekly_report.analyse import summarise
from weekly_report.api import ApiDown
from weekly_report.settings import Settings
from weekly_report.weeks import last_monday, week_bounds

MONDAY = date(2026, 10, 19)
IST = "Asia/Kolkata"


def row(student, course, amount, enrolled, refunded=None):
    return {
        "student_id": student,
        "course_id": 1,
        "course": course,
        "amount": amount,
        "enrolled_at": enrolled,
        "refunded_at": refunded,
    }


REFUND = row(
    2,
    "SQL",
    599,
    "2026-10-21T06:00:00+00:00",
    "2026-10-22T06:00:00+00:00",
)
FAKE = {
    "enrollments": [
        row(1, "Python", 499, "2026-10-18T18:45:00+00:00"),
        REFUND,
        row(3, "Python", 499, "2026-10-12T06:00:00+00:00"),
    ],
    "refunds": [REFUND],
}
EMPTY = {"enrollments": [], "refunds": []}


def settings(tmp_path):
    return Settings(
        api_user="bot",
        api_password="pw",
        out_dir=tmp_path,
        wait=0,
    )


def fake_client(data, fail_first=0):
    calls = []
    token = {"access_token": "t"}

    def handler(request):
        if request.url.path == "/auth/login":
            return httpx.Response(200, json=token)
        calls.append(request)
        if len(calls) <= fail_first:
            return httpx.Response(503)
        return httpx.Response(200, json=data)

    transport = httpx.MockTransport(handler)
    return httpx.Client(
        base_url="http://fake", transport=transport
    )


def test_week_starts_at_midnight_in_india():
    start, end = week_bounds(MONDAY, IST)
    assert start.isoformat() == "2026-10-19T00:00:00+05:30"
    assert end.isoformat() == "2026-10-26T00:00:00+05:30"


def test_last_monday():
    assert last_monday(date(2026, 10, 28)) == MONDAY


def test_summary_numbers():
    start, end = week_bounds(MONDAY, IST)
    s = summarise(FAKE, start, end, IST)
    assert (s.enrollments, s.before) == (2, 1)
    assert (s.gross, s.refunded, s.net) == (1098, 599, 499)


def test_empty_week_is_quiet(tmp_path):
    sent = []
    job.run_week(
        settings(tmp_path),
        MONDAY,
        fake_client(EMPTY),
        send=lambda s, m: sent.append(m),
    )
    body = sent[0].get_body().get_content()
    assert body.startswith("A quiet week")
    assert not list(sent[0].iter_attachments())


def test_retry_then_success(tmp_path):
    client = fake_client(FAKE, fail_first=2)
    result = job.run_week(
        settings(tmp_path),
        MONDAY,
        client,
        send=lambda s, m: None,
    )
    assert result == "sent"


def test_gives_up_after_three_tries(tmp_path):
    client = fake_client(FAKE, fail_first=9)
    with pytest.raises(ApiDown):
        job.run_week(settings(tmp_path), MONDAY, client)


def test_second_run_sends_nothing(tmp_path):
    sent = []
    args = (settings(tmp_path), MONDAY, fake_client(FAKE))
    send = lambda s, m: sent.append(m)
    assert job.run_week(*args, send=send) == "sent"
    assert job.run_week(*args, send=send) == "skipped"
    assert len(sent) == 1
