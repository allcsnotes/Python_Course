from argon2 import PasswordHasher

old = PasswordHasher(time_cost=1, memory_cost=8192)
ph = PasswordHasher()

stored = old.hash("password123")
print(stored.split("$")[3])
print(ph.check_needs_rehash(stored))

stored = ph.hash("password123")
print(stored.split("$")[3])
print(ph.check_needs_rehash(stored))
