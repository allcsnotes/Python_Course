# Exercise 06 - GST in whole paise, and pages
import math

price_paise = 199900                      # Rs 1,999
tax_paise = price_paise * 18 // 100       # whole paise, no float
total_paise = price_paise + tax_paise
rupees, paise = divmod(total_paise, 100)

print("Tax:", tax_paise, "paise")
print("Total:", total_paise, "paise")
print("That is Rs", rupees, "and", paise, "paise")

lessons = 47
per_page = 10
pages = math.ceil(lessons / per_page)
print("Pages needed:", pages)
