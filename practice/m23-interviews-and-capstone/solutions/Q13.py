# Q13 - Why a virtual environment
import subprocess
import sys
import tempfile
from pathlib import Path

print("running in a venv:", sys.prefix != sys.base_prefix)

with tempfile.TemporaryDirectory() as folder:
    env = Path(folder) / "demo-env"
    subprocess.run([sys.executable, "-m", "venv", str(env)], check=True)
    python = env / "bin" / "python"
    check = "import sys, importlib.metadata as m; print(sys.prefix != sys.base_prefix, sorted(d.name for d in m.distributions()))"
    out = subprocess.run([python, "-c", check], capture_output=True, text=True, check=True)
    print("fresh venv  :", out.stdout.strip())
    print("has its own site-packages:", (env / "lib").exists())
