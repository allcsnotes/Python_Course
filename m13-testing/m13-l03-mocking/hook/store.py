import httpx

SERVICE = "http://127.0.0.1:8133"


def fetch_price(course_id):
    url = f"{SERVICE}/courses/{course_id}"
    reply = httpx.get(url, timeout=2)
    reply.raise_for_status()
    return reply.json()["price"]


def price_with_gst(course_id):
    return fetch_price(course_id) * 118 // 100
