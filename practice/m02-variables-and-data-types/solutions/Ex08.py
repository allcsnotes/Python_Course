# Exercise 08 - The famous decimal surprise
import math
from decimal import Decimal

total = 0.1 + 0.2
print("Sum:", total)
print("Exactly 0.3?", total == 0.3)                    # the broken check
print("Close to 0.3?", math.isclose(total, 0.3))       # fix 1
print("Decimal sum:", Decimal("0.1") + Decimal("0.2")) # fix 2
print("Paise sum:", 10 + 20, "paise")                  # fix 3: whole numbers
