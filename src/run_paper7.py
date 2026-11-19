"""Runner and verification suite for Paper VII eventwise observation layer."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG_DIR = ROOT / "SEND" / "PAPER_7"
MANIFEST = PKG_DIR / "SHA256_MANIFEST.txt"
STAGE1_SCRIPT = PKG_DIR / "run_eventwise_full_tf_change_separate.py"
STAGE2_SCRIPT = PKG_DIR / "run_eventwise_c_slope_changepoint.py"


def verify_package() -> int:
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

    print(f"Paper VII manifest check: {checked} verified, {mismatches} mismatches, {missing} missing")

    exp_dir = PKG_DIR / "EXPECTED_OUTPUTS"
    exp_ok = exp_dir.exists() and any(exp_dir.iterdir())
    print(f"Paper VII expected outputs present: {exp_ok}")

    if mismatches == 0 and missing == 0 and checked > 0 and exp_ok:
        print("PAPER_7_VERIFICATION=PASS")
        return 0
    else:
        print("PAPER_7_VERIFICATION=FAIL")
        return 1


def compute_pipeline() -> int:
    print("Executing Paper VII Stage 1 (Canonical C01 operator across 99 events)...")
    res1 = subprocess.run([sys.executable, str(STAGE1_SCRIPT)], cwd=str(PKG_DIR))
    if res1.returncode != 0:
        print("ERROR: Stage 1 execution failed.", file=sys.stderr)
        return res1.returncode

    print("Executing Paper VII Stage 2 (Changepoint and slope estimation)...")
    res2 = subprocess.run([sys.executable, str(STAGE2_SCRIPT)], cwd=str(PKG_DIR))
    if res2.returncode != 0:
        print("ERROR: Stage 2 execution failed.", file=sys.stderr)
        return res2.returncode

    print("PAPER_7_COMPUTATION=PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Paper VII runner and verifier")
    parser.add_argument("--mode", choices=["verify", "compute"], default="verify",
                        help="Execution mode: verify against manifest (fast) or compute from strain files")
    args = parser.parse_args()

    if args.mode == "verify":
        return verify_package()
    else:
        return compute_pipeline()


if __name__ == "__main__":
    sys.exit(main())
