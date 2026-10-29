course = input("Course: ")
price = int(input("Price in rupees: "))
seats = int(input("Seats: "))

subtotal = price * seats
gst = subtotal * 18 // 100
total = subtotal + gst

print()
print("RECEIPT")
print("-" * 26)
print(f"{course:<14}{subtotal:>12,}")
print(f"{'GST 18%':<14}{gst:>12,}")
print(f"{'Total':<14}{total:>12,}")
