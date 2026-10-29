import json
import logging

from app.logs import JsonFormatter, request_id


def test_live_and_ready(client):
    assert client.get("/health/live").json() == {
        "status": "alive"
    }
    ready = client.get("/health/ready")
    assert ready.status_code == 200
    assert ready.json() == {
        "status": "ready",
        "postgres": "ok",
        "redis": "ok",
    }


def test_ready_is_503_when_redis_is_down(
    client, monkeypatch
):
    from app import health

    def broken():
        raise ConnectionError("redis is down")

    monkeypatch.setattr(health.redis, "ping", broken)
    response = client.get("/health/ready")
    assert response.status_code == 503
    assert response.json()["redis"] == "down"


def test_metrics_count_requests_by_route(client):
    client.get("/health/live")
    text = client.get("/metrics").text
    assert 'route="/health/live"' in text
    assert "copilot_requests_total" in text


def test_every_response_carries_a_request_id(client):
    sent = client.get(
        "/health/live", headers={"x-request-id": "abc"}
    )
    assert sent.headers["x-request-id"] == "abc"
    made = client.get("/health/live")
    assert len(made.headers["x-request-id"]) == 12


def test_log_lines_are_json_with_the_request_id():
    request_id.set("r-42")
    record = logging.LogRecord(
        "copilot",
        logging.INFO,
        "",
        0,
        "hello %s",
        ("world",),
        None,
    )
    record.lesson_id = 7
    data = json.loads(JsonFormatter().format(record))
    assert data["message"] == "hello world"
    assert data["request_id"] == "r-42"
    assert data["lesson_id"] == 7
