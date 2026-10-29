FREE = "free"


def label(plan):
    match plan:
        case FREE:
            return "no payment"
        case _:
            return "paid plan"


print(label("pro"))
