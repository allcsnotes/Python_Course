for value in (["a", "b"], ("a", "b"), "ab"):
    match value:
        case [first, second]:
            print("two items:", first, second)
        case _:
            print("no match:", value)
