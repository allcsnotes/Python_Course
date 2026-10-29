import re

found = re.search(r"ORD-\d{4}-\d{4}", "no order here")
print(found)
print(found.group())
