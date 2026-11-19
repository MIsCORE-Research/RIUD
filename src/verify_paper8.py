"""Verification runner for Paper VIII mechanism evidence."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG_DIR = ROOT / "SEND" / "PAPER_8"
MANIFEST = PKG_DIR / "SHA256_MANIFEST.txt"
OPERATOR_FILE = PKG_DIR / "OPERATORS" / "run_eventwise_full_tf_change_separate.py"
EXPECTED_OPERATOR_HASH = "26B9F63F55D39C715E6DE907F7759A04C9C7427F7F039FDA9507A4AFBF76EF45"


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

    print(f"Paper VIII manifest check: {checked} verified, {mismatches} mismatches, {missing} missing")

    op_ok = False
    if OPERATOR_FILE.exists():
        act_op_hash = hashlib.sha256(OPERATOR_FILE.read_bytes()).hexdigest().upper()
        if act_op_hash == EXPECTED_OPERATOR_HASH:
            print(f"Canonical operator C01 SHA-256 verified: {act_op_hash}")
            op_ok = True
        else:
            print(f"ERROR: C01 operator hash mismatch: {act_op_hash} != {EXPECTED_OPERATOR_HASH}")
    else:
        print(f"ERROR: C01 operator file missing: {OPERATOR_FILE}")

    etk_dir = PKG_DIR / "ETK_EXACT_BENCHMARK"
    etk_ok = etk_dir.exists() and any(etk_dir.iterdir())
    print(f"ETK exact benchmark assets present: {etk_ok}")

    if mismatches == 0 and missing == 0 and checked > 0 and op_ok and etk_ok:
        print("PAPER_8_VERIFICATION=PASS")
        return 0
    else:
        print("PAPER_8_VERIFICATION=FAIL")
        return 1


if __name__ == "__main__":
    sys.exit(main())
