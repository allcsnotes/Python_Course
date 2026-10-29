import math

from app.codes import new_code


def first_repeat(length):
    seen = set()
    while True:
        code = new_code(length)
        if code in seen:
            return len(seen) + 1
        seen.add(code)


for length in (2, 3, 4):
    runs = [first_repeat(length) for _ in range(5)]
    print(f"length {length}: {62**length:,} codes")
    print(f"  first repeat after {runs} codes")

big = 62**7
likely = int(math.sqrt(math.pi / 2 * big))
print(f"length 7: {big:,} codes")
print(f"  a repeat is likely after about {likely:,} codes")
