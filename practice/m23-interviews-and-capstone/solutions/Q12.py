# Q12 - try, except, else, finally
def parse(text):
    try:
        number = int(text)
    except ValueError:
        print("  except: not a number")
        return None
    else:
        print("  else: no error happened")
        return number
    finally:
        print("  finally: always runs")

print(parse("42"))
print(parse("forty-two"))

def which():
    try:
        return "from try"
    finally:
        print("  finally still runs before the function returns")

print(which())

try:
    try:
        1 / 0
    except ZeroDivisionError as error:
        raise ValueError("bad input") from error      # keep the original as the cause
except ValueError as error:
    print(repr(error), "| cause:", repr(error.__cause__))
