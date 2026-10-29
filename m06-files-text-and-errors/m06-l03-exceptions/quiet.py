total = 0
for text in ["1499", "999", "abc", "499"]:
    try:
        total = total + int(text)
    except ValueError:
        pass
print("Total:", total)
