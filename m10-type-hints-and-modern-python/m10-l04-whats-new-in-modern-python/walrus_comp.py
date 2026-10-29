lines = ["Python", "  ", "SQL ", "", " Git"]
once = [x.strip() for x in lines if x.strip()]
print(once)
twice = [text for x in lines if (text := x.strip())]
print(twice)
