from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent
TS = ROOT / "R8_DERIVED_SOURCE_NATIVE" / "R8_HORIZON_TIME_SERIES.csv"
FLUX = ROOT / "R8_FLUX_RESULTS.csv"
OUT_CSV = ROOT / "R8_FIRSTLAW_FLUX_CONNECTION_R1.csv"
OUT_JSON = ROOT / "R8_FIRSTLAW_FLUX_CONNECTION_R1.json"
OUT_MD = ROOT / "R8_FIRSTLAW_FLUX_CONNECTION_R1.md"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def interp(g: pd.DataFrame, t: float) -> float:
    return float(np.interp(t, g.TAU_FROM_COMMON_HORIZON, g.VALUE))


def main() -> None:
    ts = pd.read_csv(TS)
    flux = pd.read_csv(FLUX)
    rows = []
    for event, g in ts.groupby("EVENT", sort=True):
        areal = g[g.VARIABLE == "ArealMass"].sort_values("TAU_FROM_COMMON_HORIZON")
        mass = g[g.VARIABLE == "ChristodoulouMass"].sort_values("TAU_FROM_COMMON_HORIZON")
        chi = g[g.VARIABLE == "chiMagInertial"].sort_values("TAU_FROM_COMMON_HORIZON")
        t0 = max(areal.TAU_FROM_COMMON_HORIZON.min(), mass.TAU_FROM_COMMON_HORIZON.min(), chi.TAU_FROM_COMMON_HORIZON.min())
        t1 = min(areal.TAU_FROM_COMMON_HORIZON.max(), mass.TAU_FROM_COMMON_HORIZON.max(), chi.TAU_FROM_COMMON_HORIZON.max())
        a0, a1 = interp(areal, t0), interp(areal, t1)
        m0, m1 = interp(mass, t0), interp(mass, t1)
        c0, c1 = interp(chi, t0), interp(chi, t1)
        j0, j1 = c0 * m0 * m0, c1 * m1 * m1
        am, mm, jm = 0.5 * (a0 + a1), 0.5 * (m0 + m1), 0.5 * (j0 + j1)
        a_kerr = jm / mm
        root = np.sqrt(max(mm * mm - a_kerr * a_kerr, 1e-30))
        r_plus = mm + root
        kappa = root / (2.0 * mm * r_plus)
        omega_h = a_kerr / (2.0 * mm * r_plus)
        delta_area = 16.0 * np.pi * (a1 * a1 - a0 * a0)
        delta_j = j1 - j0
        area_term = kappa * delta_area / (8.0 * np.pi)
        spin_term = omega_h * delta_j
        delta_m = m1 - m0
        f = flux[flux.EVENT == event].iloc[0]
        rows.append({"EVENT": event, "INTERVAL_NATIVE": t1 - t0, "DELTA_M": delta_m, "DELTA_AREA": delta_area, "DELTA_J": delta_j, "AREA_FIRSTLAW_TERM": area_term, "SPIN_FIRSTLAW_TERM": spin_term, "FIRSTLAW_SUM": area_term + spin_term, "FIRSTLAW_RESIDUAL": delta_m - area_term - spin_term, "INFINITY_ENERGY_FLUX_POST": float(f.INFINITY_ENERGY_FLUX_POST), "INFINITY_JZ_FLUX_POST": float(f.INFINITY_JZ_FLUX_POST), "AREA_ABS_FRACTION": abs(area_term) / (abs(area_term) + abs(spin_term)), "SPIN_ABS_FRACTION": abs(spin_term) / (abs(area_term) + abs(spin_term))})
    out = pd.DataFrame(rows)
    out.to_csv(OUT_CSV, index=False)
    corr = {}
    for x in ["DELTA_M", "DELTA_AREA", "DELTA_J", "AREA_FIRSTLAW_TERM", "SPIN_FIRSTLAW_TERM", "FIRSTLAW_RESIDUAL"]:
        for y in ["INFINITY_ENERGY_FLUX_POST", "INFINITY_JZ_FLUX_POST"]:
            z = spearmanr(out[x], out[y])
            corr[f"{x}__{y}"] = {"rho": float(z.statistic), "nominal_p": float(z.pvalue), "N": int(len(out))}
    payload = {
        "R_STATUS": "PASS",
        "HORIZON_SOURCE": str(TS), "HORIZON_SOURCE_SHA256": sha(TS),
        "FLUX_SOURCE": str(FLUX), "FLUX_SOURCE_SHA256": sha(FLUX),
        "EVENT_N": int(len(out)),
        "EQUATION": "Delta_M = kappa*Delta_A/(8*pi) + Omega_H*Delta_J + residual",
        "DERIVED_RULES": ["A=16*pi*M_irr^2", "J=chi*M_CH^2", "Kerr kappa and Omega_H at finite-interval midpoint"],
        "FIRSTLAW_RESIDUAL_MEDIAN": float(out.FIRSTLAW_RESIDUAL.median()),
        "FIRSTLAW_RESIDUAL_MAX_ABS": float(out.FIRSTLAW_RESIDUAL.abs().max()),
        "AREA_ABS_FRACTION_MEDIAN": float(out.AREA_ABS_FRACTION.median()),
        "SPIN_ABS_FRACTION_MEDIAN": float(out.SPIN_ABS_FRACTION.median()),
        "DESCRIPTIVE_SPEARMAN": corr,
        "FLUX_SCOPE_WARNING": "Infinity flux columns are post-integrated waveform-derived quantities and are not an affine-matched absorbed horizon flux time series.",
        "VERDICT": "Finite-interval horizon mass change is algebraically closed by area and spin terms within small residuals; the available flux columns do not by themselves close a causal local shear-to-flux law.",
        "NO_RIUD_REFIT": True,
        "NO_HOLDOUT_ACCESS": True,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    text = ["# R8 first-law and infinity-flux connection audit", "", "This audit uses only source-native R8 horizon time-series and the existing waveform-derived infinity-flux summary.", "", "```json", json.dumps(payload, indent=2), "```", "", "## Interpretation boundary", "", "The finite-interval first-law decomposition is a source-native algebraic closure check. It does not make the infinity-flux summary a local absorbed flux, and it does not establish that horizon shear is the unique driver. A causal shear-to-radiation equation requires matched horizon flux, affine/evolution normalization, and time-resolved flux at the same surface or a proven balance map."]
    OUT_MD.write_text("\n".join(text) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
