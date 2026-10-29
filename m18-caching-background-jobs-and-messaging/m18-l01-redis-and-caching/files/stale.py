import time

import httpx
from client import BASE, LIST, login


def price():
    first = httpx.get(LIST).json()["items"][0]
    return first["title"], first["price"]


meera = login("meera@example.com", "meera-demo-pass")
print("before ", *price())
change = {"title": "Python Basics", "price": 399}
r = httpx.put(f"{BASE}/courses/1", json=change, headers=meera)
print("update ", r.status_code)
print("after  ", *price())
time.sleep(4)
print("4s late", *price())
