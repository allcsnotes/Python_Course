def is_broken(status):
    return status > 400


statuses = [200, 301, 404, 500, 400]
broken = [s for s in statuses if is_broken(s)]
print(len(broken), "of", len(statuses), "links are broken")
