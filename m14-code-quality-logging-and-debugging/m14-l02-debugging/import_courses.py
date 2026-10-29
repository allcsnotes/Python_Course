import sys

path = sys.argv[1]
start, end = int(sys.argv[2]), int(sys.argv[3])
with open(path) as file:
    titles = file.read().splitlines()[start - 1 : end]

for title in titles:
    if title.strip() == "":
        print("error: a title is blank")
        sys.exit(1)
print(f"ok: {len(titles)} titles")
