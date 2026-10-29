from argon2 import PasswordHasher

ph = PasswordHasher()
stored = ph.hash("password123")

print(ph.verify(stored, "password123"))
print(ph.verify(stored, "password124"))
print("done")
