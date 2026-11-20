"""Verification runner for Paper VIII mechanism evidence."""

from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG_DIR = ROOT / "SEND" / "PAPER_8"
MANIFEST = PKG_DIR / "SHA256_MANIFEST.txt"
CHECK_DIR = ROOT / "SEND" / "PAPER_8_CHECK"
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
            print(f"Paper VIII companion check manifest: {c_checked} verified, {c_mismatches} mismatches")

        etk_csv = CHECK_DIR / "ETK_2M_LOCAL_PHASE_AK_RESULTS_20260910.csv"
        if etk_csv.exists():
            with open(etk_csv, "r", encoding="utf-8") as f:
                rows = {r["interval"]: r for r in csv.DictReader(f)}
                r02 = rows.get("0.00-2.00M")
                r12 = rows.get("1.00-2.00M")
                if r02 and r12:
                    trap02 = float(r02["trapezoid_recovery_pct"])
                    simp02 = float(r02["simpson_recovery_pct"])
                    trap12 = float(r12["trapezoid_recovery_pct"])
                    if abs(round(trap02, 3) - 99.151) > 1e-4 or abs(round(simp02, 3) - 99.571) > 1e-4 or abs(round(trap12, 3) - 99.917) > 1e-4:
                        print("ERROR: Numerical discrepancy in Paper VIII ETK 0-2M AK results!", file=sys.stderr)
                        companion_ok = False
                    else:
                        print(f"Paper VIII companion numericals: 0-2M AK recovery {trap02:.3f}% (Simpson {simp02:.3f}%), 1-2M {trap12:.3f}% verified.")

    if mismatches == 0 and missing == 0 and checked > 0 and op_ok and etk_ok and companion_ok:
        print("PAPER_8_VERIFICATION=PASS")
        return 0
    else:
        print("PAPER_8_VERIFICATION=FAIL")
        return 1


if __name__ == "__main__":
    sys.exit(main())
