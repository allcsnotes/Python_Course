import hashlib


def fingerprint(password):
    return hashlib.sha256(password.encode()).hexdigest()
