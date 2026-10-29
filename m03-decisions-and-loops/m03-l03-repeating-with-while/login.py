attempts = 0
code = ""
while code != "4821" and attempts < 3:
    code = input("Course code: ")
    attempts += 1
if code == "4821":
    print("Welcome in!")
else:
    print("Too many tries.")
