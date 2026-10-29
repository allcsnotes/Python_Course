import copy

plan = {"name": "Pro", "courses": ["Python"]}
deep = copy.deepcopy(plan)
deep["courses"].append("SQL")
print(plan["courses"])
print(deep["courses"])
