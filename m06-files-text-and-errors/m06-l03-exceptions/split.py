text = input("People: ")
try:
    people = int(text)
    print("Each pays:", 1000 / people)
except ValueError:
    print("Please type digits only.")
