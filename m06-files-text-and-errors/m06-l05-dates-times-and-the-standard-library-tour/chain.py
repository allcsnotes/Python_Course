from itertools import chain, count

morning = ["Lukas", "Priya"]
evening = ["Meera", "Rahul"]
for name in chain(morning, evening):
    print(name)
for ticket, name in zip(count(101), morning):
    print(ticket, name)
