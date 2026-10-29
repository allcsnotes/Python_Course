with open("notes.txt", "w") as file:
    print(file.closed)
    file.write("Lukas joined the course\n")
print(file.closed)
