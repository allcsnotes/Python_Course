# Exercise 03 - Fix the broken list code (all five repaired)
scores = [70, 80, 90]
print(scores[2])                 # was scores[3]: only positions 0, 1, 2 exist

names = ["Asha", "Lukas"]
if "Priya" in names:             # was: names.remove("Priya") with no check
    names.remove("Priya")
else:
    print("Priya is not enrolled")
print(names)

marks = [3, 1, 2]
marks.sort()                     # was: result = marks.sort()  (sort returns None)
print(marks)

guests = ["Asha"]
guests = guests + ["Rahul"]      # was: guests + "Rahul"  (list + text)
print(guests)

team = ["Asha"]
team.extend(["Lukas", "Meera"])  # was: team.append("Lukas", "Meera")
print(team)
