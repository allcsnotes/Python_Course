from jinja2 import Environment

env = Environment(autoescape=True)
page = env.from_string("<p>{{ text }}</p>")
text = "Nice! <script>alert(1)</script>"
print(page.render(text=text))
