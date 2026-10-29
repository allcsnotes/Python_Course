def test_notes_belong_to_their_owner(
    client, auth, add_lesson
):
    lesson_id = add_lesson(
        "A", "Caching", "A cache keeps data."
    )
    lukas, priya = auth("Lukas"), auth("Priya")
    body = {
        "lesson_id": lesson_id,
        "body": "TTL = time to live",
    }
    assert (
        client.post(
            "/notes", json=body, headers=lukas
        ).status_code
        == 201
    )
    assert (
        len(client.get("/notes", headers=lukas).json()) == 1
    )
    assert client.get("/notes", headers=priya).json() == []


def test_note_for_a_missing_lesson_is_404(client, auth):
    body = {"lesson_id": 999, "body": "hello"}
    response = client.post(
        "/notes", json=body, headers=auth()
    )
    assert response.status_code == 404


def test_marking_done_twice_counts_once(
    client, auth, add_lesson
):
    first = add_lesson(
        "A", "One", "Some notes for lesson one."
    )
    add_lesson("B", "Two", "Some notes for lesson two.")
    headers = auth()
    client.post(f"/progress/{first}", headers=headers)
    again = client.post(
        f"/progress/{first}", headers=headers
    )
    assert again.json() == {
        "done": 1,
        "total": 2,
        "percent": 50,
    }
    assert (
        client.get("/progress", headers=headers).json()[
            "done"
        ]
        == 1
    )


def test_progress_with_no_lessons_is_zero_percent(
    client, auth
):
    body = client.get("/progress", headers=auth()).json()
    assert body == {"done": 0, "total": 0, "percent": 0}
