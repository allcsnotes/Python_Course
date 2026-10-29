# Q18 - Storing passwords: hash, salt, slow on purpose
import hashlib
import time

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

password = "correct horse battery staple"

print("sha256 is fast and unsalted:", hashlib.sha256(password.encode()).hexdigest()[:16], "...")
print("same input, same hash      :", hashlib.sha256(password.encode()).hexdigest()
      == hashlib.sha256(password.encode()).hexdigest())

ph = PasswordHasher()
first, second = ph.hash(password), ph.hash(password)
print("argon2 starts with         :", first.split("$")[1], "|", first.split("$")[2])
print("same password, two hashes  :", first != second)   # a random salt each time

print("right password verifies    :", ph.verify(first, password))
try:
    ph.verify(first, "wrong guess")
except VerifyMismatchError:
    print("wrong password             : VerifyMismatchError")

start = time.perf_counter()
ph.hash(password)
print("one hash took a noticeable time:", time.perf_counter() - start > 0.005)
