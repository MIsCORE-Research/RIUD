from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pandas as pd


PACKAGE = Path(__file__).resolve().parent
ENGINE = PACKAGE / "FROZEN_ENGINE"
OUTPUT = PACKAGE / "OUTPUT"
REFERENCE = PACKAGE / "CANONICAL_REFERENCE"
PHYSICAL = PACKAGE / "INPUTS" / "HOLDOUT5_R40_PHYSICAL_BINDING.csv"


def load_frozen_replay():
    path = ENGINE / "run_holdout5_r40_exact_replay.py"
    spec = importlib.util.spec_from_file_location("frozen_holdout5_replay", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    mod = load_frozen_replay()
    # Only I/O roots are redirected. The replay functions and constants remain
    # the frozen source copied into FROZEN_ENGINE.
    mod.OUT = OUTPUT
    mod.COVERAGE_REPLAY = REFERENCE
    mod.R5 = ENGINE
    mod.R9 = ENGINE / "R9"
    mod.R40 = ENGINE
    mod.R6 = ENGINE / "R6"
    mod.R8 = ENGINE / "R8"

    physical = pd.read_csv(PHYSICAL)
    physical_lookup = physical.set_index("EVENT")

    def frozen_physical_row(event: str):
        if event not in physical_lookup.index:
            raise RuntimeError(f"HOLDOUT5_PHYSICAL_BINDING_MISSING={event}")
        return {"EVENT": event, **physical_lookup.loc[event].to_dict()}

    mod.physical_row = frozen_physical_row
    OUTPUT.mkdir(parents=True, exist_ok=True)
    mod.main()


if __name__ == "__main__":
    main()
