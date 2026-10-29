from app import cache

COURSE = {"title": "Python Basics", "price": 499}


def make_course(client, make_user, headers):
    meera = make_user("Meera", "instructor")
    r = client.post("/courses", json=COURSE, headers=headers(meera))
    return meera, r.json()["id"]


def test_the_second_list_comes_from_redis(client):
    client.get("/courses")
    client.get("/courses")
    assert cache.r.get("stats:misses") == "1"
    assert cache.r.get("stats:hits") == "1"


def test_changing_a_course_forgets_the_cached_list(
    client, make_user, headers
):
    meera, course_id = make_course(client, make_user, headers)
    before = client.get("/courses").json()["items"][0]["price"]
    change = {**COURSE, "price": 399}
    url = f"/courses/{course_id}"
    client.put(url, json=change, headers=headers(meera))
    after = client.get("/courses").json()["items"][0]["price"]
    assert (before, after) == (499, 399)


def test_a_revoked_token_is_refused(client, make_user, login):
    lukas = make_user("Lukas")
    token = login(lukas).json()["access_token"]
    head = {"Authorization": f"Bearer {token}"}
    assert client.get("/me", headers=head).status_code == 200
    client.post("/auth/revoke", headers=head)
    assert client.get("/me", headers=head).status_code == 401
