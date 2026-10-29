import pytest

from app import mailer
from app.worker import send_progress_email
from tests.test_search import ask


def test_edit_saves_then_reindexes_and_clears_the_cache(
    client, auth, add_lesson
):
    lesson_id = add_lesson(
        "A", "Caching", "A cache keeps data."
    )
    student, admin = auth("Lukas"), auth("Meera", "admin")
    first = ask(client, student, "keeps")
    again = ask(client, student, "keeps")
    assert first.headers["x-cache"] == "MISS"
    assert again.headers["x-cache"] == "HIT"
    edit = client.put(
        f"/admin/lessons/{lesson_id}",
        json={
            "notes": "Cache aside reads the cache first."
        },
        headers=admin,
    )
    assert edit.status_code == 202
    old = ask(client, student, "keeps").json()
    new = ask(client, student, "aside").json()
    assert old["results"] == []
    assert len(new["results"]) == 1


def test_weekly_emails_are_sent_once_per_week(
    client, auth, make_user, mailbox
):
    user_id, _ = make_user("Lukas", "student")
    _, admin_token = make_user("Meera", "admin")
    headers = {"Authorization": f"Bearer {admin_token}"}
    for _ in range(2):
        response = client.post(
            "/admin/weekly-emails", headers=headers
        )
        assert response.status_code == 202
    assert len(mailbox) == 1
    assert mailbox[0]["To"] == "lukas@example.com"
    assert (
        mailbox[0]["Subject"] == "Your week: 0 of 0 lessons"
    )


def test_a_failed_send_can_be_tried_again(
    make_user, monkeypatch
):
    user_id, _ = make_user("Lukas", "student")

    def down(message):
        raise ConnectionRefusedError("mail server is down")

    monkeypatch.setattr(mailer, "send", down)
    with pytest.raises(ConnectionRefusedError):
        send_progress_email(user_id)
    sent = []
    monkeypatch.setattr(mailer, "send", sent.append)
    send_progress_email(user_id)
    assert len(sent) == 1


def test_unknown_user_is_skipped(mailbox):
    send_progress_email(12345)
    assert mailbox == []
