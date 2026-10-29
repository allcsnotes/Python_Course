import re

log = "ORD-2026-0042 paid, ORD-2026-0043 refunded"
print(re.findall(r"ORD-\d{4}-\d{4}", log))
mail = "write to lukas@example.com or priya@example.com"
print(re.findall(r"\w+@\w+\.com", mail))
