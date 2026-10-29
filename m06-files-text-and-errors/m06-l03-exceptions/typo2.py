text = input("Age: ")
try:
    age = int(text)
    print("Next year:", agee + 1)
except ValueError:
    print("Please type digits only.")
