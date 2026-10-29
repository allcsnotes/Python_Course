import hashlib

from argon2 import PasswordHasher
from clock import average

ph = PasswordHasher()
sha = average(lambda: hashlib.sha256(b"pw").hexdigest(), 100_000)
argon = average(lambda: ph.hash("password123"), 20)
print(f"sha256: {sha * 1_000_000:.1f} microseconds")
print(f"argon2: {argon * 1000:.1f} milliseconds")
guesses = 1_000_000
print(f"{guesses:,} guesses: {argon * guesses / 3600:.1f} hours")
