seats = 12
if seats >= 2:
    discount = 5
elif seats >= 5:
    discount = 15
elif seats >= 10:
    discount = 25
else:
    discount = 0
print("Discount:", discount, "percent")
