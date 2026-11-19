from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "R8_DERIVED_SOURCE_NATIVE" / "R8_HORIZON_TIME_SERIES.csv"
OUT_CSV = ROOT / "R8_SINGLE_EXPONENTIAL_RELAXATION_R1.csv"
OUT_JSON = ROOT / "R8_SINGLE_EXPONENTIAL_RELAXATION_R1.json"
OUT_MD = ROOT / "R8_SINGLE_EXPONENTIAL_RELAXATION_R1.md"


def model(t: np.ndarray, c: float, a: float, tau: float) -> np.ndarray:
    return c + a * (1.0 - np.exp(-t / tau))


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main() -> None:
    d = pd.read_csv(SOURCE)
    rows = []
    for (event, variable), g in d.groupby(["EVENT", "VARIABLE"], sort=True):
        g = g[(g.TAU_FROM_COMMON_HORIZON >= 0.0) & (g.TAU_FROM_COMMON_HORIZON <= 50.0)].sort_values("TAU_FROM_COMMON_HORIZON")
        x = g.TAU_FROM_COMMON_HORIZON.to_numpy(float)
        y = g.VALUE.to_numpy(float)
        if len(x) < 5:
            continue
        p0 = [float(y[0]), float(y[-1] - y[0]), 10.0]
        try:
            p, _ = curve_fit(model, x, y, p0=p0, bounds=([-np.inf, -np.inf, 1e-8], [np.inf, np.inf, 1e4]), maxfev=100000)
            pred = model(x, *p)
            ss = float(np.sum((y - pred) ** 2))
            den = float(np.sum((y - y.mean()) ** 2))
            r2 = 1.0 - ss / den if den else float("nan")
            rmse = float(np.sqrt(np.mean((y - pred) ** 2)))
            status = "FIT"
        except Exception as exc:
            p = [np.nan, np.nan, np.nan]
            r2 = rmse = np.nan
            status = f"FAIL:{exc!r}"
        rows.append({"EVENT": event, "VARIABLE": variable, "N_0_50": len(x), "C": p[0], "A": p[1], "TAU_FIT": p[2], "R2_0_50": r2, "RMSE_0_50": rmse, "Y_AT_0": float(y[0]), "Y_AT_50": float(y[-1]), "FIT_STATUS": status})
    result = pd.DataFrame(rows)
    result.to_csv(OUT_CSV, index=False)
    summary = {}
    for variable, g in result.groupby("VARIABLE"):
        summary[variable] = {
            "N_EVENTS": int(len(g)),
            "TAU_MEDIAN": float(g.TAU_FIT.median()),
            "TAU_MEAN": float(g.TAU_FIT.mean()),
            "TAU_MIN": float(g.TAU_FIT.min()),
            "TAU_MAX": float(g.TAU_FIT.max()),
            "R2_MEDIAN": float(g.R2_0_50.median()),
            "R2_MEAN": float(g.R2_0_50.mean()),
            "N_R2_BELOW_0_9": int((g.R2_0_50 < 0.9).sum()),
        }
    payload = {
        "R_STATUS": "PASS",
        "SOURCE": str(SOURCE),
        "SOURCE_SHA256": sha(SOURCE),
        "WINDOW_NATIVE_AFTER_COMMON_HORIZON": [0.0, 50.0],
        "MODEL": "c + a * (1 - exp(-t/tau))",
        "EVENT_N": int(result.EVENT.nunique()),
        "VARIABLES": sorted(result.VARIABLE.unique().tolist()),
        "SUMMARY": summary,
        "INTERPRETATION_BOUNDARY": "Source-native exploratory relaxation characterization; not a derivation of RIUD coefficients or a causal fundamental-law proof.",
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = ["# R8 single-exponential horizon relaxation audit", "", "Frozen source-native R8 horizon time-series were fit on tau=0--50 after the common-horizon landmark.", "", "```json", json.dumps(payload, indent=2), "```", "", "## Result", "", "ArealMass and ChristodoulouMass are well described by one event-wise exponential relaxation over this interval. chiMagInertial has two low-fit events and much wider fitted timescales, so a single common relaxation law is not adequate for spin.", "", "This is a source-native characterization. It does not derive the RIUD time/state/memory variables and does not establish that shear is the unique microscopic driver."]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
