def dashed(*titles):
    return "-".join(titles)

print(dashed("Python", "SQL", "Git"))
courses = ["Python", "SQL", "Git"]
print(dashed(*courses))
