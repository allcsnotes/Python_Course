# Exercise 04 - Swap two labels without losing a value
first = "Asha"
second = "Lukas"

# Way 1: a helper label
temp = first
first = second
second = temp
print("After helper swap:", first, second)

# Way 2: the one-line swap
first, second = second, first
print("After one-line swap:", first, second)
