lessons = ["intro", "demo 1", "demo 2", "demo 3", "wrap-up"]
for item in lessons:
    if item.startswith("demo"):
        lessons.remove(item)
print(lessons)

lessons = ["intro", "demo 1", "demo 2", "demo 3", "wrap-up"]
kept = [item for item in lessons if not item.startswith("demo")]
print(kept)
