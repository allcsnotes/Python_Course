from contextlib import contextmanager

site = {"maintenance": False}


@contextmanager
def maintenance(site):
    site["maintenance"] = True
    try:
        yield
    finally:
        site["maintenance"] = False


def update_prices(prices):
    for price in prices:
        print("fixing", int(price))


try:
    with maintenance(site):
        update_prices(["499", "abc", "999"])
except ValueError:
    print("update failed")
print("maintenance:", site["maintenance"])
