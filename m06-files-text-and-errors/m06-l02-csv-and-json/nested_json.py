import json

item = {"note": "Lunch", "tags": ["office", "weekday"]}

back = json.loads(json.dumps(item))
print(back["tags"], type(back["tags"]))
print(back["tags"][0])
