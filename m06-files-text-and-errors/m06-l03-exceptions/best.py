try:
    file = open("best_score.txt")
except FileNotFoundError:
    best = 0
else:
    best = int(file.read())
    file.close()
print("Best so far:", best)
