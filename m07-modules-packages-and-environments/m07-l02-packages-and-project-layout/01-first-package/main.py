import allcsvideos.courses
from allcsvideos.billing import total

print(allcsvideos.courses.price_of("Web Dev"))
print(total(["Python Basics", "Web Dev"]))
