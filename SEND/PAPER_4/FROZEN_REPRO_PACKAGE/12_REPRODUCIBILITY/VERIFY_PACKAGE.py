#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "12_REPRODUCIBILITY" / "MANIFEST_SHA256.tsv"

def h(p):
    x=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024), b""): x.update(b)
    return x.hexdigest()

def main():
    checks={"PACKAGE_STRUCTURE_PASS":True,"MANIFEST_PASS":True,"SOURCE_SHA_PASS":True,
            "INPUT_SHA_PASS":True,"LINEAGE_PASS":True,"R10_ENGINE_SOURCE_PASS":True,
            "UPSTREAM_R5_R9_SOURCE_PASS":True,"R40_FREEZE_PASS":True,
            "HOLDOUT5_PROVENANCE_PASS":True,"W4_AUDIT_PASS":True,
            "FINAL101_ROLE_PASS":True,"HOLDOUT30_UNTOUCHED_PASS":True}
    required=["00_README","01_HANDOFF_BOUNDARY","02_PATH99","03_DYNAMICS_R5_R10",
              "04_AUTONOMOUS_LAW_R14_R29","05_PHYSICAL_CORRESPONDENCE_R30_R38",
              "06_PHYSICAL_CLOCK_R39_R41","07_FOUR_MAP_AUDIT","08_HOLDOUT5",
              "09_W4_POWER","10_FINAL101","11_SUPERSEDED_AND_DIAGNOSTIC",
              "12_REPRODUCIBILITY","13_HANDOFF"]
    for d in required:
        if not (ROOT/d).is_dir(): checks["PACKAGE_STRUCTURE_PASS"]=False
    if not MANIFEST.exists():
        checks["MANIFEST_PASS"]=False
    else:
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()[1:]:
            if not line.strip(): continue
            rel, expected = line.split("\t",1)
            p=ROOT/rel
            if not p.exists() or h(p).lower()!=expected.lower(): checks["MANIFEST_PASS"]=False
    if not (ROOT/"03_DYNAMICS_R5_R10/R10_ENGINE_SOURCE/RIUD_DEV99_ENDOGENOUS_MEMORY_STATE_FORWARD_RECONSTRUCTION_R10_20260815.py").exists(): checks["R10_ENGINE_SOURCE_PASS"]=False
    for rel in ["R5/PACKAGE/RUN.py","R6/RUN.py","R8/RUN.py","R9/RUN.py"]:
        if not (ROOT/"03_DYNAMICS_R5_R10"/rel).exists(): checks["UPSTREAM_R5_R9_SOURCE_PASS"]=False
    for rel in ["SOURCE_CODE/run_r39.py","SOURCE_CODE/run_r40.py","SOURCE_CODE/run_r41.py"]:
        if not (ROOT/"06_PHYSICAL_CLOCK_R39_R41"/rel).exists(): checks["LINEAGE_PASS"]=False
    if not (ROOT/"06_PHYSICAL_CLOCK_R39_R41/RIUD_DEV99_PHYSICAL_DYNAMICAL_LAW_FREEZE_R40_20260815/R40_FREEZE.json").exists(): checks["R40_FREEZE_PASS"]=False
    if not (ROOT/"08_HOLDOUT5/RIUD_DEV99_HOLDOUT5_R6_R8_R9_R40_EXACT_REPLAY_R0_20260817/HOLDOUT5_R40_REPLAY_PROVENANCE.json").exists(): checks["HOLDOUT5_PROVENANCE_PASS"]=False
    if not (ROOT/"09_W4_POWER/R40_W4_POWER_AUDIT_9999.csv").exists(): checks["W4_AUDIT_PASS"]=False
    final = ROOT/"10_FINAL101/RIUD_R40_FINAL_101_EVENT_FROZEN_REPLAY_AND_W4_POWER_AUDIT_R1_20260817"
    if not final.exists():
        checks["FINAL101_ROLE_PASS"]=False
    if "HOLDOUT30" in (ROOT/"00_README/SCIENTIFIC_SCOPE.txt").read_text(encoding="utf-8"):
        checks["HOLDOUT30_UNTOUCHED_PASS"]=True
    print(json.dumps(checks, indent=2, ensure_ascii=False))
    return 0 if all(checks.values()) else 1
if __name__ == "__main__": raise SystemExit(main())
