import threading
from pages import fetch

t = threading.Thread(target=fetch(1))
t.start()
t.join()
print("done")
