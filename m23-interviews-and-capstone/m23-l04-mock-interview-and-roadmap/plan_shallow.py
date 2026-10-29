plan = {"name": "Pro", "courses": ["Python"]}
shallow = dict(plan)
shallow["courses"].append("SQL")
print(plan["courses"])
