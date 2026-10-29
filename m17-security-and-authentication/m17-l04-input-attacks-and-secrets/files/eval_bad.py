from pathlib import Path


def discount(formula):
    return eval(formula)


bad = "__import__('pathlib').Path('proof.txt').write_text('ran')"
print(discount("1000 * 0.8"))
print(discount(bad))
print(Path("proof.txt").exists())
