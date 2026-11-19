"""Master verification runner across all papers (Paper I through Paper VIII)."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "src"

TESTS = [
    ("Paper I", "src/verify_paper1.py", "Numerical companion release checks (133 tests)"),
    ("Paper II", "src/verify_paper2.py", "SXS numerical companion checks (133 tests)"),
    ("Paper III", "src/verify_paper3.py", "Independent replication suite (R27 tree)"),
    ("Paper IV", "fast_track_r40/reproduce_r40.py", "R40 Holdout-5 forward likelihood benchmark"),
    ("Paper V", "src/verify_paper5.py", "Authoritative numerical freeze check (128 files)"),
    ("Paper VI", "src/verify_paper6.py", "Frequency timing geometry and census check"),
    ("Paper VII", "src/run_paper7.py", "Eventwise observation layer and C01 operator"),
    ("Paper VIII", "src/verify_paper8.py", "Mechanism evidence and ETK benchmark closure"),
]


def main() -> int:
    t_start = time.time()
    print("MIsCORE-RIUD Master Verification Suite (Papers I - VIII)")
    print("=" * 80)
    print(f"{'Paper':<12} {'Target':<32} {'Time (s)':>10} {'Verdict':>12}")
    print("-" * 80)

    all_passed = True
    results = []

    for name, script_rel, desc in TESTS:
        script_path = ROOT / script_rel
        t0 = time.time()
        res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, cwd=str(ROOT))
        elapsed = time.time() - t0
        passed = (res.returncode == 0)
        if not passed:
            all_passed = False
        verdict = "PASS" if passed else "FAIL"
        results.append((name, script_rel, elapsed, verdict))
        print(f"{name:<12} {script_rel:<32} {elapsed:10.2f} {verdict:>12}")

    print("=" * 80)
    total_elapsed = time.time() - t_start
    print(f"Total verification time: {total_elapsed:.2f} s")
    if all_passed:
        print("OVERALL RESULT: ALL TESTS PASSED (8/8)")
        return 0
    else:
        print("OVERALL RESULT: ONE OR MORE TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
