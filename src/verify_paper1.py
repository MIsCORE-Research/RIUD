"""Verification runner for Paper I numerical companion."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TARGET_DIR = ROOT / "SEND" / "PAPER_1" / "SHARED_NUMERICAL_RELEASE_PAPER_I_II" / "RELEASE_ROOT"
SCRIPT = TARGET_DIR / "verify_numbers.py"
TABLE1_SCRIPT = ROOT / "SEND" / "PAPER_1_CHECK" / "reproduce_table1.py"


def main() -> int:
    if not SCRIPT.exists():
        print(f"ERROR: Script not found: {SCRIPT}", file=sys.stderr)
        return 1
    print("Executing Paper I numerical companion verification...")
    result = subprocess.run([sys.executable, str(SCRIPT)], cwd=str(TARGET_DIR))
    if result.returncode != 0:
        return result.returncode

    if TABLE1_SCRIPT.exists():
        print("\nExecuting Paper I Table 1 verification (29 events)...")
        res_t1 = subprocess.run([sys.executable, str(TABLE1_SCRIPT)], cwd=str(TABLE1_SCRIPT.parent))
        return res_t1.returncode

    return 0


if __name__ == "__main__":
    sys.exit(main())
