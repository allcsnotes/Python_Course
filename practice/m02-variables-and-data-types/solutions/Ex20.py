# Exercise 20 - Enrolment form for allcsvideos
print("ALLCSVIDEOS ENROLMENT")
name = " ".join(input("Full name: ").split()).title()
email = input("Email: ").strip().lower()
age_text = input("Age: ").strip()
course = input("Course: ").strip()
fee = int(input("Fee in Rs: ").replace(",", ""))
hours = float(input("Hours per week: "))

print("Age is a number:", age_text.isdigit())
age = int(age_text)
gst = fee * 18 // 100
total = fee + gst

print("Saving", end="... ")
print("done")
print("-" * 30)
print(f"{'Name':<8}: {name}")
print(f"{'Email':<8}: {email}")
print(f"{'Age':<8}: {age} (next year {age + 1})")
print(f"{'Course':<8}: {course}")
print(f"{'Hours':<8}: {hours} per week")
print(f"{'Fee':<8}: Rs {fee:>8,}")
print(f"{'GST':<8}: Rs {gst:>8,}")
print(f"{'Total':<8}: Rs {total:>8,}")
print("-" * 30)
