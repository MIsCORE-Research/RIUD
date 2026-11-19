import argparse
import csv
import sys
from pathlib import Path

import numpy as np

PKG = Path.home() / "prism2_nextgate_20260629_221648/package"
sys.path.insert(0, str(PKG))

import prism_modelbank as pm
import prism_residual_burst_scan as rb
import prism_residual_template_bank as tb


OUTCSV = Path.home() / "PRISM_2P2_FREQUENCY_RIDGE_LOCKED_VALIDATION_20260702.csv"
OUTSUMMARY = Path.home() / "PRISM_2P2_FREQUENCY_RIDGE_LOCKED_VALIDATION_20260702_SUMMARY.txt"

# Two anchors:
# 1) PRISM 2.1 ring-template anchor
# 2) PRISM 2.2-alpha template-free local-coherence anchor
ANCHORS = [
    {
        "anchor": "ring_ref_center_m0p050_w0p030",
        "center": -0.050,
        "scale": 0.030,
    },
    {
        "anchor": "tf_local_center_m0p060_w0p015",
        "center": -0.060,
        "scale": 0.015,
    },
]

PHYSICAL_LAGS = np.arange(-0.012, 0.0121, 0.001)

SLIDES = np.concatenate([
    np.arange(-2.00, -0.025, 0.01),
    np.arange(+0.025, +2.001, 0.01),
])


def projection(x, temp):
    return float(np.sum(x * temp))


def coh_same_opp(zH, zL):
    same = abs((zH + zL) / np.sqrt(2.0))
    opp = abs((zH - zL) / np.sqrt(2.0))

    if same >= opp:
        return float(same), "same", float(same), float(opp)

    return float(opp), "opposite", float(same), float(opp)


def build_ifos_safe(event_strains, psds, cfg):
    try:
        return pm.build_ifos(event_strains, psds, cfg)
    except TypeError:
        return pm.build_ifos(event_strains, psds)


def load_residual_series(event, band_low, band_high):
    cfg = pm.get_event_config(event)
    gps = float(cfg["gps"])

    params, src = rb.load_gr_params(event, gps)

    required = ["mass_1", "mass_2", "luminosity_distance", "geocent_time", "phase"]
    missing = [k for k in required if k not in params]
    if missing:
        raise RuntimeError(f"{event}: missing GR params: {missing}")

    print(f"EVENT={event}", flush=True)
    print(f"GPS={gps}", flush=True)
    print(f"GR_SOURCE={src}", flush=True)
    print(
        f"mass_1={params.get('mass_1')} mass_2={params.get('mass_2')} "
        f"total={float(params['mass_1']) + float(params['mass_2'])}",
        flush=True,
    )

    event_strains = pm.load_event_strains(event, gps)

    windows = pm.make_psd_windows(gps, "scout")
    window_name, psd_window = list(windows.items())[0]
    print(f"PSD={window_name} {psd_window}", flush=True)

    psds = pm.load_psds(event, gps, window_name, psd_window)
    ifos = build_ifos_safe(event_strains, psds, cfg)

    wfgen = pm.make_waveform_generator()
    pols = wfgen.frequency_domain_strain(params)

    detector_signals = {}
    for ifo in ifos:
        detector_signals[ifo.name] = ifo.get_detector_response(pols, params)

    n_time = int(pm.DURATION * pm.SAMPLING_FREQUENCY)
    t = np.arange(n_time) / pm.SAMPLING_FREQUENCY - pm.DURATION / 2.0

    td = {}
    for ifo in ifos:
        td[ifo.name] = rb.normalized_band_residual_time_series(
            ifo=ifo,
            signal_fd=detector_signals[ifo.name],
            band=(band_low, band_high),
            n_time=n_time,
        )

    if "H1" not in td or "L1" not in td:
        raise RuntimeError(f"{event}: missing H1/L1 residual series")

    meta = {
        "event": event,
        "gps": gps,
        "gr_source": src,
        "psd_window_name": window_name,
        "psd_start": psd_window[0],
        "psd_end": psd_window[1],
        "band_low": band_low,
        "band_high": band_high,
        "mass_1": params.get("mass_1", ""),
        "mass_2": params.get("mass_2", ""),
        "total_mass": float(params["mass_1"]) + float(params["mass_2"]),
        "geocent_time": params.get("geocent_time", ""),
    }

    return t, td["H1"], td["L1"], meta


def score_one_frequency(t, xH, xL, center, scale, f0, slide=0.0):
    """
    Ring-template frequency ridge score.
    Time anchor and scale are fixed.
    Frequency f0 is scanned.
    Best physical lag and best parity mode are recorded.
    """
    tempH = tb.make_template(t, "ring", center, scale, f0)
    zH = projection(xH, tempH)

    best = None

    for lag in PHYSICAL_LAGS:
        tempL = tb.make_template(t, "ring", center + lag + slide, scale, f0)
        zL = projection(xL, tempL)

        coh, mode, same, opp = coh_same_opp(zH, zL)

        row = {
            "f0": float(f0),
            "lag": float(lag),
            "slide": float(slide),
            "coherent": float(coh),
            "mode": mode,
            "zH1": float(zH),
            "zL1": float(zL),
            "same_score": float(same),
            "opposite_score": float(opp),
        }

        if best is None or row["coherent"] > best["coherent"]:
            best = row

    return best


def scan_frequency_grid(t, xH, xL, center, scale, freqs, slide=0.0, keep_all=False):
    rows = []
    best = None

    for f0 in freqs:
        row = score_one_frequency(
            t=t,
            xH=xH,
            xL=xL,
            center=center,
            scale=scale,
            f0=float(f0),
            slide=float(slide),
        )

        if row is None:
            continue

        rows.append(row)

        if best is None or row["coherent"] > best["coherent"]:
            best = row

    if keep_all:
        return best, rows

    return best, []


def ridge_width(freq_rows, frac=0.90):
    if not freq_rows:
        return "", "", 0

    peak = max(float(r["coherent"]) for r in freq_rows)
    keep = [float(r["f0"]) for r in freq_rows if float(r["coherent"]) >= frac * peak]

    if not keep:
        return "", "", 0

    return min(keep), max(keep), len(keep)


def verdict_from_summary(on_peak, bg_p95, bg_p99, bg_max, exceed, fmin, fmax, fstep):
    f0 = float(on_peak["f0"])
    score = float(on_peak["coherent"])

    edge = (f0 <= fmin + fstep) or (f0 >= fmax - fstep)

    if edge:
        return "RIDGE_EDGE_WARNING"

    if exceed == 0 and score > bg_p99:
        return "FREQUENCY_RIDGE_SUPPORT_STRONG"

    if score > bg_p95:
        return "FREQUENCY_RIDGE_SUPPORT_MODERATE"

    return "FREQUENCY_RIDGE_NOT_SUPPORTED"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--event", default="GW190521_074359")
    ap.add_argument("--fmin", type=float, default=20.0)
    ap.add_argument("--fmax", type=float, default=500.0)
    ap.add_argument("--fstep", type=float, default=2.0)
    ap.add_argument("--band-low", type=float, default=20.0)
    ap.add_argument("--band-high", type=float, default=500.0)
    ap.add_argument("--n-slides", type=int, default=0, help="0 means all default slides")
    args = ap.parse_args()

    print("=== PRISM 2.2-alpha FREQUENCY RIDGE LOCKED VALIDATION ===", flush=True)
    print("Unofficial exploratory diagnostic.", flush=True)
    print("Scans f0 over a fixed time anchor and compares on-source global frequency peak to time-slide global peaks.", flush=True)
    print("", flush=True)

    freqs = np.arange(args.fmin, args.fmax + 0.5 * args.fstep, args.fstep)
    slides = SLIDES
    if args.n_slides and args.n_slides > 0:
        slides = SLIDES[: args.n_slides]

    print(f"freq grid: {args.fmin} to {args.fmax} Hz step={args.fstep} n={len(freqs)}", flush=True)
    print(f"residual band: [{args.band_low}, {args.band_high}] Hz", flush=True)
    print(f"slides: n={len(slides)}", flush=True)
    print("", flush=True)

    t, xH, xL, meta = load_residual_series(args.event, args.band_low, args.band_high)

    all_rows = []
    summary_rows = []

    for anchor in ANCHORS:
        name = anchor["anchor"]
        center = float(anchor["center"])
        scale = float(anchor["scale"])

        print("------------------------------------------------------------", flush=True)
        print(f"ANCHOR={name} center={center:+.4f} scale={scale:.4f}", flush=True)

        on_peak, on_rows = scan_frequency_grid(
            t=t,
            xH=xH,
            xL=xL,
            center=center,
            scale=scale,
            freqs=freqs,
            slide=0.0,
            keep_all=True,
        )

        if on_peak is None:
            print(f"{name}: no valid on-source peak", flush=True)
            continue

        # Save on-source frequency curve.
        for r in on_rows:
            out = {}
            out.update(meta)
            out.update({
                "row_type": "on_source_frequency_curve",
                "anchor": name,
                "center": center,
                "scale": scale,
            })
            out.update(r)
            all_rows.append(out)

        bg_peaks = []
        bg_peak_rows = []

        for slide in slides:
            b, _ = scan_frequency_grid(
                t=t,
                xH=xH,
                xL=xL,
                center=center,
                scale=scale,
                freqs=freqs,
                slide=float(slide),
                keep_all=False,
            )

            if b is None:
                continue

            bg_peaks.append(float(b["coherent"]))

            row = {}
            row.update(meta)
            row.update({
                "row_type": "timeslide_global_peak",
                "anchor": name,
                "center": center,
                "scale": scale,
            })
            row.update(b)
            all_rows.append(row)
            bg_peak_rows.append(row)

        bg = np.asarray(bg_peaks, dtype=float)
        bg = bg[np.isfinite(bg)]

        if len(bg) > 0:
            bg_med = float(np.median(bg))
            bg_p95 = float(np.percentile(bg, 95))
            bg_p99 = float(np.percentile(bg, 99))
            bg_max = float(np.max(bg))
            bg_std = float(np.std(bg) + 1e-12)
            global_z = float((float(on_peak["coherent"]) - bg_med) / bg_std)
            exceed = int(np.sum(bg >= float(on_peak["coherent"])))
            emp_p = float((exceed + 1) / (len(bg) + 1))
        else:
            bg_med = bg_p95 = bg_p99 = bg_max = global_z = emp_p = float("nan")
            exceed = -1

        w90_min, w90_max, w90_count = ridge_width(on_rows, frac=0.90)
        w80_min, w80_max, w80_count = ridge_width(on_rows, frac=0.80)

        v = verdict_from_summary(
            on_peak=on_peak,
            bg_p95=bg_p95,
            bg_p99=bg_p99,
            bg_max=bg_max,
            exceed=exceed,
            fmin=args.fmin,
            fmax=args.fmax,
            fstep=args.fstep,
        )

        summary = {}
        summary.update(meta)
        summary.update({
            "anchor": name,
            "center": center,
            "scale": scale,
            "fmin": args.fmin,
            "fmax": args.fmax,
            "fstep": args.fstep,
            "n_freq": len(freqs),
            "n_bg": len(bg),
            "on_peak_coherent": float(on_peak["coherent"]),
            "on_peak_f0": float(on_peak["f0"]),
            "on_peak_lag": float(on_peak["lag"]),
            "on_peak_mode": on_peak["mode"],
            "on_peak_zH1": float(on_peak["zH1"]),
            "on_peak_zL1": float(on_peak["zL1"]),
            "on_same_score": float(on_peak["same_score"]),
            "on_opposite_score": float(on_peak["opposite_score"]),
            "ridge90_fmin": w90_min,
            "ridge90_fmax": w90_max,
            "ridge90_count": w90_count,
            "ridge80_fmin": w80_min,
            "ridge80_fmax": w80_max,
            "ridge80_count": w80_count,
            "bg_median": bg_med,
            "bg_p95": bg_p95,
            "bg_p99": bg_p99,
            "bg_max": bg_max,
            "global_z": global_z,
            "exceed": exceed,
            "empirical_p": emp_p,
            "verdict": v,
        })

        summary_rows.append(summary)

        print(
            f"{name:32s} "
            f"peak={float(on_peak['coherent']):+8.3f} "
            f"f0={float(on_peak['f0']):7.2f}Hz "
            f"lag={float(on_peak['lag']):+.4f}s "
            f"mode={on_peak['mode']:8s} "
            f"zH={float(on_peak['zH1']):+8.3f} "
            f"zL={float(on_peak['zL1']):+8.3f} "
            f"ridge90=[{w90_min},{w90_max}] n={w90_count} "
            f"bg_p99={bg_p99:+8.3f} "
            f"bg_max={bg_max:+8.3f} "
            f"globalZ={global_z:+8.3f} "
            f"emp_p={emp_p:.4f} "
            f"exceed={exceed}/{len(bg)} "
            f"verdict={v}",
            flush=True,
        )

    if all_rows:
        fieldnames = sorted(set().union(*(r.keys() for r in all_rows)))
        with open(OUTCSV, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_rows)

    lines = []
    lines.append("PRISM 2.2-alpha FREQUENCY RIDGE LOCKED VALIDATION SUMMARY - 2026-07-02")
    lines.append("")
    lines.append("Status:")
    lines.append("- Unofficial exploratory diagnostic.")
    lines.append("- Scans ring-template frequency f0 while keeping time anchor and scale fixed.")
    lines.append("- On-source global frequency peak is compared against time-slide global frequency peaks.")
    lines.append("- This controls the look-elsewhere effect across the scanned frequency grid at scout level.")
    lines.append("")
    lines.append(f"Event: {args.event}")
    lines.append(f"GR source: {meta['gr_source']}")
    lines.append(f"PSD: {meta['psd_window_name']} [{meta['psd_start']}, {meta['psd_end']})")
    lines.append(f"Residual band: [{args.band_low}, {args.band_high}] Hz")
    lines.append(f"Frequency grid: {args.fmin} to {args.fmax} Hz, step={args.fstep}, n={len(freqs)}")
    lines.append("")
    lines.append("Results:")
    lines.append("")

    for s in summary_rows:
        lines.append(f"{s['anchor']}:")
        lines.append(f"- center = {s['center']:+.6f} s")
        lines.append(f"- scale = {s['scale']:.6f} s")
        lines.append(f"- on_peak_coherent = {s['on_peak_coherent']:+.6f}")
        lines.append(f"- on_peak_f0 = {s['on_peak_f0']:.6f} Hz")
        lines.append(f"- on_peak_lag = {s['on_peak_lag']:+.6f} s")
        lines.append(f"- on_peak_mode = {s['on_peak_mode']}")
        lines.append(f"- on_peak_zH1 = {s['on_peak_zH1']:+.6f}")
        lines.append(f"- on_peak_zL1 = {s['on_peak_zL1']:+.6f}")
        lines.append(f"- ridge90 = [{s['ridge90_fmin']}, {s['ridge90_fmax']}], n={s['ridge90_count']}")
        lines.append(f"- ridge80 = [{s['ridge80_fmin']}, {s['ridge80_fmax']}], n={s['ridge80_count']}")
        lines.append(f"- bg_n = {s['n_bg']}")
        lines.append(f"- bg_median = {s['bg_median']:+.6f}")
        lines.append(f"- bg_p95 = {s['bg_p95']:+.6f}")
        lines.append(f"- bg_p99 = {s['bg_p99']:+.6f}")
        lines.append(f"- bg_max = {s['bg_max']:+.6f}")
        lines.append(f"- globalZ = {s['global_z']:+.6f}")
        lines.append(f"- exceed = {s['exceed']}/{s['n_bg']}")
        lines.append(f"- empirical_p = {s['empirical_p']:.6f}")
        lines.append(f"- verdict = {s['verdict']}")
        lines.append("")

    strong = [s for s in summary_rows if s["verdict"] == "FREQUENCY_RIDGE_SUPPORT_STRONG"]
    moderate = [s for s in summary_rows if s["verdict"] == "FREQUENCY_RIDGE_SUPPORT_MODERATE"]

    lines.append("Conservative read:")
    if len(strong) >= 2:
        lines.append("- Frequency-ridge support is strong in both anchors.")
    elif len(strong) == 1:
        lines.append("- Frequency-ridge support is strong in one anchor.")
    elif len(moderate) >= 1:
        lines.append("- Frequency-ridge support is moderate only.")
    else:
        lines.append("- Frequency-ridge support is not established under this alpha scan.")
    lines.append("")
    lines.append("Caution:")
    lines.append("- This is PRISM 2.2-alpha only.")
    lines.append("- It should not replace the PRISM 2.1 evidence stack.")
    lines.append("- Positive results require a locked rerun with more slides and a fixed GR source.")

    OUTSUMMARY.write_text("\n".join(lines) + "\n")

    print("")
    print("=== SAVED ===", flush=True)
    print("csv:", OUTCSV, flush=True)
    print("summary:", OUTSUMMARY, flush=True)
    print("", flush=True)
    print(OUTSUMMARY.read_text(), flush=True)


if __name__ == "__main__":
    main()
