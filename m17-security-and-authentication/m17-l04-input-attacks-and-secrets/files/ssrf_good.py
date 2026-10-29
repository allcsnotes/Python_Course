import servers
from fetch_good import fetch_thumbnail

logo = "http://localhost:8174/logo.png"
notes = "http://localhost:8274/admin/notes"

servers.start()
print(fetch_thumbnail(logo))
print(fetch_thumbnail(notes))
