import json

students = {1: "Lukas", 2: "Priya"}
text = json.dumps(students)
print(text)

back = json.loads(text)
print(back == students)
print(back[1])
