import re

log = "ORD-2026-0042 paid"
print(re.findall("ORD-\d{4}-\d{4}", log))
