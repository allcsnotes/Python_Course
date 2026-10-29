# Exercise 08 - Many answers from one function
def summarise(marks):
    return min(marks), max(marks), round(sum(marks) / len(marks), 1)


marks = [72, 95, 88, 61, 79]
names = ["Asha", "Lukas", "Priya"]
scores = [92, 78, 85]

lowest, highest, average = summarise(marks)
print("Lowest:", lowest, "Highest:", highest, "Average:", average)
everything = summarise(marks)
print(everything, type(everything))

for name, score in zip(names, scores):
    print(f"{name:<8}{score:>4}")

ranking = sorted(zip(names, scores), key=lambda pair: pair[1], reverse=True)
winner, *others = ranking
print("Winner:", winner)
print("Others:", others)

for place, pair in enumerate(ranking, start=1):
    print(place, pair[0], pair[1])

seat_a = "Asha"
seat_b = "Lukas"
seat_a, seat_b = seat_b, seat_a
print(seat_a, seat_b)
