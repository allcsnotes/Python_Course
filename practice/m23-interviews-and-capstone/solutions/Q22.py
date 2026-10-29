# Q22 - Scope: LEGB, global and nonlocal
students = 0

def bad():
    students += 1                   # assignment makes it local to bad()

try:
    bad()
except UnboundLocalError as error:
    print("UnboundLocalError:", error)

def make_counter():
    count = 0
    def step():
        nonlocal count              # rebind the enclosing variable
        count += 1
        return count
    return step

step = make_counter()
print(step(), step(), step())
