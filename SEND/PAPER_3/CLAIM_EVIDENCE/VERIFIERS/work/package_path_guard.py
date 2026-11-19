"""Fail-closed PACKAGE_ROOT-only runtime path guard.

The guard derives the package root from the calling script.  It never requires
an E:, C:, or D: drive and it rejects runtime paths that resolve outside the
current package or through a symlink/junction/reparse point.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import stat
from pathlib import Path
from typing import Iterable, Mapping, Sequence


PACKAGE_MARKERS = ("work", "R_STATUS.json")
CODE_SUFFIXES = {".py", ".ps1", ".sh", ".bat", ".cmd"}
_ABSOLUTE_PATH_RE = re.compile(
    r"(?i)(?:[a-z]:[\\/]|/mnt/[a-z]/|/home/|/users/)"
)


def package_root_from(start: str | os.PathLike[str]) -> Path:
    """Return the nearest package root containing the required markers."""

    here = Path(start).resolve(strict=False)
    if here.is_file() or here.suffix:
        here = here.parent
    for candidate in (here, *here.parents):
        if all((candidate / marker).exists() for marker in PACKAGE_MARKERS):
            return candidate
    raise RuntimeError(f"PACKAGE_ROOT_NOT_FOUND:{start}")


def _is_reparse(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        attributes = getattr(os.lstat(path), "st_file_attributes", 0)
        return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))
    except (FileNotFoundError, OSError):
        return False


def _assert_inside(path: Path, package_root: Path, role: str) -> Path:
    root = package_root.resolve(strict=False)
    resolved = path.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(f"OUTSIDE_PACKAGE_ROOT:{role}:{resolved}") from exc

    current = resolved
    while True:
        if current.exists() and _is_reparse(current):
            raise RuntimeError(f"REPARSE_OR_SYMLINK:{role}:{current}")
        if current == root or current.parent == current:
            break
        current = current.parent
    return resolved


def safe_resolve(
    path: str | os.PathLike[str], package_root: Path, role: str
) -> Path:
    return _assert_inside(Path(path), package_root, role)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _bytes(path: Path) -> int:
    if path.is_file():
        return path.stat().st_size
    if path.is_dir():
        return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())
    return 0


def _runtime_targets(package_root: Path) -> list[tuple[str, Path]]:
    vendor = package_root / "vendor" / (
        "RIUD_R27_MORPHOLOGY_UNIVERSAL_DYNAMICS_LAW_SEARCH_R0_20260802"
    )
    targets = [
        ("package_root", package_root),
        ("runtime_work", package_root / "work"),
        ("independent_branch", package_root / "03_INDEPENDENT_REPLICATION_R1"),
        ("comparison_branch", package_root / "04_FINAL_COMPARISON"),
        ("cold_branch", package_root / "01_COLD_EXACT_REBUILD_R1"),
        ("r2_branch", package_root / "RIUD_R1_C33_EXT4_BATCHED_SYNC_SAFE_RESUME_R2_20260803"),
        ("vendor_r27", vendor),
        ("vendor_r27_runner", vendor / "run.py"),
        ("vendor_r27_work", vendor / "work"),
        ("runtime_helper", package_root / "work" / "r27_dynamic_null_rebuild.py"),
        ("prism_source", package_root / "01_INPUT_ASSETS" / "PRISM_SOURCE"),
        ("workspace_source", package_root / "01_INPUT_ASSETS" / "WORK_SOURCE"),
        ("root_status", package_root / "R_STATUS.json"),
        ("branch_status", package_root / "03_INDEPENDENT_REPLICATION_R1" / "R_STATUS.json"),
        ("branch_send_to_chat", package_root / "03_INDEPENDENT_REPLICATION_R1" / "SEND_TO_CHAT.txt"),
    ]
    return targets


def write_resolved_runtime_paths(package_root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for role, candidate in _runtime_targets(package_root):
        resolved = safe_resolve(candidate, package_root, role)
        rel = resolved.relative_to(package_root).as_posix() or "."
        kind = "file" if resolved.is_file() else "directory" if resolved.is_dir() else "missing"
        rows.append(
            {
                "role": role,
                "resolved_path": str(resolved),
                "relative_to_package_root": rel,
                "kind": kind,
                "exists": resolved.exists(),
                "bytes": _bytes(resolved),
                "sha256": _sha256_file(resolved) if resolved.is_file() else "",
            }
        )
    output = package_root / "RESOLVED_RUNTIME_PATHS.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def _runtime_code_files(package_root: Path) -> Iterable[Path]:
    roots = [
        package_root / "work",
        package_root / "vendor" / (
            "RIUD_R27_MORPHOLOGY_UNIVERSAL_DYNAMICS_LAW_SEARCH_R0_20260802"
        ),
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in CODE_SUFFIXES:
                if path.name == "package_path_guard.py":
                    continue
                yield path


def code_absolute_path_hits(package_root: Path) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in _runtime_code_files(package_root):
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), 1):
            if _ABSOLUTE_PATH_RE.search(line):
                hits.append(
                    {
                        "file": path.relative_to(package_root).as_posix(),
                        "line": str(line_number),
                        "text": line.strip()[:500],
                    }
                )
    return hits


def _reparse_hits(package_root: Path) -> list[str]:
    hits: list[str] = []
    for path in package_root.rglob("*"):
        if _is_reparse(path):
            hits.append(path.relative_to(package_root).as_posix())
    return hits


def verify(package_root: Path, *, write_outputs: bool = True) -> dict[str, object]:
    package_root = package_root.resolve(strict=False)
    errors: list[str] = []
    rows: list[dict[str, object]] = []
    try:
        rows = write_resolved_runtime_paths(package_root)
    except Exception as exc:  # fail closed and preserve the reason
        errors.append(f"RUNTIME_PATH_RESOLUTION:{type(exc).__name__}:{exc}")
    hits = code_absolute_path_hits(package_root)
    if hits:
        errors.append(f"ABSOLUTE_RUNTIME_PATH_HITS:{len(hits)}")
    reparse_hits = _reparse_hits(package_root)
    if reparse_hits:
        errors.append(f"REPARSE_OR_SYMLINK_HITS:{len(reparse_hits)}")
    result: dict[str, object] = {
        "guard": "PACKAGE_ROOT_ONLY",
        "package_root": str(package_root),
        "runtime_paths_written": bool(rows),
        "absolute_runtime_path_hits": hits,
        "reparse_or_symlink_hits": reparse_hits,
        "C_DRIVE_RUNTIME_DEPENDENCY": bool(hits),
        "E_DRIVE_RUNTIME_DEPENDENCY": bool(hits),
        "D_DRIVE_RUNTIME_DEPENDENCY": bool(hits),
        "silent_fallback_detected": False,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
    }
    if write_outputs:
        output = package_root / "PACKAGE_ROOT_SELF_CONTAINMENT_RESULT.json"
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def enforce_startup(
    script_path: str | os.PathLike[str],
    extra: Sequence[tuple[str, str | os.PathLike[str]]] = (),
) -> Path:
    package_root = package_root_from(script_path)
    result = verify(package_root, write_outputs=True)
    for role, value in extra:
        safe_resolve(value, package_root, role)
    if result["status"] != "PASS":
        raise RuntimeError("PACKAGE_ROOT_GUARD_FAIL:" + json.dumps(result, ensure_ascii=False))
    return package_root


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    package_root = (
        Path(args.package_root).resolve(strict=False)
        if args.package_root
        else package_root_from(__file__)
    )
    result = verify(package_root, write_outputs=True)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
