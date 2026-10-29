import os

import httpx

SERVICE = "http://127.0.0.1:8133"


class Gateway:
    def charge(self, student, amount):
        body = {"student": student, "amount": amount}
        httpx.post(f"{SERVICE}/charge", json=body, timeout=2)


def fetch_price(course_id):
    url = f"{SERVICE}/courses/{course_id}"
    reply = httpx.get(url, timeout=2)
    reply.raise_for_status()
    return reply.json()["price"]


def gst_percent():
    return int(os.environ.get("GST_PERCENT", "18"))


def price_with_gst(course_id):
    price = fetch_price(course_id)
    return price * (100 + gst_percent()) // 100


def safe_price(course_id):
    try:
        return price_with_gst(course_id)
    except httpx.HTTPError:
        return None


def buy(student, course_id, gateway):
    price = price_with_gst(course_id)
    gateway.charge(student, price)
    return f"{student} bought {course_id} for Rs {price}"
