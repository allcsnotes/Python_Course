class Student:
    def __init__(self, name):
        self.name = name
        self.done = []


lukas = Student("Lukas")
priya = Student("Priya")
lukas.done.append("lesson 1")
print(priya.done)
print(lukas.done)
