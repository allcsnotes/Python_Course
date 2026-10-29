import json

student = {
    "name": "Lukas",
    "courses": 3,
    "rating": 4.5,
    "active": True,
    "coupon": None,
    "tags": ["python", "csv"],
}
print(json.dumps(student))
