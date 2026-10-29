titles = ("Python Basics", "SQL Basics", "Git Basics")
prices = (1499, 999)
for title, price in zip(titles, prices):
    print(f"{title}: Rs {price}")
