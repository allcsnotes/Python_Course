def is_prime(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True


def count_primes(start, stop):
    found = [n for n in range(start, stop) if is_prime(n)]
    return len(found)
