"""Reproduction runner for Paper IV Holdout-5 R40 benchmark."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "fast_track_r40" / "reproduce_r40.py"


def main() -> int:
    if not SCRIPT.exists():
        print(f"ERROR: Script not found: {SCRIPT}", file=sys.stderr)
        return 1
    result = subprocess.run([sys.executable, str(SCRIPT)], cwd=str(ROOT))
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
