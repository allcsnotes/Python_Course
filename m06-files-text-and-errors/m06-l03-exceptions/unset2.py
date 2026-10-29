text = input("Age: ")
try:
    age = int(text)
except ValueError:
    print("Please type digits only.")
else:
    print("Next year:", age + 1)
