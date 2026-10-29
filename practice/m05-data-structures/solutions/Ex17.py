# Exercise 17 - Loops into comprehensions
prices = [1499, 999, 799, 499]
names = ["asha", "lukas", "priya"]

squares = []
for n in range(1, 6):
    squares.append(n * n)
evens = []
for n in range(1, 11):
    if n % 2 == 0:
        evens.append(n)
with_gst = []
for p in prices:
    with_gst.append(p * 118 // 100)
shouting = []
for name in names:
    shouting.append(name.upper())
lengths = []
for name in names:
    lengths.append(len(name))

squares2 = [n * n for n in range(1, 6)]
evens2 = [n for n in range(1, 11) if n % 2 == 0]
with_gst2 = [p * 118 // 100 for p in prices]
shouting2 = [name.upper() for name in names]
lengths2 = [len(name) for name in names]

print("squares:", squares)
print("squares (comprehension):", squares2)
print("evens:", evens)
print("evens (comprehension):", evens2)
print("with GST:", with_gst)
print("with GST (comprehension):", with_gst2)
print("shouting:", shouting)
print("shouting (comprehension):", shouting2)
print("lengths:", lengths)
print("lengths (comprehension):", lengths2)
print(squares == squares2, evens == evens2, with_gst == with_gst2,
      shouting == shouting2, lengths == lengths2)
