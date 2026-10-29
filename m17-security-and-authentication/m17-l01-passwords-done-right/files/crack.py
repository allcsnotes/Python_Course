from fp import fingerprint

stolen = {
    "Lukas": fingerprint("password123"),
    "Priya": fingerprint("password123"),
    "Meera": fingerprint("Monsoon-Chai-Lamp-84"),
}
common = ["123456", "password", "password123", "qwerty"]
lookup = {fingerprint(word): word for word in common}

for name, stolen_hash in stolen.items():
    print(name, lookup.get(stolen_hash, "not found"))
