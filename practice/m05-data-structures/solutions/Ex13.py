# Exercise 13 - The nested catalog
catalog = {
    "Python": {"price": 1499, "lessons": 104, "tags": ["beginner", "backend"]},
    "SQL": {"price": 999, "lessons": 30, "tags": ["data"]},
    "Docker": {"price": 799, "lessons": 25, "tags": ["devops"]},
}
print(catalog["Python"]["price"])
print(catalog["Python"]["tags"][0])

catalog["Git"] = {"price": 499, "lessons": 12, "tags": []}
catalog["SQL"]["price"] -= 100
catalog["Python"]["tags"].append("popular")

for slug, info in catalog.items():
    print(f"{slug:<8} Rs {info['price']:>5}  {info['lessons']:>3} lessons  tags={info['tags']}")

total = 0
for info in catalog.values():
    total += info["price"]
print("Whole catalog: Rs", total)

enrolments = [("Asha", "Python"), ("Lukas", "SQL"), ("Priya", "Python"),
              ("Meera", "Git"), ("Rahul", "Python")]
by_course = {}
for student, slug in enrolments:
    if slug not in by_course:
        by_course[slug] = []
    by_course[slug].append(student)
print(by_course)

print(catalog.get("Go", {}).get("price", "not sold"))
