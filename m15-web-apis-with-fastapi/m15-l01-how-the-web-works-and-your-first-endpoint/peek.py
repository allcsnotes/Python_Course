from main import app, home

print(home())
for route in app.routes:
    print(route.path)
