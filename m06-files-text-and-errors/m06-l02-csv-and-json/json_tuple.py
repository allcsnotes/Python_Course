import json

point = (3, 4)
text = json.dumps(point)
print(text)

back = json.loads(text)
print(back)
print(back == point)
