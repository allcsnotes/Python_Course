def factorial(n):
    result = 1
    for number in range(2, n + 1):
        result = result * number
    return result


print(factorial(4))
print(len(str(factorial(1000))))
