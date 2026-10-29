from datetime import date

today = date(2026, 10, 25)  # fixed so the output repeats; use date.today() for real
birthday = date(today.year, 3, 14)  # Asha's birthday: 14 March
if birthday < today:
    birthday = date(today.year + 1, 3, 14)  # already passed this year: use next year

gap = birthday - today
print(f"{gap.days} days until my birthday")
print(birthday.strftime("%A, %d %B"))
