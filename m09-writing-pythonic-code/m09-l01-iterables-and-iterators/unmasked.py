lessons = ["Intro", "Loops", "Functions"]

walker = iter(lessons)
while True:
    try:
        lesson = next(walker)
    except StopIteration:
        break
    print(lesson)
