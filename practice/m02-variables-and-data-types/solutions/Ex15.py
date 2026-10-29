# Exercise 15 - Fix the broken yes/no code (all four repaired)
is_enrolled = True            # was: true
has_paid = False

price = 499                   # was: 499 = price
print("Price is 499?", price == 499)

answer = "False"              # typed text, as input() would give it
has_certificate = answer == "True"   # a comparison makes a real boolean
print(has_certificate)

seats = 0                     # was: None, then seats + 1
print(seats + 1)
