# Exercise 22 - Fix the sharing bugs (all four repaired)
scores = [70, 80]
backup = scores.copy()                      # was: backup = scores
scores.append(95)
print("Scores:", scores, "Backup:", backup)

grid = [[0] * 3 for row in range(3)]        # was: [[0] * 3] * 3
grid[0][0] = 1
print(grid)


def add_course(course, cart=None):          # was: cart=[]
    if cart is None:
        cart = []
    cart.append(course)
    return cart


print(add_course("Python"))
print(add_course("SQL"))


def top_mark(marks):
    return max(marks)                       # was: marks.sort(); return marks[-1]


marks = [50, 90, 30]
print(top_mark(marks), marks)
