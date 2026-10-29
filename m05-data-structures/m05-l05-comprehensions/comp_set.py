titles = ["python", "sql", "git", "docker", "go", "rust"]
as_list = [len(title) for title in titles]
as_set = {len(title) for title in titles}
print(as_list)
print(as_set)
