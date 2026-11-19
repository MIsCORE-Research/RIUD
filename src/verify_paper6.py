"""Verification runner for Paper VI frequency timing geometry."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
PKG_DIR = ROOT / "SEND" / "PAPER_6"
MANIFEST = PKG_DIR / "SHA256_MANIFEST.txt"
SUMMARY_CSV = PKG_DIR / "NUMERICAL_SUMMARY.csv"


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

    print(f"Paper VI manifest check: {checked} verified, {mismatches} mismatches, {missing} missing")

    num_ok = True
    if SUMMARY_CSV.exists():
        df = pd.read_csv(SUMMARY_CSV)
        print("Numerical summary metrics:")
        for _, row in df.iterrows():
            metric = row.get("METRIC", row.get(df.columns[0]))
            val = row.get("VALUE", row.get(df.columns[1]))
            print(f"  {metric}: {val}")
    else:
        print("WARNING: NUMERICAL_SUMMARY.csv missing")
        num_ok = False

    if mismatches == 0 and missing == 0 and checked > 0 and num_ok:
        print("PAPER_6_VERIFICATION=PASS")
        return 0
    else:
        print("PAPER_6_VERIFICATION=FAIL")
        return 1


if __name__ == "__main__":
    sys.exit(main())
