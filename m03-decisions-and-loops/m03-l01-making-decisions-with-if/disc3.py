seats = 3
if seats >= 10:
    discount = 25
elif seats >= 5:
    discount = 15
elif seats >= 2:
    discount = 5
else:
    discount = 0
print("Discount:", discount, "percent")
