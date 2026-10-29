import hashlib


def fingerprint(password):
    data = password.encode()
    return hashlib.sha256(data).hexdigest()


print(fingerprint("password123")[:32])
print(fingerprint("password123")[:32])
print(fingerprint("Password123")[:32])
