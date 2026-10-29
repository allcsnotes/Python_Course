import threading


def greet(name):
    me = threading.current_thread().name
    print(f"{me}: hello, {name}")


t = threading.Thread(target=greet, args=("Lukas",))
t.start()
t.join()
print("main: all done")
