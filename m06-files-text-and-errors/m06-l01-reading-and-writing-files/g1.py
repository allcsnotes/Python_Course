with open("chai.txt", "w", encoding="utf-8") as file:
    file.write("Priya paid for chai at the café")

with open("chai.txt", encoding="utf-8") as file:
    print(file.read())
