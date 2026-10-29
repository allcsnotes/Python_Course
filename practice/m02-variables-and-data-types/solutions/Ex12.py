# Exercise 12 - Clean what people type
raw_name = "   lUKAS     wEBER  "
raw_email = "  Lukas@Mail.COM "
raw_title = "  Python   FOR  Absolute   Beginners "

name = " ".join(raw_name.split()).title()
email = raw_email.strip().lower()
slug = "-".join(raw_title.lower().split())

print("Name:", name)
print("Email:", email)
print("Has an @:", "@" in email)
print("Ends with mail.com:", email.endswith("mail.com"))
print("Slug:", slug)
print(f"Address: allcsvideos.com/courses/{slug}")
print("Slug length:", len(slug))
