"""Verification runner for Paper III independent replication."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = ROOT / "SEND" / "PAPER_3" / "CLAIM_EVIDENCE" / "VERIFIERS"
WORK = PACKAGE_ROOT / "work"
if str(WORK) not in sys.path:
    sys.path.insert(0, str(WORK))

from package_path_guard import verify  # noqa: E402


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _csv_rows(path: Path) -> int:
    if not path.exists():
        return -1
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return max(sum(1 for _ in csv.DictReader(handle)), 0)


def main() -> int:
    # Run guard without overwriting frozen manifest file on disk
    guard = verify(PACKAGE_ROOT, write_outputs=False)
    branch = PACKAGE_ROOT.parent / "INDEPENDENT_REPLICATION"
    status_path = branch / "R_STATUS.json"
    status = _read_json(status_path) if status_path.exists() else {}
    checks = {
        "guard_status": guard["status"],
        "branch_status_exists": status_path.exists(),
        "independent_replication_status": status.get("INDEPENDENT_REPLICATION_STATUS"),
        "raw_rows": _csv_rows(branch / "PAPERIII_RESULTS.csv"),
        "draw_rows": _csv_rows(branch / "PAPERIII_DRAW_TABLE.csv"),
        "final_verdict": status.get("FINAL_VERDICT"),
    }
    checks["status"] = "PASS" if guard["status"] == "PASS" and status_path.exists() else "FAIL"
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    return 0 if checks["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
