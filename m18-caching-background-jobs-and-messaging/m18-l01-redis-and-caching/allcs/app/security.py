from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

hasher = PasswordHasher()
DUMMY_HASH = hasher.hash("not a real password")


def hash_password(password):
    return hasher.hash(password)


def verify_password(stored_hash, password):
    try:
        return hasher.verify(stored_hash, password)
    except VerifyMismatchError:
        return False


def needs_rehash(stored_hash):
    return hasher.check_needs_rehash(stored_hash)
