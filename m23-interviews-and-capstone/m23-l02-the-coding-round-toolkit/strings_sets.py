text = "A man, a plan, a canal: Panama"
clean = "".join(c.lower() for c in text if c.isalnum())
print(clean)
print(clean == clean[::-1])
mine = {"Priya", "Asha", "Lukas", "Meera"}
yours = {"Lukas", "Meera", "Rahul"}
both, only = mine & yours, mine - yours
print(sorted(both), sorted(only), len(mine | yours))
print(len(set("hello")), "a-b-c".split("-"), "-".join("abc"))
