from topk import top_k

text = "the cat and the dog and the bird saw a cat".split()
print(top_k(text, 2))
print(top_k(text, 10))
print(top_k([], 3))
