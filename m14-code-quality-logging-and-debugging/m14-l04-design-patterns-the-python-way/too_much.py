class HelloStrategy:
    def say(self):
        return "hello"


class HelloFactory:
    def make(self):
        return HelloStrategy()


print(HelloFactory().make().say())
print("hello")
