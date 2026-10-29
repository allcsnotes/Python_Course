import copy

batches = [["Lukas", "Priya"], ["Asha"]]
backup = copy.deepcopy(batches)
backup[0].append("Meera")
print(batches)
print(backup)
print(batches[0] is backup[0])
