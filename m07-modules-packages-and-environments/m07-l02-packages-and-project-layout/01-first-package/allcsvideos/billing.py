from allcsvideos.courses import price_of


def total(titles):
    amount = 0
    for title in titles:
        amount += price_of(title)
    return amount


if __name__ == "__main__":
    print(total(["Python Basics", "Web Dev"]))
