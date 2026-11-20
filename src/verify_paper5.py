"""Verification runner for Paper V authoritative freeze."""

from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG_DIR = ROOT / "SEND" / "PAPER_5"
MANIFEST = PKG_DIR / "SHA256_MANIFEST.txt"
CHECK_DIR = ROOT / "SEND" / "PAPER_5_CHECK"


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

    companion_ok = True
    if CHECK_DIR.exists():
        check_manifest = CHECK_DIR / "SHA256_MANIFEST.txt"
        if check_manifest.exists():
            c_checked = 0
            c_mismatches = 0
            for line in check_manifest.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(None, 1)
                if len(parts) == 2:
                    exp_h, rel_f = parts[0], parts[1].strip()
                    tf = CHECK_DIR / rel_f
                    if tf.exists() and hashlib.sha256(tf.read_bytes()).hexdigest().lower() == exp_h.lower():
                        c_checked += 1
                    else:
                        c_mismatches += 1
                        companion_ok = False
            print(f"Paper V companion check manifest: {c_checked} verified, {c_mismatches} mismatches")

        stats_csv = CHECK_DIR / "GAP_POST_T0_SHORT_TRACK_STATS.csv"
        if stats_csv.exists():
            with open(stats_csv, "r", encoding="utf-8") as f:
                row = next(csv.DictReader(f))
                p_fisher = float(row["FISHER_P_ONE_SIDED"])
                p_perm = float(row["PERM_P_ONE_SIDED"])
                spin_med = float(row["SHORT_SPIN_POST_MEDIAN"])
                if abs(p_fisher - 8.389830113725958e-11) > 1e-18 or p_perm != 1e-05 or abs(spin_med - 0.4582079579083361) > 1e-6:
                    print("ERROR: Numerical discrepancy in Paper V Short-Track statistics!", file=sys.stderr)
                    companion_ok = False
                else:
                    print(f"Paper V companion numericals: Fisher p={p_fisher:.4e}, Perm p={p_perm:.1e}, Spin med={spin_med:.4f} verified.")

    if mismatches == 0 and missing == 0 and checked > 0 and companion_ok:
        print("VERIFY_PAPER5_FREEZE=PASS")
        return 0
    else:
        print("VERIFY_PAPER5_FREEZE=FAIL")
        return 1


if __name__ == "__main__":
    sys.exit(main())

