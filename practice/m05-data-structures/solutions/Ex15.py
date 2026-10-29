# Exercise 15 - Fix the broken set code (all five repaired)
viewers = set()                    # was: {}  (that is a dictionary)
viewers.add("Asha")
print(viewers)

tags = {"b", "a"}
print(sorted(tags)[0])             # was: tags[0]

points = {(1, 2), 3}               # was: {[1, 2], 3}
print(len(points))

s = {1, 2}
s.discard(5)                       # was: s.remove(5)
print(s)

print({1, 2} | {3})                # was: {1, 2} + {3}
