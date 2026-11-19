from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import sxs


ROOT = Path(r"E:\RIUD_ACTIVE_20260808")
PANEL_ROOT = ROOT / "SXS_RED_DOT_COMMON_HORIZON_BLIND_SMOKE10_R0_20260815"
PANEL = PANEL_ROOT / "selection" / "SXS_PHYSICAL_PANEL10_SELECTED.csv"
HORIZON_SUMMARY = ROOT / "RIUD_SXS_NATIVE_STRUCTURE_HORIZON_SYNC_R0_20260821" / "SXS_STRUCTURE_HORIZON_SYNC.csv"
FROZEN_RULE = ROOT / "RIUD_DEV99_PATH_ONLY_CPU_ADAPTIVE_R10G_20260811_WORK" / "runtime" / "GW150914_095045" / "engine" / "frozen" / "candidate_first_rule_frozen.py"
R40_COORD = ROOT / "RIUD_DEV99_PHYSICAL_DYNAMICAL_LAW_FREEZE_R40_20260815" / "R40_PHYSICAL_COORDINATE.json"
OUT = ROOT / "RIUD_SXS_NATIVE_RIUD_REPLAY_SYM_0P3S_R0_20260823"

M_REF_MS = 60.0
# Geometric time for the frozen 60 Msun reference: G M / c^3.
M_SEC = M_REF_MS * 4.92549095e-6
# Extension-only branch: all source-native rules are unchanged; only the
# Symmetric extension-only support: -0.30..+0.30 s.
CENTER_S = np.round(np.arange(-0.30, 0.3000001, 0.01), 6)
WIDTH_S = np.asarray([0.010, 0.020, 0.030, 0.040, 0.050, 0.060], float)
FREQ_HZ = np.arange(60.0, 330.0001, 10.0)
LAG_S = np.round(np.arange(-0.012, 0.0120001, 0.001), 6)
MODES = ("same", "opposite")
NULL_N = 200
EPS = 1e-12
GAMMA = 0.3162354634393393


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def import_rule():
    spec = importlib.util.spec_from_file_location("frozen_candidate_rule", FROZEN_RULE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"RULE_IMPORT_FAILED:{FROZEN_RULE}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def robust_z(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, float)
    med = float(np.median(x))
    mad = float(np.median(np.abs(x - med)))
    scale = max(1.4826 * mad, np.finfo(float).eps)
    return (x - med) / scale


def load_mode(path: Path):
    w = sxs.load(str(path), transform_to_inertial=False, ignore_validation=True)
    lm = np.asarray(w.LM)
    hits = np.flatnonzero((lm[:, 0] == 2) & (lm[:, 1] == 2))
    if len(hits) != 1:
        raise RuntimeError(f"MODE_22_NOT_UNIQUE:{path}:{len(hits)}")
    h22 = np.asarray(w[:, int(hits[0])], dtype=complex)
    t = np.asarray(w.t, dtype=float)
    order = np.argsort(t)
    t = t[order]
    h22 = h22[order]
    tu = np.linspace(float(t[0]), float(t[-1]), len(t))
    re = np.interp(tu, t, h22.real)
    im = np.interp(tu, t, h22.imag)
    amp = np.hypot(re, im)
    peak_i = int(np.nanargmax(amp))
    t_rel = tu - float(tu[peak_i])
    return t_rel, robust_z(re), robust_z(im), {
        "N_TIME": int(len(tu)),
        "N_MODES": int(w.shape[1]),
        "ELL_MIN": int(w.ell_min),
        "ELL_MAX": int(w.ell_max),
        "T_START_NATIVE": float(t_rel[0]),
        "T_END_NATIVE": float(t_rel[-1]),
        "T_PEAK_NATIVE": float(tu[peak_i]),
    }


def channel_map(t: np.ndarray, x: np.ndarray, centers_s: np.ndarray) -> np.ndarray:
    centers_native = centers_s / M_SEC
    widths_native = WIDTH_S / M_SEC
    freqs_native = FREQ_HZ * M_SEC
    all_centers = np.unique(np.round(np.concatenate([centers_s, (centers_s[:, None] + LAG_S[None, :]).ravel()]), 9))
    out = np.zeros((len(all_centers), len(FREQ_HZ), len(WIDTH_S)), dtype=complex)
    for ci, center_s in enumerate(all_centers):
        center = float(center_s / M_SEC)
        for wi, width in enumerate(widths_native):
            sigma = max(float(width) / 2.355, float(np.median(np.diff(t))))
            g = np.exp(-0.5 * ((t - center) / sigma) ** 2)
            denom = math.sqrt(float(np.sum(g * g))) + EPS
            for fi, freq in enumerate(freqs_native):
                out[ci, fi, wi] = np.sum(x * g * np.exp(-2j * np.pi * freq * (t - center))) / denom
    return all_centers, out


def source_state(t: np.ndarray, q0: np.ndarray, q1: np.ndarray):
    base_centers, m0 = channel_map(t, q0, CENTER_S)
    _, m1 = channel_map(t, q1, CENTER_S)
    center_i = {round(float(x), 9): i for i, x in enumerate(base_centers)}
    score = np.full((len(CENTER_S), len(FREQ_HZ), len(WIDTH_S)), -np.inf, float)
    chosen_lag = np.zeros_like(score)
    chosen_mode = np.empty(score.shape, dtype=object)
    for ci, c in enumerate(CENTER_S):
        for fi in range(len(FREQ_HZ)):
            for wi in range(len(WIDTH_S)):
                best = (-np.inf, 0.0, "")
                for lag in LAG_S:
                    j = center_i.get(round(float(c + lag), 9))
                    if j is None:
                        continue
                    a = m0[center_i[round(float(c), 9)], fi, wi]
                    b = m1[j, fi, wi]
                    bal = min(abs(a), abs(b)) / (max(abs(a), abs(b)) + EPS)
                    for mode in MODES:
                        sign = 1.0 if mode == "same" else -1.0
                        val = abs(a + sign * b) / math.sqrt(2.0) * bal
                        if val > best[0]:
                            best = (float(val), float(lag), mode)
                score[ci, fi, wi] = best[0]
                chosen_lag[ci, fi, wi] = best[1]
                chosen_mode[ci, fi, wi] = best[2]
    null = np.stack([np.roll(score, int((b * 7) % len(CENTER_S)), axis=0) for b in range(NULL_N)], axis=0)
    mean = np.mean(null, axis=0)
    std = np.std(null, axis=0, ddof=0)
    positive = std[np.isfinite(std) & (std > 0)]
    floor = max(float(np.quantile(positive, 0.05)) if len(positive) else 1e-6, 1e-6)
    state = ((score - mean) / np.maximum(std, floor)).astype(np.float32)
    return state, score, chosen_lag, chosen_mode, floor


def physical_s(row, horizon, coord):
    m1 = float(row["M_HEAVY"])
    m2 = float(row["M_LIGHT"])
    s1 = math.sqrt(sum(float(row[k]) ** 2 for k in ("CHI_H_X", "CHI_H_Y", "CHI_H_Z")))
    s2 = math.sqrt(sum(float(row[k]) ** 2 for k in ("CHI_L_X", "CHI_L_Y", "CHI_L_Z")))
    mf = float(horizon["AHC_FINAL_CHRISTODOULOUS_MASS"])
    sf = float(horizon["AHC_FINAL_SPIN_MAG"])
    irr = lambda m, s: m * math.sqrt((1.0 + math.sqrt(max(0.0, 1.0 - min(0.999999, s * s)))) / 2.0)
    R = irr(mf, sf) / (irr(m1, s1) + irr(m2, s2))
    den = abs(float(row["CHI_H_Z"])) + abs(float(row["CHI_L_Z"]))
    chi_a = (float(row["CHI_H_Z"]) - float(row["CHI_L_Z"])) / den if den > 0 else 0.0
    S = float(coord["COEFFICIENT_R"]) * ((R - float(coord["R_MEAN"])) / float(coord["R_STD"])) + float(coord["COEFFICIENT_CHI_A"]) * ((chi_a - float(coord["CHI_A_MEAN"])) / float(coord["CHI_A_STD"]))
    return R, chi_a, S


def run_event(row, horizons, coord, rule):
    sid = row["SXS_ID"]
    short = sid.split(":")[-1]
    source = PANEL_ROOT / "waveforms" / f"SXS_BBH_{short}" / f"Lev{row['LEV']}" / "Strain_N2.h5"
    t, q0, q1, meta = load_mode(source)
    state, score, lag, mode, floor = source_state(t, q0, q1)
    res = rule.search_hypergrid(state, CENTER_S, FREQ_HZ, WIDTH_S, rule.SCENARIOS[0], return_path=True)
    t_i = np.asarray(res.get("candidate_t_i", []), int)
    f_i = np.asarray(res.get("candidate_f_i", []), int)
    w_i = np.asarray(res.get("candidate_w_i", []), int)
    pidx = [int(x) for x in res.get("path_node_indices", [])]
    path_freq = [float(FREQ_HZ[f_i[j]]) for j in pidx] if len(f_i) else []
    path_tau = [float(CENTER_S[t_i[j]]) for j in pidx] if len(t_i) else []
    freq_increase = int(sum(b > a for a, b in zip(path_freq, path_freq[1:])))
    freq_decrease = int(sum(b < a for a, b in zip(path_freq, path_freq[1:])))
    R, chi_a, S = physical_s(row, horizons[sid], coord)
    event_dir = "UP" if GAMMA * S > 0 else ("DOWN" if GAMMA * S < 0 else "NEUTRAL")
    result = {
        "SXS_ID": sid,
        "CATEGORY": row["CATEGORY_NAME"],
        "SOURCE_SHA256": sha256(source),
        "N_TIME": meta["N_TIME"],
        "N_MODES": meta["N_MODES"],
        "SOURCE_TIME_UNIT": "M",
        "SOURCE_CHANNELS": "Re(h22),Im(h22)",
        "SOURCE_PEAK_ORIGIN": "argmax(abs(h22))",
        "NODE_STATUS": "PATH_FOUND" if res.get("status") == "PATH_FOUND" else "NO_PATH",
        "CANDIDATE_COUNT": int(res.get("candidate_count", 0)),
        "PATH_NODE_COUNT": int(res.get("path_nodes", 0)),
        "PATH_SCORE": float(res.get("score", 0.0)),
        "PATH_TAU_START_S": path_tau[0] if path_tau else "",
        "PATH_TAU_END_S": path_tau[-1] if path_tau else "",
        "PATH_FREQUENCY_INCREASES": freq_increase,
        "PATH_FREQUENCY_DECREASES": freq_decrease,
        "INTRINSIC_ORDERING": "INCREASING" if freq_increase > freq_decrease else ("DECREASING" if freq_decrease > freq_increase else "MIXED_OR_EMPTY"),
        "R_MIRR_RATIO": R,
        "CHI_A_NORMALIZED": chi_a,
        "S_FROZEN": S,
        "GAMMA_S": GAMMA * S,
        "S_RATE_DIRECTION": event_dir,
        "SOURCE_NULL200": "CIRCULAR_CENTER_SHIFT_200",
        "ROBUST_SCALE_FLOOR": floor,
        "OBSERVED_TOPOLOGY": "NOT_ESTABLISHED_FROM_SINGLE_SOURCE_PATH",
    }
    node_rows = []
    if len(t_i):
        cand_z = np.asarray(res.get("candidate_z", []), float)
        cand_p = np.asarray(res.get("candidate_persistence", []), int)
        path_set = set(pidx)
        for j in range(len(t_i)):
            node_rows.append({"SXS_ID": sid, "CENTER_S": CENTER_S[t_i[j]], "FREQUENCY_AXIS": FREQ_HZ[f_i[j]], "WIDTH_S": WIDTH_S[w_i[j]], "STATE_Z": cand_z[j], "WIDTH_PERSISTENCE": cand_p[j], "IS_PATH_NODE": int(j in path_set)})
    with (OUT / f"{short}_NODES.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["SXS_ID", "CENTER_S", "FREQUENCY_AXIS", "WIDTH_S", "STATE_Z", "WIDTH_PERSISTENCE", "IS_PATH_NODE"])
        writer.writeheader(); writer.writerows(node_rows)
    with (OUT / f"{short}_PATH.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["SXS_ID", "PATH_INDEX", "CENTER_S", "FREQUENCY_AXIS", "WIDTH_S"])
        writer.writeheader()
        for k, j in enumerate(pidx):
            writer.writerow({"SXS_ID": sid, "PATH_INDEX": k, "CENTER_S": CENTER_S[t_i[j]], "FREQUENCY_AXIS": FREQ_HZ[f_i[j]], "WIDTH_S": WIDTH_S[w_i[j]]})
    return result


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    panel = read_csv(PANEL)
    horizons = {r["SXS_ID"]: r for r in read_csv(HORIZON_SUMMARY)}
    coord = json.loads(R40_COORD.read_text(encoding="utf-8"))
    rule = import_rule()
    workers = min(16, len(panel))
    results = []
    print(f"GLOBAL_WORKERS={workers} EVENTS={len(panel)} MODE=EVENT_PARALLEL_SINGLE_POOL", flush=True)
    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="sxs-event") as pool:
        futures = {pool.submit(run_event, row, horizons, coord, rule): row["SXS_ID"] for row in panel}
        for n, future in enumerate(as_completed(futures), 1):
            sid = futures[future]
            result = future.result()
            results.append(result)
            print(f"PROGRESS={n}/{len(panel)} EVENT={sid} STATUS={result['NODE_STATUS']} NODES={result['CANDIDATE_COUNT']} PATH={result['PATH_NODE_COUNT']}", flush=True)
    order = {row["SXS_ID"]: i for i, row in enumerate(panel)}
    results.sort(key=lambda r: order[r["SXS_ID"]])
    total_nodes = sum(int(r["CANDIDATE_COUNT"]) for r in results)
    total_path = sum(int(r["PATH_NODE_COUNT"]) for r in results)

    fields = list(results[0])
    with (OUT / "SXS_NATIVE_EVENT_RESULTS.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader(); writer.writerows(results)
    summary = {
        "R_STATUS": "PARTIAL_NODE_PATH_REPLAY",
        "BRANCH": "SXS_NATIVE_RIUD_REPLAY_SYM_0P3S_R0_20260823",
        "EVENTS": len(results),
        "NODE_PATH_POSITIVE_N": sum(r["NODE_STATUS"] == "PATH_FOUND" for r in results),
        "TOTAL_CANDIDATE_NODES": total_nodes,
        "TOTAL_PATH_NODES": total_path,
        "SXS_NATIVE_ADAPTER": "Re(h22), Im(h22), source t/M, fixed global 60 Msun conversion of frozen detector map grid, circular center-shift source NULL200",
        "SEARCH_SUPPORT_S": "-0.30..+0.30",
        "FROZEN_RULE_SHA256": sha256(FROZEN_RULE),
        "R40_COORD_SHA256": sha256(R40_COORD),
        "HORIZON_H5_READ": False,
        "HORIZON_SUMMARY_REUSED": True,
        "TOPOLOGY_REPRODUCTION": "NOT_ESTABLISHED_FROM_SINGLE_EVENT_PATH",
        "INTRINSIC_ORDERING": "COMPUTED_FROM_PATH_FREQUENCY_ORDER",
        "S_DEPENDENT_DIRECTION": "COMPUTED_AS_EXP(GAMMA*S) DIRECTION ONLY",
        "EXACT_FROZEN_REPLAY": False,
        "NEW_NODE_PATH_RULE": False,
        "R40_REFIT": False,
        "HOLDOUT30_ACCESSED": False,
        "VERDICT": "SXS_NATIVE_NODE_PATH_OBSERVATION_COMPLETE_STATE_TOPOLOGY_REQUIRES_EXPLICIT_SOURCE_HISTORY_BINDING",
    }
    (OUT / "SXS_NATIVE_REPLAY_SUMMARY.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    contract = f"""SXS_NATIVE_RIUD_REPLAY_R0 CONTRACT

ADAPTER_NAME=SOURCE_QUADRATURE_H22_NATIVE_M
CHANNEL_0=Re(h_22); CHANNEL_1=Im(h_22)
TIME_COORDINATE=SXS_NATIVE_SIMULATION_TIME/M
PEAK_ORIGIN=argmax(abs(h_22)), same rule for all 10
GLOBAL_MASS_REFERENCE_MS={M_REF_MS}
FROZEN_CENTER_GRID_S=-0.30..+0.30 step 0.01, represented in native M using this single global reference
FROZEN_WIDTHS_S=0.01|0.02|0.03|0.04|0.05|0.06, represented in native M
FROZEN_FREQUENCY_AXIS=60..330 Hz labels, Fourier evaluation uses f*M_REF
SOURCE_NULL200=CIRCULAR_CENTER_SHIFT_200, shifts=(b*7) mod center_count, b=0..199
NODE_RULE=FROZEN_CANDIDATE_RULE, SHA256={sha256(FROZEN_RULE)}
PATH_RULE=FROZEN_CANDIDATE_RULE_SEARCH_HYPERGRID
S_RULE=FROZEN_R40_COORDINATE, gamma={GAMMA}
HORIZON_H5_READ=FALSE
HORIZON_SUMMARY_REUSED=TRUE
NEW_SURROGATE=FALSE
EXACT_FROZEN_REPLAY=FALSE
STATE_TOPOLOGY=NOT_CLAIMED; a single source event path does not carry the frozen population state labels N0/A1/G/AR without a new history-binding rule.
"""
    (OUT / "SXS_NATIVE_REPLAY_CONTRACT.txt").write_text(contract, encoding="utf-8")
    send = [
        "R_STATUS=EXTENDED_SEARCH_SUPPORT_REPLAY",
        f"EVENTS={len(results)}",
        f"NODE_PATH_POSITIVE_N={sum(r['NODE_STATUS']=='PATH_FOUND' for r in results)}",
        f"TOTAL_CANDIDATE_NODES={total_nodes}",
        f"TOTAL_PATH_NODES={total_path}",
        "NODE_RULE=FROZEN_CANDIDATE_RULE",
        "PATH_RULE=FROZEN_CANDIDATE_RULE_SEARCH_HYPERGRID",
        "SXS_ADAPTER=Re(h22)|Im(h22)|NATIVE_t_over_M",
        "SOURCE_NULL200=CIRCULAR_CENTER_SHIFT_200",
        "S_FROZEN=TRUE",
        "GAMMA_FROZEN=0.3162354634393393",
        "SEARCH_SUPPORT_S=-0.30..+0.30",
        "TOPOLOGY_REPRODUCTION=NOT_ESTABLISHED_FROM_SINGLE_EVENT_PATH",
        "INTRINSIC_ORDERING=COMPUTED",
        "S_DEPENDENT_DIRECTION=COMPUTED",
        "EXACT_FROZEN_REPLAY=FALSE",
        "HORIZON_H5_READ=FALSE",
        "HORIZON_SUMMARY_REUSED=TRUE",
        "NEW_NODE_PATH_RULE=FALSE",
        "R40_REFIT=FALSE",
        "HOLDOUT30_ACCESSED=FALSE",
        "SCIENTIFIC_VERDICT=SXS_NATIVE_NODE_PATH_OBSERVATION_COMPLETE_STATE_TOPOLOGY_NOT_ESTABLISHED",
        "NEXT=REQUIRE_PRELOCKED_SOURCE_STATE_HISTORY_BINDING_FOR_N0_A1_G_AR_TEST",
    ]
    (OUT / "SEND_TO_CHAT.txt").write_text("\n".join(send) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
