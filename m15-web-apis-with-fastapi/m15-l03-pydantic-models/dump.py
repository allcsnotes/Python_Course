from levels import Course

c = Course(title="Python", price=1499, level="advanced")
print(c.model_dump())
print(c.model_dump(mode="json"))
print(c.model_dump_json())
print(c.model_dump(exclude={"price"}, mode="json"))
