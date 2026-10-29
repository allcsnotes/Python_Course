import httpx

from read_page import read_page

r = httpx.get("http://localhost:22280/new/courses?page=1")
rows, nxt = read_page(r.text)
print(len(rows), "courses; first:", rows[0]["title"], rows[0]["price"])
print("next page:", nxt)
