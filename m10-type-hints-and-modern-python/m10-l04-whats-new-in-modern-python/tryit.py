from html import escape
from string.templatelib import Interpolation

words = iter(["go", "sql", "stop", "rust"])
while (word := next(words)) != "stop":
    print(word)
lines = ["x", " ", "y "]
print([t for line in lines if (t := line.strip())])
try:
    raise ExceptionGroup("two", [ValueError("a"), KeyError("b")])
except* ValueError as group:
    print(len(group.exceptions))
except* KeyError as group:
    print(len(group.exceptions))
plan = {"name": "yearly"}
print(f"Plan: {plan["name"]}")
name = "<i>Asha</i>"
parts = [escape(i.value) if isinstance(i, Interpolation) else i for i in t"<p>{name}</p>"]
print("".join(parts))
