from search_bad import build_sql

for q in ["python", "zzz' OR true --"]:
    print(build_sql(q))
    print()
