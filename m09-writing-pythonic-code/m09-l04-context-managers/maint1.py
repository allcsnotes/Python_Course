class Maintenance:
    def __init__(self, site):
        self.site = site

    def __enter__(self):
        self.site["maintenance"] = True

    def __exit__(self, exc_type, exc_value, traceback):
        self.site["maintenance"] = False


site = {"maintenance": False}


def update_prices(prices):
    for price in prices:
        print("fixing", int(price))


try:
    with Maintenance(site):
        update_prices(["499", "abc", "999"])
except ValueError:
    print("update failed")
print("maintenance:", site["maintenance"])
