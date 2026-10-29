# Exercise 11 - A receipt for Priya
student = "Priya"
course = "Python Basics"
price = 1499
tax = price * 0.18
total = price + tax

print("=" * 30)
print(f"{'RECEIPT':^30}")
print("=" * 30)
print(f"Student: {student}")
print(f"{course:<20}{price:>10,.2f}")
print(f"{'GST 18%':<20}{tax:>10,.2f}")
print(f"{'Total':<20}{total:>10,.2f}")
print("=" * 30)
