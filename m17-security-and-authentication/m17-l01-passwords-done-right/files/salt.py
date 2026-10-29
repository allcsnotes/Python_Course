import hashlib
import secrets


def salted(password):
    salt = secrets.token_hex(8)
    data = (salt + password).encode()
    return salt, hashlib.sha256(data).hexdigest()


for name in ["Lukas", "Priya"]:
    salt, digest = salted("password123")
    print(name, salt, digest[:16] + "...")
