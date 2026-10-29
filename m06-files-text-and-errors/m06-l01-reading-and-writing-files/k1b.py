score = 42
with open("score.txt", "w", encoding="utf-8") as file:
    file.write(str(score))

with open("score.txt", encoding="utf-8") as file:
    print(file.read())
