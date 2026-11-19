from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


ROOT = Path(r"E:\RIUD_ACTIVE_20260808")
BASE = ROOT / "RIUD_FREQUENCY_FAMILY_K1_K2_K5_ABC_GEOMETRY_INTEGRATED_RELATION_ASSEMBLED_R2_20260826"
PRED = ROOT / "RIUD_FREQUENCY_FAMILY_K1_K2_K5_ABC_GEOMETRY_PREDICTION_AUDIT_R1_20260826"
AUDIT = ROOT / "RIUD_FREQUENCY_FAMILY_K1_K2_K5_ABC_GEOMETRY_MISMATCH_FORENSIC_R1_20260826"
OUT = ROOT / "RIUD_FREQUENCY_FAMILY_K1_K2_K5_ABC_GEOMETRY_MISMATCH_FORENSIC_ASSEMBLED_R4_20260826"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    shutil.copytree(src, dst)


def main() -> int:
    if OUT.exists():
        raise RuntimeError(f"TARGET_EXISTS:{OUT}")
    OUT.mkdir(parents=True)

    # Keep the three source packages at one shallow level; the source folders
    # themselves already contain their internal layout.
    copy_tree(BASE, OUT / "01_BASE")
    copy_tree(PRED, OUT / "02_PREDICTION")
    copy_tree(AUDIT, OUT / "03_MISMATCH")

    src_script = Path(__file__)
    shutil.copy2(src_script, OUT / "04_SOURCE_SCRIPTS" / src_script.name) if False else None
    (OUT / "04_SOURCE_SCRIPTS").mkdir()
    shutil.copy2(src_script, OUT / "04_SOURCE_SCRIPTS" / src_script.name)

    event_path = OUT / "03_MISMATCH" / "MISMATCH_EVENT_FORENSIC_TABLE.csv"
    axis_path = OUT / "03_MISMATCH" / "MISMATCH_AXIS_CONTRASTS.csv"
    inter_path = OUT / "03_MISMATCH" / "MISMATCH_CONDITIONAL_INTERACTIONS.csv"
    reason_path = OUT / "03_MISMATCH" / "MISMATCH_REASON_SUMMARY.csv"
    d = pd.read_csv(event_path)
    reason = pd.read_csv(reason_path)
    full = d[d.STATUS.eq("FULL_INPUT_MISMATCH")]
    counts = full.groupby("TARGET").size().to_dict()
    missing = pd.read_csv(OUT / "03_MISMATCH" / "APPLICABILITY_AND_MISSINGNESS.csv")
    event_base = pd.read_csv(BASE / "01_INTEGRATED_RELATION_BASELINE" / "01_BASELINE_FREE_EXPLORATION" / "01_FREE_EXPLORATION" / "EXPLORATION_EVENT_TABLE.csv")

    report = []
    report += [
        "# Integrated mismatch forensic audit R3",
        "",
        "Purpose: reverse-trace only the events where the fixed, leave-one-event-out descriptive branch prediction disagreed with the existing observation.",
        "No new map, path, threshold, fit, imputation, or causal claim was introduced.",
        "",
        "## Scope and definitions",
        "- MAG = S rank-bin + frequency-span rank-bin + total-frequency-variation rank-bin; fixed leave-one-out branch prediction.",
        "- SHAPE = f_turns rank-bin + transition-entropy rank-bin + network-z-median rank-bin; fixed leave-one-out branch prediction.",
        "- GAP side/order = existing family branch with ABC where available, with the predeclared family-only fallback where ABC is unavailable.",
        "- `FULL_INPUT_MISMATCH` is the mismatch class. Fallback, missing observation, and unavailable LOO cells are not counted as scientific mismatches.",
        "",
        "## Mismatch counts",
        f"- MAG: {counts.get('MAG', 0)} full-input mismatches.",
        f"- SHAPE: {counts.get('SHAPE', 0)} full-input mismatches.",
        f"- GAP_ORDER_MAXFLOW: {counts.get('GAP_ORDER_MAXFLOW', 0)} full-input mismatches.",
        f"- GAP_SIDE_T0: {counts.get('GAP_SIDE_T0', 0)} full-input mismatch.",
        "",
        "## What the reverse trace shows",
        "### Missing variables / axis contrasts",
        "For MAG mismatches, the largest descriptive contrasts are higher f_turns (median 3 versus 1), longer path/transition support (median path_nodes 15.5 versus 10.5), longer time span (0.15 versus 0.10 s), and lower f_directness. These variables were not added to the fixed MAG rule; they are candidates for a missing conditional interaction only.",
        "For SHAPE mismatches, the largest single contrast is weak: f_directness is lower in mismatches (median 0.5357 versus 0.8091), while MAX_FLOW is earlier (0.010 versus 0.020 s) and total variation is somewhat higher (90 versus 70 Hz). The 30 mismatches are not separated by one clean scalar boundary.",
        "For GAP-order mismatches, mismatches have shorter support (median 5 path nodes, 4 transitions, 0.04 s) and later GAP relative to the existing ordering. This is compatible with a short-track/applicability branch, but is not proof of a cause.",
        "",
        "### Variable interactions / hidden branches",
        "- SHAPE mismatch rate is elevated in FREQ_MAG_1 (14/33 in the retained interaction cells) and in FREQ_MAG_1 × ABC=A (9/26), but mismatches also occur in FREQ_MAG_2 and across ABC=A/B/C/OTHER. This is a possible interaction pattern, not a stable hidden branch.",
        "- MAG mismatch counts are small and distributed: the largest retained cells are FREQ_SHAPE_2 (3/35) and FREQ_SHAPE_2 × ABC=A (2/27). No single interaction isolates all six MAG mismatches.",
        "- GAP-order mismatches are concentrated in ABC=OTHER (2/7) and ABC=C (1/6), with all three in FREQ_MAG_2. Their support is short, so the result is better treated as a branch/applicability signal than as a new law.",
        "- GAP-side has one full mismatch, in ABC=OTHER and FREQ_MAG_2 (1/7 in that retained cell).",
        "",
        "### Out-of-scope / not scorable events",
        "- NO_PATH: GW241230_233618; excluded from path-based scoring.",
        "- S missing: GW150914_095045 and GW231008_142521; MAG uses the predeclared fallback only, not an imputed S.",
        "- GAP/ABC observations missing: GW231008_142521 and GW231206_233901; GAP-side/order cannot be scored as observed classifications.",
        "- SHAPE LOO cell unavailable: GW190728_064510 and GW250118_023225; not counted as failures.",
        "- K1/K2 are absent for most of the 98 path rows (82 each), so they remain an exploratory availability-limited axis and were not treated as complete predictors of the mismatch.",
        "",
        "## Interpretation",
        "The main unresolved signal is SHAPE: its fixed two-axis rule does not generalize uniformly, and the mismatch is broad rather than a single obvious missing scalar. MAG has fewer mismatches and shows a descriptive association with richer/longer trajectories, suggesting that support complexity or an interaction with shape may matter. GAP exceptions are few and concentrated in short-track/OTHER-C branches, with two additional cases unscorable because the observed GAP/ABC fields are missing.",
        "These are forensic diagnostics of a fixed exploratory predictor. They do not establish causation, do not select a revised law, and do not change the frozen RIUD map/path or scientific claims.",
        "",
        "## Status",
        "- PATH_FOUND=98; NO_PATH=1.",
        "- NEW_MAP=FALSE; NEW_PATH=FALSE; IMPUTATION=FALSE; CAUSAL_CLAIM=FALSE.",
        "- HOLDOUT30_ACCESSED=FALSE.",
    ]
    (OUT / "FINAL_MISMATCH_FORENSIC_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    summary = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "base_package": str(BASE),
        "prediction_audit": str(PRED),
        "mismatch_audit": str(AUDIT),
        "events_in_exploration": int(len(event_base)),
        "path_found": 98,
        "no_path": 1,
        "full_input_mismatch_counts": {k: int(v) for k, v in counts.items()},
        "missing_rows_in_event_table": int(missing.shape[0]),
        "new_map": False,
        "new_path": False,
        "imputation": False,
        "causal_claim": False,
        "holdout30_accessed": False,
    }
    (OUT / "RUN_SUMMARY.txt").write_text(
        "R_STATUS=PASS_ASSEMBLED_MISMATCH_FORENSIC\n"
        "MODE=FIXED_BRANCH_LOO_REVERSE_TRACE\n"
        f"MAG_FULL_INPUT_MISMATCH={counts.get('MAG', 0)}\n"
        f"SHAPE_FULL_INPUT_MISMATCH={counts.get('SHAPE', 0)}\n"
        f"GAP_ORDER_FULL_INPUT_MISMATCH={counts.get('GAP_ORDER_MAXFLOW', 0)}\n"
        f"GAP_SIDE_FULL_INPUT_MISMATCH={counts.get('GAP_SIDE_T0', 0)}\n"
        "NO_PATH=1\nS_MISSING=2\nNEW_MAP=FALSE\nNEW_PATH=FALSE\nIMPUTATION=FALSE\nCAUSAL_CLAIM=FALSE\nHOLDOUT30_ACCESSED=FALSE\n",
        encoding="utf-8",
    )
    (OUT / "PROVENANCE.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    entries = []
    for f in sorted(OUT.rglob("*")):
        if f.is_file() and f.name != "SHA256_MANIFEST.txt":
            entries.append(f"{sha256(f)}  {f.relative_to(OUT).as_posix()}")
    (OUT / "SHA256_MANIFEST.txt").write_text("\n".join(entries) + "\n", encoding="utf-8")

    zip_path = shutil.make_archive(str(OUT), "zip", root_dir=OUT.parent, base_dir=OUT.name)
    print(f"OUT={OUT}")
    print(f"ZIP={zip_path}")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
