# Q10 - __name__ == "__main__" and circular imports
import sys
import tempfile
from pathlib import Path

print("this file's __name__ is", __name__)

def main():
    print("main() runs only when the file is run directly")

if __name__ == "__main__":
    main()

with tempfile.TemporaryDirectory() as folder:
    root = Path(folder)
    (root / "orders.py").write_text("from billing import charge\ndef place(): return charge()\n")
    (root / "billing.py").write_text("from orders import place\ndef charge(): return 'charged'\n")
    (root / "billing_ok.py").write_text("def charge():\n    from orders_ok import place   # imported when needed\n    return 'charged'\n")
    (root / "orders_ok.py").write_text("from billing_ok import charge\ndef place(): return charge()\n")
    sys.path.insert(0, folder)
    try:
        import orders
    except ImportError as error:
        print("ImportError:", str(error).split(" (")[0])
    import orders_ok
    print("fixed:", orders_ok.place())
