from argon2 import PasswordHasher

ph = PasswordHasher()
first = ph.hash("password123")
second = ph.hash("password123")

print(first[:50] + "...")
print(second[:50] + "...")
print("same?", first == second)
print(first.split("$")[1:4])
print(ph.verify(first, "password123"))
