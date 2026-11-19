"""R40 Holdout-5 Fast-Track Reproduction Runner.

Executes the frozen R40 forward likelihood engine across the five holdout
gravitational wave events (GW241114_024711, GW240830_211120, GW240612_081540,
GW241130_110422, GW250119_190238) and compares the computed Delta log-likelihood
and trajectory metrics against the canonical reference outputs.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
PAPER4_DIR = ROOT / "SEND" / "PAPER_4"
ENGINE_DIR = PAPER4_DIR / "FROZEN_ENGINE"
INPUT_DIR = PAPER4_DIR / "INPUTS"
REFERENCE_DIR = PAPER4_DIR / "CANONICAL_REFERENCE"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def load_frozen_engine():
    engine_file = ENGINE_DIR / "run_holdout5_r40_exact_replay.py"
    if not engine_file.exists():
        raise FileNotFoundError(f"Frozen engine not found: {engine_file}")
    spec = importlib.util.spec_from_file_location("frozen_holdout5_replay", engine_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module spec from {engine_file}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_reproduction() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    mod = load_frozen_engine()

    # Route I/O without modifying frozen source packages
    mod.OUT = OUTPUT_DIR
    mod.COVERAGE_REPLAY = REFERENCE_DIR
    mod.R5 = ENGINE_DIR
    mod.R9 = ENGINE_DIR / "R9"
    mod.R40 = ENGINE_DIR
    mod.R6 = ENGINE_DIR / "R6"
    mod.R8 = ENGINE_DIR / "R8"

    binding_file = INPUT_DIR / "HOLDOUT5_R40_PHYSICAL_BINDING.csv"
    if not binding_file.exists():
        raise FileNotFoundError(f"Physical binding file not found: {binding_file}")
    physical_df = pd.read_csv(binding_file).set_index("EVENT")

    def lookup_physical_row(event: str) -> dict:
        if event not in physical_df.index:
            raise KeyError(f"Event {event} missing in physical binding table")
        return {"EVENT": event, **physical_df.loc[event].to_dict()}

    mod.physical_row = lookup_physical_row

    # Run frozen forward engine
    mod.main()

    # Automatically remove legacy chat artifact if generated
    legacy_chat = OUTPUT_DIR / "SEND_TO_CHAT.txt"
    if legacy_chat.exists():
        legacy_chat.unlink()

    # Verify produced likelihood table against canonical reference
    result_csv = OUTPUT_DIR / "HOLDOUT5_R40_W1_W4_EXACT_LIKELIHOOD.csv"
    ref_csv = REFERENCE_DIR / "HOLDOUT5_R40_W1_W4_EXACT_LIKELIHOOD.csv"

    if not result_csv.exists() or not ref_csv.exists():
        print("ERROR: Result or reference file missing.", file=sys.stderr)
        return 1

    df_res = pd.read_csv(result_csv)
    df_ref = pd.read_csv(ref_csv)

    print("")
    print("MIsCORE-RIUD R40 Fast-Track Reproduction Report")
    print("-" * 72)
    print(f"Events evaluated (N=5): {', '.join(mod.EVENTS)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("-" * 72)
    print(f"{'Window':<18} {'DeltaLL (Obs)':>14} {'DeltaLL (Ref)':>14} {'Diff':>12} {'Status':>10}")
    print("-" * 72)

    all_passed = True
    for idx, row in df_res.iterrows():
        w_name = str(row["MAP_NAME"])
        obs_dll = float(row["DELTA_LOGLIK"])
        ref_row = df_ref[df_ref["MAP_NAME"] == w_name]
        if ref_row.empty:
            print(f"{w_name:<18} {obs_dll:14.6f} {'MISSING':>14} {'N/A':>12} {'FAIL':>10}")
            all_passed = False
            continue
        ref_dll = float(ref_row["DELTA_LOGLIK"].iloc[0])
        diff = abs(obs_dll - ref_dll)
        passed = diff < 1e-5
        if not passed:
            all_passed = False
        status_str = "PASS" if passed else "FAIL"
        print(f"{w_name:<18} {obs_dll:14.6f} {ref_dll:14.6f} {diff:12.2e} {status_str:>10}")

    print("-" * 72)
    if all_passed:
        print("VERDICT: PASS (All windows match canonical reference within numerical tolerance)")
        return 0
    else:
        print("VERDICT: FAIL (Numerical discrepancy detected against canonical reference)")
        return 1


if __name__ == "__main__":
    sys.exit(run_reproduction())
