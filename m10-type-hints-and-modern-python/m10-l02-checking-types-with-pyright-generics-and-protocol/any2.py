import json

raw = '{"title": "Python", "price": 999}'
data = json.loads(raw)
reveal_type(data)
reveal_type(data["price"])
