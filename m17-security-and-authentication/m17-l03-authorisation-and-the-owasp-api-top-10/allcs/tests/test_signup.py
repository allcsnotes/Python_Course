def test_sign_up_cannot_choose_a_role(client):
    body = {
        "name": "attacker",
        "email": "attacker@example.com",
        "password": "attacker-demo-pass",
        "role": "admin",
    }
    r = client.post("/students", json=body)
    assert r.status_code == 422
