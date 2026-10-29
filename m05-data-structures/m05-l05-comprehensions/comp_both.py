titles = ["python", "sql", "git", "docker"]
long_names = [
    title.upper()
    for title in titles
    if len(title) > 3
]
print(long_names)
