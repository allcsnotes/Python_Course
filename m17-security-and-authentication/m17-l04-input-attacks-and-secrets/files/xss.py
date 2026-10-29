import html

description = "Nice! <script>alert(1)</script>"


def card_bad(text):
    return f"<p>{text}</p>"


def card_good(text):
    return f"<p>{html.escape(text)}</p>"


print(card_bad(description))
print(card_good(description))
