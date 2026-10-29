def total_paid(amounts):
    total = 0
    for index, amount in enumerate(amounts):
        total = total + amount
    return total


amounts = [500] * 1000
amounts[612] = -500
print(total_paid(amounts))
