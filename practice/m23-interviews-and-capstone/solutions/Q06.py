# Q06 - *args, **kwargs, keyword-only and positional-only
def enroll(student, /, course, *tags, level="beginner", **extra):
    return student, course, tags, level, extra

print(enroll("Asha", "Python"))
print(enroll("Asha", "Python", "video", "live", level="advanced", city="Pune"))

args = ("Lukas", "SQL")
kwargs = {"level": "intermediate"}
print(enroll(*args, **kwargs))       # unpack a tuple and a dict into a call

try:
    enroll(student="Asha", course="Python")
except TypeError as error:
    print("TypeError:", error)
