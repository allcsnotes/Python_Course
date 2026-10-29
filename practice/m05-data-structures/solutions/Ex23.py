# Exercise 23 - Shallow and deep copies
import copy

batches = [["Lukas", "Priya"], ["Asha"]]
alias = batches
shallow = batches.copy()
sliced = batches[:]
deep = copy.deepcopy(batches)

batches[0].append("Meera")
batches.append(["Rahul"])

print("batches:", batches)
print("alias  :", alias)
print("shallow:", shallow)
print("sliced :", sliced)
print("deep   :", deep)

print(alias is batches)
print(shallow is batches)
print(shallow[0] is batches[0])
print(deep[0] is batches[0])

course = {"name": "Python", "tags": ["beginner"]}
backup = copy.deepcopy(course)
course["name"] = "Python 2"
course["tags"].append("hot")
print("course:", course)
print("backup:", backup)
