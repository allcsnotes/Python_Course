# Exercise 10 - Fix the broken string code (all five repaired)
name = "Python"
new_name = "J" + name[1:]          # strings cannot be changed, build a new one
print(new_name)

title = "python basics"
title = title.upper()              # keep the result with a label
print(title)

student = "Asha"
print(f"Hello, {student}")         # the f was missing

total = 1768.82
print("Total:", total)             # or: print(f"Total: {total}")

print(name[len(name) - 1])         # last index is len - 1 (or just name[-1])
