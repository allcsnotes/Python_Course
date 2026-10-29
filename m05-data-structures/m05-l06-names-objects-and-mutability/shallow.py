batches = [["Lukas", "Priya"], ["Asha"]]
backup = batches.copy()
backup[0].append("Meera")
print(batches)
print(backup)
print(batches is backup)
print(batches[0] is backup[0])
