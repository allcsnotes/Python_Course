lessons = ["Intro", "Loops", "Functions"]
walker = iter(lessons)

for lesson in walker:
    print(lesson)
print("--- again ---")
for lesson in walker:
    print(lesson)
