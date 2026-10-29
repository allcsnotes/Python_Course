from search_good import search

attacks = [
    "python",
    "zzz' OR true --",
    "zzz' UNION SELECT email FROM students --",
]
for q in attacks:
    print(f"{len(search(q))} found for {q!r}")
