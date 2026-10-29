class Anything:
    def __eq__(self, other):
        return True


thing = Anything()
print(thing == None)
print(thing is None)
