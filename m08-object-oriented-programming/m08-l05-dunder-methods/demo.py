from course import Course

basics = Course("Python Basics", 499, ["Intro", "Loops"])
loops = Course("Loops Deep Dive", 299, ["while", "for"])
twin = Course("Python Basics", 499, ["Intro", "Loops"])

print(basics)
print([basics, loops])
print(basics == twin, len({basics, twin}))
print(len(basics), basics[0], "Loops" in basics)
print(min(basics, loops))
