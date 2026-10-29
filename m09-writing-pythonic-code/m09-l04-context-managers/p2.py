from contextlib import contextmanager

site = {"maintenance": False}


@contextmanager
def maintenance(site):
    site["maintenance"] = True
    try:
        yield
    finally:
        site["maintenance"] = False


with maintenance(site) as m:
    print(m)
