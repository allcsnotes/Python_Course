class Student:
    done = []

    def __init__(self, name):
        self.name = name


lukas = Student("Lukas")
priya = Student("Priya")
lukas.done.append("lesson 1")
print(priya.done)
print(lukas.done is priya.done)
