price = 199900
gst = price * 18 // 100
total = price + gst
rupees, paise = divmod(total, 100)
print(gst)
print(total)
print(rupees, paise)
