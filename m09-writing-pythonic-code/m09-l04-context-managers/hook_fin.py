site = {"maintenance": False}


def update_prices(prices):
    site["maintenance"] = True
    try:
        for price in prices:
            print("fixing", int(price))
    finally:
        site["maintenance"] = False


try:
    update_prices(["499", "abc", "999"])
except ValueError:
    print("update failed")
print("maintenance:", site["maintenance"])
