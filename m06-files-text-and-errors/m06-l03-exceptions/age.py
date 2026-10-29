text = input("Age: ")
try:
    age = int(text)
    print("Next year:", age + 1)
except ValueError:
    print("Please type digits only.")
print("Thanks!")
