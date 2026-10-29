from itertools import product

plans = ["monthly", "yearly"]
countries = ["India", "Germany", "Brazil"]
for plan, country in product(plans, countries):
    print(plan, country)
print(len(list(product(plans, countries))))
