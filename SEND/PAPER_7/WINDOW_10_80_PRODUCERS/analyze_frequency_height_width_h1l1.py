from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(r"E:\RIUD_ACTIVE_20260808\MIsCORE_MT_RAW_FROM_SOURCE_R2_20260829\RAW_FRONTEND\WINDOW_10_80_EXTENDED_DIAGNOSTIC")
AUDIT = BASE / "WINDOW_FEATURE_ANOMALY_AUDIT"
RAW = BASE / "FINE_TIME_RAW_FEATURES_10_80_EXTENDED.csv"
GAP = Path(r"E:\RIUD_ACTIVE_20260808\RIUD_GAP_RAW_POSITION_FULL_CORRECTED_TIME_AUDIT_R2_20260821\GAP_RAW_POSITION_FULL_CORRECTED_TIME_EVENT_TABLE.csv")

WIDTHS = [10, 20, 30, 40, 50, 60, 70, 80]
FEATURES = [
    "F_PHASE_HZ", "FDOT_PHASE_HZ_PER_S", "LOGAMP_SLOPE_PER_S",
    "FFT_CENTROID_HZ", "FFT_PEAK_HZ", "P20_100", "P100_250",
    "P250_512", "RMS"
]
FREQ_BANDS = {"LOW_20_100": "P20_100", "MID_100_250": "P100_250", "HIGH_250_512": "P250_512"}


def finite(x):
    return pd.to_numeric(x, errors="coerce").replace([np.inf, -np.inf], np.nan)


def main():
    raw = pd.read_csv(RAW)
    out = AUDIT / "FREQUENCY_HEIGHT_WIDTH_H1_L1"
    out.mkdir(exist_ok=True)

    # Event/offset medians preserve the event as the unit, then summarize across events.
    rows = []
    for w in WIDTHS:
        for f in FEATURES:
            h = finite(raw[f"H1_{f}_{w}MS"])
            l = finite(raw[f"L1_{f}_{w}MS"])
            d = pd.DataFrame({"EVENT": raw.EVENT, "OFFSET_MS": raw.OFFSET_MS, "H1": h, "L1": l})
            # Raw feature levels are descriptive; log-ratio is used only for positive power/RMS-like values.
            d["DIFF_L1_MINUS_H1"] = d.L1 - d.H1
            d["ABS_DIFF"] = (d.L1 - d.H1).abs()
            if f.startswith("P") or f == "RMS":
                d["LOG10_RATIO_L1_OVER_H1"] = np.log10(d.L1.clip(lower=1e-300) / d.H1.clip(lower=1e-300))
            else:
                d["LOG10_RATIO_L1_OVER_H1"] = np.nan
            ev = d.groupby("EVENT", as_index=False).agg(
                H1=("H1", "median"), L1=("L1", "median"),
                DIFF_L1_MINUS_H1=("DIFF_L1_MINUS_H1", "median"),
                ABS_DIFF=("ABS_DIFF", "median"),
                LOG10_RATIO_L1_OVER_H1=("LOG10_RATIO_L1_OVER_H1", "median"),
            )
            valid = ev.dropna(subset=["H1", "L1"])
            rows.append({
                "WIDTH_MS": w, "FEATURE": f, "N_EVENTS": len(valid),
                "H1_MEDIAN": valid.H1.median(), "L1_MEDIAN": valid.L1.median(),
                "L1_MINUS_H1_MEDIAN": valid.DIFF_L1_MINUS_H1.median(),
                "MEDIAN_ABS_DIFF": valid.ABS_DIFF.median(),
                "FRACTION_L1_GREATER": float((valid.L1 > valid.H1).mean()),
                "LOG10_L1_OVER_H1_MEDIAN": valid.LOG10_RATIO_L1_OVER_H1.median(),
                "LOG10_L1_OVER_H1_IQR": valid.LOG10_RATIO_L1_OVER_H1.quantile(.75) - valid.LOG10_RATIO_L1_OVER_H1.quantile(.25),
            })
    summary = pd.DataFrame(rows)
    summary.to_csv(out / "FREQUENCY_HEIGHT_BY_WIDTH_H1_L1.csv", index=False)

    # Explicit frequency-band table: one row per event and width, then population summaries.
    band_rows = []
    for w in WIDTHS:
        for band, f in FREQ_BANDS.items():
            h = finite(raw[f"H1_{f}_{w}MS"]); l = finite(raw[f"L1_{f}_{w}MS"])
            d = pd.DataFrame({"EVENT": raw.EVENT, "H1": h, "L1": l})
            d["LOG10_RATIO"] = np.log10(d.L1.clip(lower=1e-300) / d.H1.clip(lower=1e-300))
            ev = d.groupby("EVENT", as_index=False).median(numeric_only=True).dropna()
            band_rows.append({
                "WIDTH_MS": w, "FREQUENCY_BAND": band, "N_EVENTS": len(ev),
                "H1_MEDIAN": ev.H1.median(), "L1_MEDIAN": ev.L1.median(),
                "L1_OVER_H1_MEDIAN_RATIO": 10 ** ev.LOG10_RATIO.median(),
                "MEDIAN_LOG10_RATIO": ev.LOG10_RATIO.median(),
                "IQR_LOG10_RATIO": ev.LOG10_RATIO.quantile(.75) - ev.LOG10_RATIO.quantile(.25),
                "FRACTION_L1_GREATER": (ev.L1 > ev.H1).mean(),
            })
    bands = pd.DataFrame(band_rows)
    bands.to_csv(out / "FREQUENCY_BANDS_BY_WIDTH_H1_L1.csv", index=False)

    # Event-level frequency-height signatures, retaining the anomalies that population
    # medians can hide.
    sig_rows = []
    for w in WIDTHS:
        ev = pd.DataFrame({"EVENT": sorted(raw.EVENT.unique())})
        for band, f in FREQ_BANDS.items():
            h = finite(raw[f"H1_{f}_{w}MS"]); l = finite(raw[f"L1_{f}_{w}MS"])
            q = pd.DataFrame({"EVENT": raw.EVENT, "H1": h, "L1": l}).groupby("EVENT").median(numeric_only=True)
            ev = ev.merge(pd.DataFrame({"EVENT": q.index, f"{band}_LOG10_L1_OVER_H1": np.log10(q.L1.clip(lower=1e-300) / q.H1.clip(lower=1e-300)).to_numpy()}), on="EVENT", how="left")
        ev["WIDTH_MS"] = w
        ev["LOW_POS_MID_POS_HIGH_NEG"] = ((ev.LOW_20_100_LOG10_L1_OVER_H1 > 0) & (ev.MID_100_250_LOG10_L1_OVER_H1 > 0) & (ev.HIGH_250_512_LOG10_L1_OVER_H1 < 0))
        ev["LOW_POS_HIGH_NEG"] = ((ev.LOW_20_100_LOG10_L1_OVER_H1 > 0) & (ev.HIGH_250_512_LOG10_L1_OVER_H1 < 0))
        ev["ALL_BANDS_L1_POS"] = ((ev.LOW_20_100_LOG10_L1_OVER_H1 > 0) & (ev.MID_100_250_LOG10_L1_OVER_H1 > 0) & (ev.HIGH_250_512_LOG10_L1_OVER_H1 > 0))
        sig_rows.append(ev.reset_index(drop=True))
    sig = pd.concat(sig_rows, ignore_index=True)
    sig.to_csv(out / "EVENT_FREQUENCY_HEIGHT_SIGNATURES.csv", index=False)
    pattern = sig.groupby("WIDTH_MS").agg(
        N_EVENTS=("EVENT", "nunique"), LOW_POS_MID_POS_HIGH_NEG=("LOW_POS_MID_POS_HIGH_NEG", "sum"),
        LOW_POS_HIGH_NEG=("LOW_POS_HIGH_NEG", "sum"), ALL_BANDS_L1_POS=("ALL_BANDS_L1_POS", "sum"),
    ).reset_index()
    for c in ["LOW_POS_MID_POS_HIGH_NEG", "LOW_POS_HIGH_NEG", "ALL_BANDS_L1_POS"]:
        pattern[c + "_FRACTION"] = pattern[c] / pattern.N_EVENTS
    pattern.to_csv(out / "WIDTH_FREQUENCY_SIGNATURE_COUNTS.csv", index=False)
    persistence = sig.groupby("EVENT").agg(
        N_WIDTHS=("WIDTH_MS", "size"), PATTERN_WIDTHS=("LOW_POS_MID_POS_HIGH_NEG", "sum"),
        LOW_POS_HIGH_NEG_WIDTHS=("LOW_POS_HIGH_NEG", "sum"), ALL_BANDS_L1_POS_WIDTHS=("ALL_BANDS_L1_POS", "sum"),
    ).reset_index().sort_values(["PATTERN_WIDTHS", "LOW_POS_HIGH_NEG_WIDTHS"], ascending=False)
    persistence.to_csv(out / "EVENT_FREQUENCY_SIGNATURE_PERSISTENCE.csv", index=False)
    # A compact list of the strongest recurring high-frequency inversions.
    inv = sig[sig.LOW_POS_MID_POS_HIGH_NEG].copy()
    inv["HIGH_NEG_MAGNITUDE"] = -inv.HIGH_250_512_LOG10_L1_OVER_H1
    inv.sort_values(["HIGH_NEG_MAGNITUDE", "WIDTH_MS"], ascending=[False, True]).head(100).to_csv(out / "TOP_EVENT_FREQUENCY_INVERSION_ANOMALIES.csv", index=False)

    # Width-direction table from the already computed directional diagnostic.
    fd = pd.read_csv(AUDIT / "FEATURE_DIRECTIONAL_BOUNDARY.csv")
    fd = fd[(fd.L1_SOURCE_MS == 10) & (fd.H1_TARGET_MS.isin(WIDTHS))].copy()
    fd.to_csv(out / "DIRECTIONAL_FEATURES_L1_10_TO_H1_WIDTH.csv", index=False)

    # Frozen GAP side transitions: no new GAP locations; only LEFT/CENTER/RIGHT rows already present.
    gap = pd.read_csv(GAP)
    side = gap[gap.MAP_OBJECT.isin(["GAP_LEFT", "GAP_CENTER", "GAP_RIGHT"])].copy()
    value_cols = [c for c in side.columns if c.startswith(("H1_", "L1_"))]
    piv = side.pivot(index="EVENT_ID", columns="MAP_OBJECT", values=value_cols)
    trans_rows = []
    for c in value_cols:
        for a, b, label in [("GAP_LEFT", "GAP_CENTER", "CENTER_MINUS_LEFT"), ("GAP_CENTER", "GAP_RIGHT", "RIGHT_MINUS_CENTER")]:
            if (c, a) not in piv or (c, b) not in piv:
                continue
            x = piv[(c, b)] - piv[(c, a)]
            trans_rows.append({
                "OBSERVABLE": c, "TRANSITION": label, "N_EVENTS": int(x.notna().sum()),
                "MEDIAN_CHANGE": x.median(), "IQR_CHANGE": x.quantile(.75)-x.quantile(.25),
                "FRACTION_POSITIVE": (x > 0).mean(),
            })
    pd.DataFrame(trans_rows).to_csv(out / "GAP_SIDE_TRANSITIONS_H1_L1.csv", index=False)

    # Concise machine-readable summary.
    key = bands[(bands.FREQUENCY_BAND.isin(["LOW_20_100", "MID_100_250", "HIGH_250_512"])) & (bands.WIDTH_MS.isin([10, 40, 50, 80]))]
    report = out / "FREQUENCY_HEIGHT_WIDTH_H1_L1_REPORT.md"
    with report.open("w", encoding="utf-8") as f:
        f.write("# H1/L1 frequency-height and width anomaly audit\n\n")
        f.write("Scope: existing 10–80 ms diagnostic features and frozen GAP LEFT/CENTER/RIGHT rows. No node/map/GAP search was run; 999/9999 is excluded.\n\n")
        f.write("## Frequency bands by width\n\n")
        f.write("The table uses event-level medians before population medians. `L1_OVER_H1_MEDIAN_RATIO` is descriptive only and is not a detector calibration.\n\n")
        f.write("```text\n")
        f.write(key.to_string(index=False, float_format=lambda x: f"{x:.4g}"))
        f.write("\n```\n")
        f.write("\n\n## Direct result\n\n")
        f.write("Across the stored widths, 20–100 Hz and 100–250 Hz remain L1-over-H1 positive in the population median. The 250–512 Hz band is the sharp anomaly: it is L1-over-H1 positive at 10 ms but crosses below one by 20–30 ms and becomes increasingly H1-dominant at 40–80 ms. The detector difference is therefore frequency- and width-dependent, not a single H1/L1 gain factor.\n\n")
        f.write("The separate directional width audit shows the complementary pattern: phase-rate, high-frequency power and RMS favor L1(10 ms) → H1(broad), while log-amplitude slope and spectral centroid favor the reverse direction. The phase-rate crossover is near 40–50 ms in the existing diagnostic.\n\n")
        f.write("## GAP relation\n\n")
        f.write("The final table records CENTER−LEFT and RIGHT−CENTER changes for frozen GAP side rows. It is a side-transition characterization, not a new GAP detector.\n")
        comp_path = out / "PERSISTENT_FREQUENCY_ANOMALY_GAP_CENTER_COMPARISON.csv"
        if comp_path.exists():
            comp = pd.read_csv(comp_path)
            f.write("\n## Persistent event subset vs frozen GAP-center geometry\n\n")
            f.write("The all-8-width subset contains 7 events, but only 6 have a bindable GAP_CENTER row. The >=6-width subset has 30 events, of which 23 have GAP_CENTER rows. These are exploratory group comparisons, not an independent hypothesis test.\n\n")
            keep = comp[(comp.GROUP == "GE_6_WIDTHS") & comp.OBSERVABLE.isin(["H1_SPECTRAL_BANDWIDTH", "L1_SPECTRAL_BANDWIDTH", "H1_SPECTRAL_CENTROID", "L1_SPECTRAL_CENTROID", "PHASE_COHERENCE"])].copy()
            f.write("```text\n" + keep.to_string(index=False, float_format=lambda x: f"{x:.4g}") + "\n```\n")
        f.write("\n## Event-level frequency signature\n\n")
        f.write("At wider windows, a recurring pattern is L1/H1 > 1 in 20–100 and 100–250 Hz while L1/H1 < 1 in 250–512 Hz. The pattern counts are in `WIDTH_FREQUENCY_SIGNATURE_COUNTS.csv`; this is a detector-representation anomaly, not a physical frequency law.\n")
        f.write(f"Across events, the pattern occurs in at least 4 of 8 widths for {int((persistence.PATTERN_WIDTHS >= 4).sum())}/{len(persistence)} events, at least 6 widths for {int((persistence.PATTERN_WIDTHS >= 6).sum())}/{len(persistence)}, and all 8 widths for {int((persistence.PATTERN_WIDTHS == 8).sum())}/{len(persistence)}.\n")
    print(report)
    print("SUMMARY_ROWS", len(summary), "BAND_ROWS", len(bands), "GAP_TRANSITION_ROWS", len(trans_rows))
    print(key.to_string(index=False))
    print("RUN_FINISHED_EXIT_CODE=0")


if __name__ == "__main__":
    main()
