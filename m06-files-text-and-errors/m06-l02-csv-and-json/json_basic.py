import json

expense = {"amount": 250.0, "category": "food", "note": "Lunch"}

text = json.dumps(expense)
print(text)
print(type(text))

back = json.loads(text)
print(back)
print(back == expense)
