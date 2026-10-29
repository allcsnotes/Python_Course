import httpx

BASE = "http://localhost:8284"


def pay(key=None):
    headers = {"Idempotency-Key": key} if key else {}
    try:
        httpx.post(BASE + "/charge", headers=headers, timeout=1.0)
    except httpx.TimeoutException:
        print("no answer, asking again")
        httpx.post(BASE + "/charge", headers=headers, timeout=5.0)


def charges():
    count = httpx.get(BASE + "/charges").json()["count"]
    print("charges so far:", count)


pay()
charges()
pay("order-17")
charges()
