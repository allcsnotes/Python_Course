def starter(code):
    match code:
        case "C101" | "C102" as chosen:
            return f"starter course {chosen}"
        case _:
            return "other course"


print(starter("C102"))
print(starter("C300"))
