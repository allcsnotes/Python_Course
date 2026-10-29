def show_banner():
    print("=== Number Guessing Game ===")

def ask_again():
    return input("Play again? (y/n): ").strip().lower()

show_banner()
again = ask_again()
print(f"You chose: {again}")
