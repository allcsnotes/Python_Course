def test_live_says_alive(client):
    r = client.get("/health/live")
    assert r.status_code == 200
    assert r.json() == {"status": "alive"}


def test_ready_checks_postgres_and_redis(client):
    r = client.get("/health/ready")
    assert r.status_code == 200
    body = r.json()
    assert body["postgres"] == "ok"
    assert body["redis"] == "ok"


def test_version_reports_the_release(client):
    r = client.get("/version")
    assert r.status_code == 200
    assert r.json()["version"] == "dev"


def test_root_names_the_service(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "allcsvideos"
