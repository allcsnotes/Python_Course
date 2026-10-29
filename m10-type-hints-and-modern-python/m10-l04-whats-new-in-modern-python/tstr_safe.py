from html import escape
from string.templatelib import Interpolation


def clean_html(template):
    parts = []
    for item in template:
        if isinstance(item, Interpolation):
            parts.append(escape(item.value))
        else:
            parts.append(item)
    return "".join(parts)


name = "<b>Lukas</b>"
print(clean_html(t"<p>Hello {name}</p>"))
