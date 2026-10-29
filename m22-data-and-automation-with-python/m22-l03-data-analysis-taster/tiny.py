import pandas as pd

courses = pd.DataFrame({
    "title": ["Python", "SQL", "Git"],
    "price": [2999, 1499, 999],
})
print(courses)
print(courses["price"])
print(courses["price"].sum())
print(courses["price"].to_numpy())
