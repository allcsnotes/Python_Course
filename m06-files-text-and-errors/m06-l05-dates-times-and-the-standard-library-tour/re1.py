import re

text = "Order ORD-2026-0042 shipped to lukas@example.com"
found = re.search(r"ORD-\d{4}-\d{4}", text)
print(found)
print(found.group())
