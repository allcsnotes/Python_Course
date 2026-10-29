import httpx

url = "http://localhost:8153"
good = {"title": "Python Basics", "price": 1499}
text = {"title": "Pydantic", "price": "free"}
empty = {"title": "Oops"}

for body in (good, text, empty):
    r = httpx.post(url + "/courses", json=body)
    print(r.status_code, r.json())

r = httpx.get(url + "/total")
print(r.status_code, r.text)
