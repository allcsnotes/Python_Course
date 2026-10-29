password = "lukas2024"
for ch in password:
    if ch.isdigit():
        print("Good: it has a digit")
        break
else:
    print("Add at least one digit")
