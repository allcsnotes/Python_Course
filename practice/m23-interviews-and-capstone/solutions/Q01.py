# Q01 - List vs tuple
seats = {("A", 1): "Asha", ("A", 2): "Lukas"}   # tuples can be dict keys
print(seats[("A", 2)])
try:
    {["A", 1]: "Priya"}
except TypeError as error:
    print("TypeError:", error)

city, country = "Frankfurt", "Germany"           # packing and unpacking
city, country = country, city                    # swap, no temp variable
print(city, country)

first, *middle, last = [1, 2, 3, 4, 5]
print(first, middle, last)
