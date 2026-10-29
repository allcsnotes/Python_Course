import time


def timer(func):
    def wrapper():
        start = time.perf_counter()
        result = func()
        took = time.perf_counter() - start
        print(f"Took {took:.1f} seconds")
        return result

    return wrapper


def weekly_report():
    time.sleep(0.2)
    print("Report ready")


weekly_report = timer(weekly_report)
weekly_report()
