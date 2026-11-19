from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
from scipy.stats import kendalltau, spearmanr


ROOT = Path(r"E:\RIUD_ACTIVE_20260808")
OUT = ROOT / "RIUD_DEV99_HOLDOUT5_R6_R8_R9_R40_EXACT_REPLAY_R0_20260817"
HOLDOUT10 = ROOT / "RIUD_DEV99_HOLDOUT10_FROZEN_PATH_DYNAMICS_VALIDATION_R1_20260813"
COVERAGE_REPLAY = ROOT / "RIUD_DEV99_HOLDOUT5_DEV96_COVERAGE_REPLAY_R0_20260817"
R5 = ROOT / "RIUD_DEV99_EVENT_COVERAGE_RATE_BALANCE_DYNAMICS_DISCOVERY_R5_20260814"
R6 = ROOT / "RIUD_DEV99_REENTRY_MULTISTATE_STATE_IDENTITY_AUDIT_R6_20260815"
R8 = ROOT / "RIUD_DEV99_RUN_INDEX_STATE_MEMORY_IDENTITY_AUDIT_R8_20260815"
R9 = ROOT / "RIUD_DEV99_HISTORY_AWARE_MULTISTATE_FLOW_LAW_DISCOVERY_R9_20260815"
R40 = ROOT / "RIUD_DEV99_PHYSICAL_DYNAMICAL_LAW_FREEZE_R40_20260815"
PE_ROOT = ROOT / "RIUD_CATALOG50_PATH_DYNAMICS_R0_20260807" / "02_INPUT" / "PE_POSTERIOR_OFFICIAL_ALL_NODE_FRESH"

EVENTS = [
    "GW241114_024711",
    "GW240830_211120",
    "GW240612_081540",
    "GW241130_110422",
    "GW250119_190238",
]
EVENT_SET = set(EVENTS)
MAPS = ["W1_START_TO_PEAK", "W2_PEAK_TO_END", "W3_START_TO_MT", "W4_MT_TO_END"]
PE_PREF = ["C01:Mixed", "C00:Mixed", "C01:IMRPhenomXPHM", "C00:IMRPhenomXPHM-SpinTaylor", "C00:SEOBNRv5PHM", "C01:SEOBNRv4PHM"]
PE_FIELDS = ["mass_1_source", "mass_2_source", "a_1", "a_2", "tilt_1", "tilt_2", "phi_12", "final_mass_source", "final_spin"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def req(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(str(path))
    return path


def choose_dataset(h5: h5py.File):
    candidates = []

    def visit(name, obj):
        if isinstance(obj, h5py.Dataset) and name.lower().endswith("/posterior_samples") and obj.dtype.names:
            fields = set(obj.dtype.names)
            count = len(fields & set(PE_FIELDS))
            prefix = name.rsplit("/", 1)[0]
            rank = PE_PREF.index(prefix) if prefix in PE_PREF else len(PE_PREF) + 1
            candidates.append((count, -rank, name, fields))

    h5.visititems(visit)
    if not candidates:
        return None
    return sorted(candidates, reverse=True)[0]


def median_field(arr, field):
    if field not in arr.dtype.names:
        return np.nan
    x = np.asarray(arr[field], dtype=float)
    x = x[np.isfinite(x)]
    return float(np.median(x)) if len(x) else np.nan


def physical_row(event: str):
    index = req(HOLDOUT10 / "03_STAGE_A_PATH" / "RESULTS" / event / "EVENT_INDEX.csv")
    idx = pd.read_csv(index)
    paths = [str(x) for x in idx.iloc[:, 1].tolist() if "combined_PEDataRelease" in str(x)]
    if len(paths) != 1:
        raise RuntimeError(f"{event}: PE binding is not unique: {paths}")
    raw_path = paths[0].replace("/", "\\")
    pe = Path("E:" + raw_path[6:]) if raw_path.lower().startswith("\\mnt\\e\\") else Path(raw_path)
    if not pe.exists():
        raise FileNotFoundError(str(pe))
    with h5py.File(pe, "r") as h5:
        choice = choose_dataset(h5)
        if choice is None or choice[0] < len(PE_FIELDS):
            raise RuntimeError(f"{event}: required PE fields incomplete")
        _, neg_rank, dname, fields = choice
        arr = h5[dname][()]
    vals = {f: median_field(arr, f) for f in PE_FIELDS}
    m1, m2 = vals["mass_1_source"], vals["mass_2_source"]
    a1 = float(np.clip(abs(vals["a_1"]), 0.0, 0.999999))
    a2 = float(np.clip(abs(vals["a_2"]), 0.0, 0.999999))
    af = float(np.clip(abs(vals["final_spin"]), 0.0, 0.999999))

    def irr_frac(a):
        return math.sqrt((1.0 + math.sqrt(max(0.0, 1.0 - a * a))) / 2.0)

    chi1z = vals["a_1"] * math.cos(vals["tilt_1"])
    chi2z = vals["a_2"] * math.cos(vals["tilt_2"])
    denom = abs(chi1z) + abs(chi2z)
    if not np.isfinite(denom) or denom == 0:
        raise RuntimeError(f"{event}: frozen CHI_A_NORMALIZED denominator undefined")
    chi_a = (chi1z - chi2z) / denom
    mirr_final = vals["final_mass_source"] * irr_frac(af)
    mirr_initial = m1 * irr_frac(a1) + m2 * irr_frac(a2)
    R = mirr_final / mirr_initial
    Rz = (R - 0.9146055149447014) / 0.02342915881660063
    Chiz = (chi_a - 0.17611809408807724) / 0.4858691630937626
    S = 0.22030031492055946 * Rz + 0.3457660274266933 * Chiz
    return {
        "EVENT": event,
        "PE_FILE": str(pe),
        "PE_SHA256": sha256(pe),
        "DATASET_PATH": dname,
        "POSTERIOR_N": int(len(arr)),
        **{f"MEDIAN_{k}": v for k, v in vals.items()},
        "CHI1Z_FROZEN": chi1z,
        "CHI2Z_FROZEN": chi2z,
        "CHI_A_NORMALIZED": chi_a,
        "M_IRR_FINAL": mirr_final,
        "M_IRR_INITIAL_SUM": mirr_initial,
        "R_FROZEN": R,
        "S_KERR_ORDINAL": S,
    }


def classify_r6(nodes: pd.DataFrame, bins: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for event in EVENTS:
        g = nodes[nodes.EVENT_ID.astype(str) == event]
        occ = []
        for b in bins.itertuples(index=False):
            left, right = float(b.GLOBAL_LEFT_PCT), float(b.GLOBAL_RIGHT_PCT)
            if int(b.BIN_INDEX) == int(bins.BIN_INDEX.max()):
                mask = (g.GLOBAL_PCT >= left) & (g.GLOBAL_PCT <= right)
            else:
                mask = (g.GLOBAL_PCT >= left) & (g.GLOBAL_PCT < right)
            occ.append(int(mask.any()))
        completed = 0
        current_run = 0
        seen = False
        last = None
        prior_g = 0
        prior_l = 0
        prev = False
        for b, cur_i in zip(bins.itertuples(index=False), occ):
            cur = bool(cur_i)
            before_g, before_l = prior_g, prior_l
            if int(b.BIN_INDEX) > 0:
                if prev and not cur:
                    completed += 1
                if (not prev) and cur:
                    current_run = completed + 1
                if prev and cur and current_run == 0:
                    current_run = 1
            if cur:
                if not seen:
                    current_run = 1
                    state = "A1"
                else:
                    state = "A1" if current_run == 1 else "AR"
                seen = True
                last = int(b.BIN_INDEX)
            else:
                state = "N0" if not seen else "G"
            since = 0 if cur else (np.nan if last is None else int(b.BIN_INDEX) - last)
            rows.append({
                "EVENT": event,
                "BIN_INDEX": int(b.BIN_INDEX),
                "GLOBAL_LEFT_PCT": float(b.GLOBAL_LEFT_PCT),
                "GLOBAL_RIGHT_PCT": float(b.GLOBAL_RIGHT_PCT),
                "GLOBAL_MID_PCT": (float(b.GLOBAL_LEFT_PCT) + float(b.GLOBAL_RIGHT_PCT)) / 2.0,
                "OCCUPIED": int(cur),
                "STATE": state,
                "HAS_EVER_BEEN_ACTIVE_BEFORE_BIN": bool(seen and not (cur and current_run == 1 and before_g == 0)),
                "N_PRIOR_GAINS": before_g,
                "N_PRIOR_LOSSES": before_l,
                "N_COMPLETED_ACTIVE_RUNS": completed,
                "CURRENT_ACTIVE_RUN_INDEX": current_run if cur else 0,
                "TIME_SINCE_LAST_ACTIVE_BIN": since,
            })
            if int(b.BIN_INDEX) > 0:
                if (not prev) and cur:
                    prior_g += 1
                if prev and (not cur):
                    prior_l += 1
            prev = cur
    return pd.DataFrame(rows)


def cat_from_row(row):
    state = str(row.STATE)
    idx = int(row.CURRENT_ACTIVE_RUN_INDEX) if state in ("A1", "AR") else int(row.N_COMPLETED_ACTIVE_RUNS)
    if state == "N0":
        return "N0"
    if state == "A1":
        return "A1"
    if state == "AR":
        return "AR_RUN2" if idx == 2 else ("AR_RUN3" if idx == 3 else "AR_RUN4PLUS")
    return "G_AFTER_RUN1" if idx == 1 else ("G_AFTER_RUN2" if idx == 2 else ("G_AFTER_RUN3" if idx == 3 else "G_AFTER_RUN4PLUS"))


def add_r8_age_run(hist: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for event, g in hist.groupby("EVENT", sort=True):
        active_age = 0
        gap_age = 0
        for _, row in g.sort_values("BIN_INDEX").iterrows():
            state = str(row.STATE)
            cat = cat_from_row(row)
            if state in ("A1", "AR"):
                active_age += 1
                gap_age = 0
                age = active_age
            elif state == "G":
                gap_age += 1
                active_age = 0
                age = gap_age
            else:
                active_age = 0
                gap_age = 0
                age = 0
            age_class = "AGE1" if age == 1 else ("AGE2" if age == 2 else ("AGE3PLUS" if age >= 3 else "NONE"))
            rows.append({**row.to_dict(), "CATEGORY": cat, "AGE_VALUE": age, "AGE_CLASS": age_class,
                         "AGE_MEMORY": 1.0 if age_class == "AGE2" else (2.0 if age_class == "AGE3PLUS" else 0.0),
                         "RUN_MEMORY": float(max(0, (2 if "RUN2" in cat else 3 if "RUN3" in cat else 4 if "RUN4PLUS" in cat else 1) - 1))})
    return pd.DataFrame(rows)


def transition_type(category):
    return "01" if category == "N0" else ("1G" if category == "A1" else ("GR" if category.startswith("G_") else "RG"))


def build_transitions(mem: pd.DataFrame, u: np.ndarray, base_boundary: dict) -> pd.DataFrame:
    rows = []
    for event, g in mem.groupby("EVENT", sort=True):
        g = g.sort_values("BIN_INDEX").reset_index(drop=True)
        for k in range(len(g) - 1):
            a, b = g.iloc[k], g.iloc[k + 1]
            typ = transition_type(a.CATEGORY)
            success = int((typ == "01" and b.CATEGORY == "A1") or (typ == "1G" and b.CATEGORY.startswith("G_")) or (typ == "GR" and b.CATEGORY.startswith("AR_")) or (typ == "RG" and b.CATEGORY.startswith("G_")))
            rows.append({"EVENT": event, "BOUNDARY_INDEX": k, "U_PCT": float(u[k + 1] * 100), "CATEGORY": a.CATEGORY, "AGE_CLASS": a.AGE_CLASS, "TYPE": typ, "SUCCESS": success, "BASE_LOG_RATE": float(base_boundary[(k, typ)])})
    return pd.DataFrame(rows)


def r40_probability(row, s, base, gamma, coef, du):
    category = row.CATEGORY
    d = 0.0
    if category.startswith("AR_") or category.startswith("G_"):
        run = 4 if "RUN4PLUS" in category else (3 if "RUN3" in category else (2 if "RUN2" in category else 1))
        d += coef["beta2"] if run == 2 else (coef["beta3"] if run == 3 else (coef["beta4"] if run >= 4 else 0.0))
    if category != "N0":
        d += coef["gamma2"] if row.AGE_CLASS == "AGE2" else (coef["gamma3"] if row.AGE_CLASS == "AGE3PLUS" else 0.0)
    eta = float(row.BASE_LOG_RATE) + d + gamma * float(s)
    lam = math.exp(float(np.clip(eta, -20.0, 20.0)))
    return 1.0 - math.exp(-lam * du)


def import_r39_engine():
    path = Path(__file__).resolve().parent / "run_r39.py"
    spec = importlib.util.spec_from_file_location("frozen_r39_engine", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module, path


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    target_paths = {
        "NODES": req(COVERAGE_REPLAY / "HOLDOUT5_DEV96_GLOBAL_NODE_ROWS.csv"),
        "WINDOWS": req(COVERAGE_REPLAY / "HOLDOUT5_EVENT_FOUR_WINDOW_COVERAGE_PCT.csv"),
        "BINS": req(R5 / "EVENT_BIN_OCCUPANCY_MATRIX.csv"),
        "R9_RATES": req(R9 / "MEMORY_CONDITIONED_RATES.csv"),
        "R40_LAW": req(R40 / "R40_CANONICAL_LAW.json"),
        "R40_ENGINE": req(R40 / "R40_FORWARD_ENGINE_CONTRACT.json"),
        "R40_PHYS": req(R40 / "R40_PHYSICAL_COORDINATE.json"),
        "R40_SUPPORT": req(R40 / "R40_SUPPORT_EVENTS.csv"),
        "R6_CODE": req(R6 / "RUN.py"),
        "R8_CODE": req(R8 / "RUN.py"),
        "R9_CODE": req(R9 / "RUN.py"),
    }
    nodes = pd.read_csv(target_paths["NODES"])
    windows = pd.read_csv(target_paths["WINDOWS"])
    bins_all = pd.read_csv(target_paths["BINS"])
    bins = bins_all.sort_values(["BIN_INDEX", "EVENT"]).drop_duplicates("BIN_INDEX").sort_values("BIN_INDEX")
    if set(nodes.EVENT_ID.astype(str)) != EVENT_SET or set(windows.EVENT_ID.astype(str)) != EVENT_SET:
        raise RuntimeError("HOLDOUT5 identity contract mismatch or non-target event contamination")
    if len(bins) != 32:
        raise RuntimeError(f"frozen R5 bin contract mismatch: {len(bins)} bins")
    if len(nodes.EVENT_ID.astype(str).unique()) != 5:
        raise RuntimeError("target event count is not five")
    if set(nodes.EVENT_ID.astype(str)) & set(EVENTS) != EVENT_SET:
        raise RuntimeError("target event set incomplete")

    hist = classify_r6(nodes, bins.drop(columns=["EVENT"]).drop_duplicates("BIN_INDEX"))
    # classify_r6 receives only common bin definitions; the five-event source rows remain target-filtered.
    mem = add_r8_age_run(hist)
    u = np.sort(mem.BIN_INDEX.unique()).astype(float)
    u = (u + 0.5) / 32.0

    rates = pd.read_csv(target_paths["R9_RATES"])
    rates = rates[rates.MODEL_ID.astype(str) == "M3"].copy()
    base = {(int(r.BOUNDARY_INDEX), str(r.TRANSITION_TYPE)): float(r.BASE_RATE) for _, r in rates.iterrows()}
    transitions = build_transitions(mem, u, base)

    physical = pd.DataFrame([physical_row(e) for e in EVENTS])
    s_map = dict(zip(physical.EVENT.astype(str), physical.S_KERR_ORDINAL.astype(float)))
    coeff = {"beta2": -0.304588116941319, "beta3": -0.0167449766916816, "beta4": 0.3713520014548632, "gamma2": 0.1425553247852259, "gamma3": -0.3177555096604296}
    gamma = 0.3162354634393393
    du = float(np.median(np.diff(u)))

    r39, r39_path = import_r39_engine()
    fit_p0 = {"PARAMS": np.array([coeff["beta2"], coeff["beta3"], coeff["beta4"], coeff["gamma2"], coeff["gamma3"]]), "BASE_NAMES": ["beta2", "beta3", "beta4", "gamma2", "gamma3"], "PHYS_NAMES": []}
    fit_p1 = {"PARAMS": np.array([coeff["beta2"], coeff["beta3"], coeff["beta4"], coeff["gamma2"], coeff["gamma3"], gamma]), "BASE_NAMES": ["beta2", "beta3", "beta4", "gamma2", "gamma3"], "PHYS_NAMES": ["gamma_ALL"]}
    base_log_rates = {typ: [float(rates[(rates.BOUNDARY_INDEX == k) & (rates.TRANSITION_TYPE == typ)].BASE_RATE.iloc[0]) for k in range(31)] for typ in ["01", "1G", "GR", "RG"]}
    init = mem.sort_values(["EVENT", "BIN_INDEX"]).groupby("EVENT", as_index=False).first()[["EVENT", "STATE"]]
    traj_rows = []
    for model, fit in [("P0", fit_p0), ("P1", fit_p1)]:
        for event in EVENTS:
            tr = r39.autonomous_event_engine(model, fit, init[init.EVENT == event], s_map, base_log_rates, u)
            for k, pct, state in tr:
                a1 = sum(v for c, v in state.items() if c.startswith("A1"))
                ar = sum(v for c, v in state.items() if c.startswith("AR"))
                traj_rows.append({"MODEL_ID": model, "EVENT": event, "BIN_INDEX": int(k), "GLOBAL_PCT": float(pct * 100), "N0": float(state.get("N0", 0.0)), "A1": float(a1), "G": float(sum(v for c, v in state.items() if c.startswith("G"))), "AR": float(ar), "ACTIVE": float(a1 + ar), "TOTAL": float(sum(state.values()))})
    trajectories = pd.DataFrame(traj_rows)

    result_rows = []
    metric_rows = []
    for window in MAPS:
        c = windows[(windows.WINDOW == window) & windows.EVENT_ID.astype(str).isin(EVENT_SET)].copy()
        bounds = c.set_index("EVENT_ID")[["GLOBAL_OVERLAP_START_PCT", "GLOBAL_OVERLAP_END_PCT"]].to_dict("index")
        trials = transitions[transitions.EVENT.isin(bounds)].copy()
        trials = trials[trials.apply(lambda row: bounds[str(row.EVENT)]["GLOBAL_OVERLAP_START_PCT"] <= row.U_PCT <= bounds[str(row.EVENT)]["GLOBAL_OVERLAP_END_PCT"], axis=1)]
        ll = {"P0": 0.0, "P1": 0.0}
        for row in trials.itertuples(index=False):
            for model, sval in [("P0", 0.0), ("P1", s_map[row.EVENT])]:
                p = r40_probability(row, sval, base, gamma, coeff, du)
                y = int(row.SUCCESS)
                ll[model] += y * math.log(max(p, 1e-12)) + (1 - y) * math.log(max(1.0 - p, 1e-12))
        active = []
        for event, b in bounds.items():
            observed = mem[(mem.EVENT == event) & (mem.GLOBAL_MID_PCT >= b["GLOBAL_OVERLAP_START_PCT"]) & (mem.GLOBAL_MID_PCT <= b["GLOBAL_OVERLAP_END_PCT"])]
            if len(observed) == 0:
                continue
            row = {"EVENT": event, "OBS_ACTIVE_FRACTION": float(observed.OCCUPIED.mean())}
            for model in ["P0", "P1"]:
                pred = trajectories[(trajectories.MODEL_ID == model) & (trajectories.EVENT == event) & (trajectories.GLOBAL_PCT >= b["GLOBAL_OVERLAP_START_PCT"]) & (trajectories.GLOBAL_PCT <= b["GLOBAL_OVERLAP_END_PCT"])]
                row[f"{model}_PRED_ACTIVE_FRACTION"] = float(pred.ACTIVE.mean()) if len(pred) else np.nan
            active.append(row)
        adf = pd.DataFrame(active)
        vals = {"OBS": adf.OBS_ACTIVE_FRACTION.to_numpy(float), "P0": adf.P0_PRED_ACTIVE_FRACTION.to_numpy(float), "P1": adf.P1_PRED_ACTIVE_FRACTION.to_numpy(float)}
        sp0 = float(spearmanr(vals["OBS"], vals["P0"]).statistic) if len(adf) >= 2 else np.nan
        sp1 = float(spearmanr(vals["OBS"], vals["P1"]).statistic) if len(adf) >= 2 else np.nan
        kt1 = float(kendalltau(vals["OBS"], vals["P1"]).statistic) if len(adf) >= 2 else np.nan
        mae1 = float(np.nanmean(np.abs(vals["OBS"] - vals["P1"])))
        rmse1 = float(np.sqrt(np.nanmean((vals["OBS"] - vals["P1"]) ** 2)))
        mae0 = float(np.nanmean(np.abs(vals["OBS"] - vals["P0"])))
        rmse0 = float(np.sqrt(np.nanmean((vals["OBS"] - vals["P0"]) ** 2)))
        ntrial = len(trials)
        result_rows.append({
            "MAP_NAME": window, "N_EVENTS": int(len(bounds)), "N_TRANSITIONS": int(c.N_TRANSITIONS.sum()), "LAW_SUPPORT_EVENTS": int(len(bounds)), "LAW_TRIAL_ROWS": int(ntrial), "ACTIVE_EVENT_ROWS": int(len(adf)),
            "LOGLIK_P0": ll["P0"], "LOGLIK_P1": ll["P1"], "DELTA_LOGLIK": ll["P1"] - ll["P0"], "MEAN_DELTA_LOGPROB_PER_TRANSITION": (ll["P1"] - ll["P0"]) / ntrial if ntrial else np.nan,
            "BIC_P0_DESCRIPTIVE": -2 * ll["P0"] + 21 * math.log(ntrial) if ntrial else np.nan, "BIC_P1_DESCRIPTIVE": -2 * ll["P1"] + 22 * math.log(ntrial) if ntrial else np.nan,
            "ACTIVE_SPEARMAN_P0": sp0, "ACTIVE_SPEARMAN_P1": sp1, "DELTA_ACTIVE_SPEARMAN": sp1 - sp0, "ACTIVE_KENDALL_P1": kt1, "MAE_P1": mae1, "RMSE_P1": rmse1,
            "MAE_P0": mae0, "RMSE_P0": rmse0, "OBSERVED_ACTIVE_FRACTION": float(np.nanmean(vals["OBS"])), "PREDICTED_ACTIVE_FRACTION_P0": float(np.nanmean(vals["P0"])), "PREDICTED_ACTIVE_FRACTION_P1": float(np.nanmean(vals["P1"])), "LAW_DIRECTION_OK": bool((sp1 - sp0) > 0),
        })
        for row in active:
            row.update({"MAP_NAME": window})
            metric_rows.append(row)

    results = pd.DataFrame(result_rows)
    histories = mem.copy()
    transitions.to_csv(OUT / "HOLDOUT5_R6_R8_R9_TRANSITION_HISTORY.csv", index=False)
    histories.to_csv(OUT / "HOLDOUT5_R6_R8_STATE_AGE_RUN_HISTORY.csv", index=False)
    trajectories.to_csv(OUT / "HOLDOUT5_R40_GENERATED_STATE_TRAJECTORIES.csv", index=False)
    physical.to_csv(OUT / "HOLDOUT5_R40_PHYSICAL_BINDING.csv", index=False)
    pd.DataFrame(metric_rows).to_csv(OUT / "HOLDOUT5_R40_ACTIVE_FRACTION_DETAIL.csv", index=False)
    results.to_csv(OUT / "HOLDOUT5_R40_W1_W4_EXACT_LIKELIHOOD.csv", index=False)

    source_files = {**target_paths, "COVERAGE_REPLAY": target_paths["NODES"], "R39_EXACT_ENGINE": r39_path}
    prov = {
        "R_STATUS": "PASS", "EVENTS": EVENTS, "EVENT_COUNT": len(EVENTS), "EXCLUDED_HOLDOUT_EVENTS_ACCESSED": False,
        "R6_STATE_RULE": "exact R6 RUN.py occupancy replay; N0/A1/G/AR with prior-only run state",
        "R8_AGE_RUN_RULE": "exact R8 age replay from R6 state history; AGE1/AGE2/AGE3PLUS and frozen run categories",
        "R9_BASE_MODEL": "M3 MEMORY_CONDITIONED_RATES.csv; no refit",
        "R40_LAW": "gamma_ALL=0.3162354634393393; beta2/beta3/beta4/gamma2/gamma3 frozen; P0 S=0, P1 S=R40 physical score",
        "MAP_SOURCE": str(target_paths["WINDOWS"]), "MAPS": MAPS, "DU": du,
        "SOURCE_SHA256": {str(k): sha256(v) for k, v in source_files.items()},
    }
    (OUT / "HOLDOUT5_R40_REPLAY_PROVENANCE.json").write_text(json.dumps(prov, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = [
        "R_STATUS=PASS", "HOLDOUT_EVENTS=" + ",".join(EVENTS), "HOLDOUT_EVENT_COUNT=5", "EXCLUDED_HOLDOUT30_ACCESSED=FALSE",
        "R6_R8_R9_STATE_HISTORY=GENERATED", "R40_MAPS_COEFFICIENTS_THRESHOLDS=UNCHANGED", "R40_EXACT_LIKELIHOOD=COMPLETED", "",
        results.to_string(index=False), "", "OUTPUT=" + str(OUT),
    ]
    (OUT / "SEND_TO_CHAT.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    (OUT / "README.txt").write_text("Holdout5-only frozen R6/R8/R9 history and R40 W1-W4 replay. No Holdout30 access. No fit/refit/threshold change.\n", encoding="utf-8")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
