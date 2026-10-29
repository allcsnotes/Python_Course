from pathlib import Path

path = Path("best_score.txt")


def load_best():
    if not path.exists():
        return 0
    return int(path.read_text(encoding="utf-8"))


def save_best(score):
    path.write_text(str(score), encoding="utf-8")


best = load_best()
tries = int(input("How many tries did you need? "))
if best == 0 or tries < best:
    best = tries
    save_best(best)
    print("New best score!")
print(f"Best so far: {best}")
