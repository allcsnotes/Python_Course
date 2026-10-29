import re

a = "Payment failed for order 8841"
b = "Payment failed for order 1042"
print(re.sub(r"\d+", "#", a))
print(re.sub(r"\d+", "#", b))
