from argon2 import PasswordHasher

hash_ = PasswordHasher().hash("Monsoon-Chai-Lamp-84")
STUDENT = {
    "id": 2,
    "name": "Lukas",
    "email": "lukas@example.com",
    "password_hash": hash_,
}
