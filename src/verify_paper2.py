"""Verification runner for Paper II numerical companion."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TARGET_DIR = ROOT / "SEND" / "PAPER_2" / "SHARED_NUMERICAL_RELEASE_PAPER_I_II" / "RELEASE_ROOT"
SCRIPT = TARGET_DIR / "verify_numbers.py"


def main() -> int:
    if not SCRIPT.exists():
        print(f"ERROR: Script not found: {SCRIPT}", file=sys.stderr)
        return 1
    print("Executing Paper II numerical companion verification...")
    result = subprocess.run([sys.executable, str(SCRIPT)], cwd=str(TARGET_DIR))
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
