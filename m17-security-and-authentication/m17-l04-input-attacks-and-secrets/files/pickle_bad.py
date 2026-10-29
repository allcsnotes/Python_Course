import pickle


class Evil:
    def __reduce__(self):
        return (print, ("this ran just by loading the data",))


blob = pickle.dumps(Evil())
print("received", len(blob), "bytes")
data = pickle.loads(blob)
