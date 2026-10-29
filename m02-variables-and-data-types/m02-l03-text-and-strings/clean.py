raw_name = "   lukas    WEBER  "
raw_email = " Lukas.Weber@Example.COM "
name = " ".join(raw_name.split()).title()
email = raw_email.strip().lower()
print(f"Welcome, {name}!")
print(email)
print(email.endswith("@example.com"))
