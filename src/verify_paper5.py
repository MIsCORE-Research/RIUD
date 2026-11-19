"""Verification runner for Paper V authoritative freeze."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG_DIR = ROOT / "SEND" / "PAPER_5"
MANIFEST = PKG_DIR / "SHA256_MANIFEST.txt"


def main() -> int:
    if not MANIFEST.exists():
        print(f"ERROR: Manifest missing: {MANIFEST}", file=sys.stderr)
        return 1

    lines = MANIFEST.read_text(encoding="utf-8", errors="ignore").splitlines()
    checked = 0
    mismatches = 0
    missing = 0

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        exp_hash, rel_path = parts[0], parts[1].strip()
        fpath = PKG_DIR / rel_path
        if not fpath.exists():
            missing += 1
            continue
        checked += 1
        act_hash = hashlib.sha256(fpath.read_bytes()).hexdigest()
        if act_hash.lower() != exp_hash.lower():
            mismatches += 1

    print(f"Paper V freeze manifest check: {checked} verified, {mismatches} mismatches, {missing} missing")
    if mismatches == 0 and missing == 0 and checked > 0:
        print("VERIFY_PAPER5_FREEZE=PASS")
        return 0
    else:
        print("VERIFY_PAPER5_FREEZE=FAIL")
        return 1


if __name__ == "__main__":
    sys.exit(main())
