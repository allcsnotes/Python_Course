# Q03 - Generators
import sys

def squares(limit):
    for n in range(limit):
        yield n * n                 # pauses here, resumes on the next call

gen = squares(3)
print(next(gen), next(gen), next(gen))
print(list(squares(5)))

as_list = [n * n for n in range(1_000_000)]
as_gen = (n * n for n in range(1_000_000))
print("list bytes:", sys.getsizeof(as_list), "| generator bytes:", sys.getsizeof(as_gen))
print(sum(as_gen))                  # still gives the full answer, one item at a time
print(sum(as_gen))                  # but a generator can be used only once

def first_words(lines):             # a lazy pipeline stage
    for line in lines:
        yield line.split()[0]

print(list(first_words(["python is fun", "sql is old", "rust is new"])))
