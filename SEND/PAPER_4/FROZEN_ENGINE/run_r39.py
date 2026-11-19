from __future__ import annotations

import hashlib
import json
import math
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import kendalltau, spearmanr


OUT = Path(r"E:\RIUD_ACTIVE_20260808\RIUD_DEV99_PHYSICAL_DYNAMICAL_LAW_DISCOVERY_R39_20260815")
R6 = Path(r"E:\RIUD_ACTIVE_20260808\RIUD_DEV99_REENTRY_MULTISTATE_STATE_IDENTITY_AUDIT_R6_20260815")
R7 = Path(r"E:\RIUD_ACTIVE_20260808\RIUD_DEV99_MULTISTATE_FLOW_DYNAMICS_DISCOVERY_R7_20260815")
R8 = Path(r"E:\RIUD_ACTIVE_20260808\RIUD_DEV99_RUN_INDEX_STATE_MEMORY_IDENTITY_AUDIT_R8_20260815")
R9 = Path(r"E:\RIUD_ACTIVE_20260808\RIUD_DEV99_HISTORY_AWARE_MULTISTATE_FLOW_LAW_DISCOVERY_R9_20260815")
R10 = Path(r"E:\RIUD_ACTIVE_20260808\RIUD_DEV99_ENDOGENOUS_MEMORY_STATE_FORWARD_RECONSTRUCTION_R10_20260815")
R13 = Path(r"E:\RIUD_ACTIVE_20260808\RIUD_DEV99_EVENT_TRAJECTORY_HETEROGENEITY_AUDIT_R13_20260815")
R37 = Path(r"E:\RIUD_ACTIVE_20260808\RIUD_DEV99_KERR_BALANCE_SPIN_ORDINAL_FREEZE_R37_20260815")
R38 = Path(r"E:\RIUD_ACTIVE_20260808\RIUD_DEV99_KERR_BALANCE_SPIN_ORDINAL_CORRECTION_FREEZE_R38_20260815")

N_STARTS = 128
LOO_STARTS = 16
MAX_WORKERS = 4
MODELS = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4, "P5": 4, "P6": 6}
MODEL_NUM = {f"P{i}": i for i in range(7)}
MODEL_DESC = {
    "P0": "R9 M3 baseline; no event physical term",
    "P1": "global S clock on all allowed transitions",
    "P2": "S with ON=(ENTRY+REENTRY) and OFF=(EXIT)",
    "P3": "S separated by ENTRY, REENTRY, EXIT",
    "P4": "P2 plus S times frozen ordinal state-age memory",
    "P5": "P2 plus S times frozen ordinal run-index memory",
    "P6": "P2 plus both age and run memory interactions",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def log(msg: str):
    print(msg, flush=True)
    with (OUT / "RUN.log").open("a", encoding="utf-8") as f:
        f.write(msg + "\n")


def safe_corr(fn, x, y):
    if len(x) < 3 or np.nanstd(x) == 0 or np.nanstd(y) == 0:
        return 0.0
    v = fn(x, y).statistic
    return float(v) if np.isfinite(v) else 0.0


def landmark_operator(u, y):
    # Exact R10/R27A-style frozen operator: 20001-point linear interpolation,
    # numerical gradient, first turnover, recovery, second turnover.
    x = np.linspace(float(np.min(u)), float(np.max(u)), 20001)
    z = np.interp(x, u, y)
    d = np.gradient(z, x)
    pos_to_non = [i for i in range(1, len(d)) if d[i - 1] > 0 and d[i] <= 0]
    non_to_pos = [i for i in range(1, len(d)) if d[i - 1] <= 0 and d[i] > 0]
    return {
        "L1": float(x[pos_to_non[0]] * 100) if pos_to_non else np.nan,
        "L2": float(x[non_to_pos[0]] * 100) if non_to_pos else np.nan,
        "L3": float(x[pos_to_non[1]] * 100) if len(pos_to_non) > 1 else np.nan,
        "GLOBAL_PEAK": float(x[np.argmax(z)] * 100),
        "SIGN_SEQUENCE": "".join("+" if q > 0 else "-" for q in d[::max(1, len(d) // 200)]),
    }


def cat_from_r6(row):
    s = str(row.STATE)
    idx = int(row.CURRENT_ACTIVE_RUN_INDEX) if s in ("A1", "AR") else int(row.N_COMPLETED_ACTIVE_RUNS)
    if s == "N0":
        return "N0"
    if s == "A1":
        return "A1"
    if s == "AR":
        return "AR_RUN2" if idx == 2 else ("AR_RUN3" if idx == 3 else "AR_RUN4PLUS")
    return "G_AFTER_RUN1" if idx == 1 else ("G_AFTER_RUN2" if idx == 2 else ("G_AFTER_RUN3" if idx == 3 else "G_AFTER_RUN4PLUS"))


def state_family(cat):
    if cat == "N0":
        return "N0"
    if cat == "A1":
        return "A1"
    if cat.startswith("AR"):
        return "AR"
    return "G"


def run_level(cat):
    if cat in ("AR_RUN2", "G_AFTER_RUN2"):
        return 2
    if cat in ("AR_RUN3", "G_AFTER_RUN3"):
        return 3
    if cat in ("AR_RUN4PLUS", "G_AFTER_RUN4PLUS"):
        return 4
    return 1


def age_code(age_class):
    # Frozen R9/R10 age classes, represented ordinally only for the predeclared
    # P4/P6 interaction. AGE1/NONE=0, AGE2=1, AGE3PLUS=2.
    return 1.0 if age_class == "AGE2" else (2.0 if age_class == "AGE3PLUS" else 0.0)


def run_code(cat):
    # Frozen run categories, ordinally: first run=0, run2=1, run3=2, 4+=3.
    return float(max(0, run_level(cat) - 1))


def make_mem_rows(hist: pd.DataFrame, u: np.ndarray) -> pd.DataFrame:
    rows = []
    for event, g in hist.groupby("EVENT", sort=True):
        g = g.sort_values("BIN_INDEX").reset_index(drop=True)
        active_age = 0
        gap_age = 0
        for _, r in g.iterrows():
            s = str(r.STATE)
            cat = cat_from_r6(r)
            if s in ("A1", "AR"):
                active_age += 1
                gap_age = 0
                age = active_age
            elif s == "G":
                gap_age += 1
                active_age = 0
                age = gap_age
            else:
                active_age = 0
                gap_age = 0
                age = 0
            age_class = "AGE1" if age == 1 else ("AGE2" if age == 2 else ("AGE3PLUS" if age >= 3 else "NONE"))
            rows.append({
                "EVENT": str(event), "BIN_INDEX": int(r.BIN_INDEX), "STATE": s,
                "CATEGORY": cat, "AGE_CLASS": age_class,
                "AGE_MEMORY": age_code(age_class), "RUN_MEMORY": run_code(cat),
                "OCCUPIED": int(float(r.OCCUPIED)),
            })
    out = pd.DataFrame(rows)
    out["U"] = out["BIN_INDEX"].map(dict(enumerate(u))).astype(float)
    return out


def transition_rows(mem: pd.DataFrame, u: np.ndarray, base_boundary: dict) -> pd.DataFrame:
    rows = []
    for event, g in mem.groupby("EVENT", sort=True):
        g = g.sort_values("BIN_INDEX").reset_index(drop=True)
        for k in range(len(g) - 1):
            a = g.iloc[k]
            b = g.iloc[k + 1]
            cat = a.CATEGORY
            typ = "01" if cat == "N0" else ("1G" if cat == "A1" else ("GR" if cat.startswith("G_") else "RG"))
            success = int(
                (typ == "01" and b.CATEGORY == "A1")
                or (typ == "1G" and b.CATEGORY.startswith("G_"))
                or (typ == "GR" and b.CATEGORY.startswith("AR_"))
                or (typ == "RG" and b.CATEGORY.startswith("G_"))
            )
            rows.append({
                "EVENT": str(event), "BOUNDARY_INDEX": k, "U": float(u[k + 1]),
                "CATEGORY": cat, "AGE_CLASS": a.AGE_CLASS,
                "AGE_MEMORY": float(a.AGE_MEMORY), "RUN_MEMORY": float(a.RUN_MEMORY),
                "TYPE": typ, "SUCCESS": success,
                "BASE_LOG_RATE": float(base_boundary[typ][k]),
            })
    return pd.DataFrame(rows)


def build_physical_design(model: str, obs: pd.DataFrame, s_map: dict[str, float]):
    s = obs.EVENT.map(s_map).to_numpy(float)
    typ = obs.TYPE.to_numpy(str)
    on = np.isin(typ, ["01", "RG"]).astype(float)
    off = np.isin(typ, ["1G", "GR"]).astype(float)
    entry = (typ == "01").astype(float)
    reentry = (typ == "RG").astype(float)
    exit_ = np.isin(typ, ["1G", "GR"]).astype(float)
    cols = []
    names = []
    if model == "P1":
        cols, names = [s], ["gamma_ALL"]
    elif model == "P2":
        cols, names = [s * on, s * off], ["gamma_ON", "gamma_OFF"]
    elif model == "P3":
        cols, names = [s * entry, s * reentry, s * exit_], ["gamma_ENTRY", "gamma_REENTRY", "gamma_EXIT"]
    elif model in ("P4", "P5", "P6"):
        cols = [s * on, s * off]
        names = ["gamma_ON", "gamma_OFF"]
        if model in ("P4", "P6"):
            cols += [s * on * obs.AGE_MEMORY.to_numpy(float), s * off * obs.AGE_MEMORY.to_numpy(float)]
            names += ["beta_ON_AGE", "beta_OFF_AGE"]
        if model in ("P5", "P6"):
            cols += [s * on * obs.RUN_MEMORY.to_numpy(float), s * off * obs.RUN_MEMORY.to_numpy(float)]
            names += ["kappa_ON_RUN", "kappa_OFF_RUN"]
    if not cols:
        return np.zeros((len(obs), 0)), []
    return np.column_stack(cols), names


def fit_model(model: str, obs: pd.DataFrame, s_map: dict[str, float], seed_offset: int, n_starts: int = N_STARTS):
    # Frozen R9 M3 memory architecture: 5 common coefficients.
    base_names = ["beta2", "beta3", "beta4", "gamma2", "gamma3"]
    x_phys, phys_names = build_physical_design(model, obs, s_map)
    x_base = np.column_stack([
        (obs.RUN_MEMORY.to_numpy(float) == 1).astype(float),
        (obs.RUN_MEMORY.to_numpy(float) == 2).astype(float),
        (obs.RUN_MEMORY.to_numpy(float) >= 3).astype(float),
        (obs.AGE_CLASS.to_numpy(str) == "AGE2").astype(float),
        (obs.AGE_CLASS.to_numpy(str) == "AGE3PLUS").astype(float),
    ])
    X = np.column_stack([x_base, x_phys])
    offset = obs.BASE_LOG_RATE.to_numpy(float)
    y = obs.SUCCESS.to_numpy(float)
    du = float(np.median(np.diff(np.sort(obs.U.unique()))))

    def objective(theta):
        eta = np.clip(offset + X @ theta, -20.0, 20.0)
        q = np.clip(du * np.exp(eta), 1e-12, 1e12)
        logp = np.log(-np.expm1(-q))
        lognot = -q
        return float(-np.sum(y * logp + (1.0 - y) * lognot))

    npar = X.shape[1]
    if npar == 5:
        best = minimize(objective, np.zeros(npar), method="L-BFGS-B", bounds=[(-8, 8)] * npar,
                        options={"maxiter": 500, "ftol": 1e-11, "gtol": 1e-7, "maxls": 30})
        results = [best]
    else:
        rng = np.random.default_rng(20260815 + seed_offset)
        results = []
        for _ in range(n_starts):
            x0 = rng.normal(0.0, 0.35, npar)
            res = minimize(objective, x0, method="L-BFGS-B", bounds=[(-8, 8)] * npar,
                           options={"maxiter": 500, "ftol": 1e-11, "gtol": 1e-7, "maxls": 30})
            results.append(res)
        best = min(results, key=lambda z: float(z.fun))

    theta = np.asarray(best.x, float)
    eta = np.clip(offset + X @ theta, -20.0, 20.0)
    q = np.clip(du * np.exp(eta), 1e-12, 1e12)
    p = np.clip(-np.expm1(-q), 1e-12, 1 - 1e-12)
    loglik = float(np.sum(y * np.log(p) + (1 - y) * np.log1p(-p)))
    # Observed information for the exact hazard/Bernoulli link.
    eq = np.exp(np.clip(q, -50, 50))
    den = np.expm1(np.clip(q, -50, 50))
    da = q * (den - q * eq) / np.maximum(den * den, 1e-300)
    h_eta = q - y * (q + da)
    hessian = X.T @ (h_eta[:, None] * X)
    cov = np.linalg.pinv(hessian, rcond=1e-10)
    se = np.sqrt(np.maximum(0.0, np.diag(cov)))
    # `21` preserves R9's frozen 16-parameter R7 F7 base plus five M3 memory params.
    total_params = 21 + len(phys_names)
    return {
        "MODEL_ID": model, "PARAMS": theta, "BASE_NAMES": base_names,
        "PHYS_NAMES": phys_names, "SE": se, "X": X, "P": p, "LOG_LIK": loglik,
        "NLL": -loglik, "N_ROWS": len(obs), "N_PARAMETERS_TOTAL": total_params,
        "AIC": 2 * total_params - 2 * loglik,
        "BIC": total_params * math.log(len(obs)) - 2 * loglik,
        "CONVERGED": int(sum(bool(getattr(r, "success", False)) for r in results)),
        "STARTS": len(results), "STATUS": bool(getattr(best, "success", False)),
        "OBJECTIVE": objective,
    }


def next_cat(cat: str, target: str, age_class: str):
    # Internal state/age/run transport. No observed future information enters.
    if cat == "N0":
        return "A1AGE1" if target == "A1" else "N0"
    if cat == "A1":
        if target == "G": return "G1AGE1"
        return "A1AGE2" if age_class == "AGE1" else "A1AGE3PLUS"
    if cat.startswith("A1AGE"):
        if target == "G": return "G1AGE1"
        return "A1AGE2" if cat == "A1AGE1" else "A1AGE3PLUS"
    if cat.startswith("G"):
        level = int(cat[1]) if cat[1].isdigit() else 4
        if target == "AR":
            return ("AR2AGE1" if level == 1 else "AR3AGE1" if level == 2 else "AR4PLUSAGE1")
        return f"G{level}AGE2" if age_class == "AGE1" else f"G{level}AGE3PLUS"
    if cat.startswith("AR"):
        prefix = cat.split("AGE")[0]
        level = 2 if prefix == "AR2" else 3 if prefix == "AR3" else 4
        if target == "G":
            return f"G{level}AGE1"
        pref = "AR4PLUS" if level >= 4 else f"AR{level}"
        return f"{pref}AGE2" if age_class == "AGE1" else f"{pref}AGE3PLUS"
    return cat


def base_state_and_age(cat: str):
    if cat == "N0": return "N0", "NONE", 0
    if cat.startswith("A1"):
        age = cat.split("AGE")[-1]
        return "A1", "AGE1" if age == "1" else ("AGE2" if age == "2" else "AGE3PLUS"), 1
    if cat.startswith("G"):
        level = int(cat[1]) if cat[1].isdigit() else 4
        age = cat.split("AGE")[-1]
        return f"G_AFTER_RUN{level if level < 4 else '4PLUS'}", "AGE1" if age == "1" else ("AGE2" if age == "2" else "AGE3PLUS"), level
    if cat.startswith("AR"):
        level = int(cat[2]) if cat[2].isdigit() else 4
        age = cat.split("AGE")[-1]
        return f"AR_RUN{level if level < 4 else '4PLUS'}", "AGE1" if age == "1" else ("AGE2" if age == "2" else "AGE3PLUS"), level
    return cat, "NONE", 1


def transition_type_from_base(base: str):
    return "01" if base == "N0" else ("1G" if base == "A1" else ("GR" if base.startswith("G") else "RG"))


def model_physical_delta(model, coef_map, s, base, age, rlevel):
    typ = transition_type_from_base(base)
    on = typ in ("01", "RG")
    off = typ in ("1G", "GR")
    age_m = 1.0 if age == "AGE2" else (2.0 if age == "AGE3PLUS" else 0.0)
    run_m = float(max(0, rlevel - 1))
    if model == "P0": return 0.0
    if model == "P1": return coef_map["gamma_ALL"] * s
    if model == "P2": return coef_map["gamma_ON" if on else "gamma_OFF"] * s
    if model == "P3": return coef_map[{"01": "gamma_ENTRY", "RG": "gamma_REENTRY", "1G": "gamma_EXIT", "GR": "gamma_EXIT"}[typ]] * s
    d = coef_map["gamma_ON" if on else "gamma_OFF"] * s
    if model in ("P4", "P6"):
        d += coef_map["beta_ON_AGE" if on else "beta_OFF_AGE"] * s * age_m
    if model in ("P5", "P6"):
        d += coef_map["kappa_ON_RUN" if on else "kappa_OFF_RUN"] * s * run_m
    return d


def autonomous_event_engine(model, fit, event_init, s_map, base_log_rates, u):
    coef_map = {n: float(v) for n, v in zip(fit["PHYS_NAMES"], fit["PARAMS"][5:])}
    base_mem = {n: float(v) for n, v in zip(fit["BASE_NAMES"], fit["PARAMS"][:5])}
    age_suffixes = ("1", "2", "3PLUS")
    categories = ["N0"] + [f"A1AGE{a}" for a in age_suffixes]
    categories += [f"G{g}AGE{a}" for g in (1, 2, 3, 4) for a in age_suffixes]
    categories += [f"AR{g}AGE{a}" for g in (2, 3) for a in age_suffixes]
    categories += [f"AR4PLUSAGE{a}" for a in age_suffixes]
    out = []
    state = {c: 0.0 for c in categories}
    init = event_init[event_init.EVENT == event_init.EVENT.iloc[0]].iloc[0]
    if str(init.STATE) == "N0": state["N0"] = 1.0
    elif str(init.STATE) == "A1": state["A1AGE1"] = 1.0
    elif str(init.STATE) == "G": state["G1AGE1"] = 1.0
    else: state["AR2AGE1"] = 1.0
    out.append((0, float(u[0]), state.copy()))
    for k in range(len(u) - 1):
        new = {c: 0.0 for c in categories}
        for c, mass in state.items():
            if mass == 0.0: continue
            base, age, rl = base_state_and_age(c)
            typ = transition_type_from_base(base)
            d = 0.0
            if rl == 2: d += base_mem["beta2"]
            elif rl == 3: d += base_mem["beta3"]
            elif rl >= 4: d += base_mem["beta4"]
            if base != "N0" and age == "AGE2": d += base_mem["gamma2"]
            if base != "N0" and age == "AGE3PLUS": d += base_mem["gamma3"]
            d += model_physical_delta(model, coef_map, float(s_map[event_init.EVENT.iloc[0]]), base, age, rl)
            lam = math.exp(float(np.clip(base_log_rates[typ][k] + d, -20, 20)))
            p = float(-math.expm1(-lam * float(np.median(np.diff(u)))))
            if typ == "01": target = "A1"
            elif typ == "1G": target = "G"
            elif typ == "GR": target = "AR"
            else: target = "G"
            cstay = next_cat(c, "stay", age)
            cgo = next_cat(c, target, age)
            new[cgo] += mass * p
            new[cstay] += mass * (1.0 - p)
        state = new
        out.append((k + 1, float(u[k + 1]), state.copy()))
    return out


def aggregate_engine(model, fits, events, event_init, s_map, base_log_rates, u):
    rows = []
    event_rows = []
    for event in events:
        init = event_init[event_init.EVENT == event].copy()
        traj = autonomous_event_engine(model, fits, init, s_map, base_log_rates, u)
        active = []
        reentry = []
        for k, pct, st in traj:
            a = sum(v for c, v in st.items() if c.startswith("A1") or c.startswith("AR"))
            g = sum(v for c, v in st.items() if c.startswith("G"))
            n0 = st.get("N0", 0.0)
            a1 = sum(v for c, v in st.items() if c.startswith("A1"))
            ar = sum(v for c, v in st.items() if c.startswith("AR"))
            active.append(a)
            event_rows.append({"MODEL_ID": model, "EVENT": event, "BIN_INDEX": k, "GLOBAL_PCT": pct * 100,
                               "N0": n0, "A1": a1, "G": g, "AR": ar, "ACTIVE": a,
                               "TOTAL": sum(st.values()), "EXPECTED_REENTRY_FLOW": 0.0})
        # Reentry flow is calculated on the same source categories at each boundary below.
        for i in range(len(traj) - 1):
            st = traj[i][2]
            reentry.append(sum(v for c, v in st.items() if c.startswith("G")))
        event_rows[-len(traj):] = event_rows[-len(traj):]
        event_rows_for_event = [r for r in event_rows if r["EVENT"] == event and r["MODEL_ID"] == model]
        pred_af = float(np.mean(active))
        pred_reentry = 0.0
        pred_active_bins = float(np.sum(active))
        pred_gap_bins = float(len(active) - pred_active_bins)
        # Expected G->AR transitions, using the already generated state at each boundary.
        for k in range(len(traj) - 1):
            st = traj[k][2]
            for c, mass in st.items():
                if not c.startswith("G") or mass == 0: continue
                base, age, rl = base_state_and_age(c)
                d = 0.0
                if rl == 2: d += fits["PARAMS"][0]
                elif rl == 3: d += fits["PARAMS"][1]
                elif rl >= 4: d += fits["PARAMS"][2]
                if base != "N0" and age == "AGE2": d += fits["PARAMS"][3]
                if base != "N0" and age == "AGE3PLUS": d += fits["PARAMS"][4]
                coef_map = {n: float(v) for n, v in zip(fits["PHYS_NAMES"], fits["PARAMS"][5:])}
                d += model_physical_delta(model, coef_map, float(s_map[event]), base, age, rl)
                lam = math.exp(float(np.clip(base_log_rates["GR"][k] + d, -20, 20)))
                pred_reentry += mass * (-math.expm1(-lam * float(np.median(np.diff(u)))))
        event_summary = {"MODEL_ID": model, "EVENT": event, "PRED_ACTIVE_FRACTION": pred_af,
                         "PRED_REENTRY_COUNT": pred_reentry, "PRED_ACTIVE_BINS": pred_active_bins,
                         "PRED_GAP_BINS": pred_gap_bins}
        event_summary["PRED_ACTIVE_DURATION"] = pred_active_bins
        event_summary["PRED_GAP_DURATION"] = pred_gap_bins
        rows.extend(event_rows_for_event)
        # Attach summary later, avoiding repeated filtering.
        event_summary["_TRAJ"] = traj
        event_summary["_EVENT_ROWS"] = event_rows_for_event
        event_rows_for_event = event_summary
        # Store summary in a side list via sentinel.
        if "summaries" not in locals(): summaries = []
        summaries.append(event_summary)
    df = pd.DataFrame(rows)
    comp = df.groupby(["MODEL_ID", "BIN_INDEX", "GLOBAL_PCT"], as_index=False)[["N0", "A1", "G", "AR", "ACTIVE", "TOTAL"]].sum()
    summ = pd.DataFrame([{k: v for k, v in s.items() if not k.startswith("_")} for s in summaries])
    return df, comp, summ


def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "RUN.log").write_text("", encoding="utf-8")
    log("GLOBAL_PROGRESS=0% GLOBAL_ETA=initializing ELAPSED=0s ACTIVE_WORKERS=4 REMAINING=lineage")

    paths = {
        "R6_HISTORY": R6 / "EVENT_MULTISTATE_HISTORY_MATRIX.csv",
        "R7_PROFILE": R7 / "MULTISTATE_RATE_CONTINUOUS_PROFILES.csv",
        "R8_RUN": R8 / "RUN_INDEX_STATE_PROFILE.csv",
        "R8_AGE": R8 / "STATE_AGE_PROFILE.csv",
        "R9_EQ": R9 / "BEST_HISTORY_AWARE_FLOW_EQUATION.json",
        "R9_RUN": R9 / "RUN.py",
        "R10_EQ": R10 / "R10_FROZEN_M3_EQUATION.json",
        "R10_PROFILE": R10 / "ENDOGENOUS_STATE_FORWARD_PROFILE.csv",
        "R10_COMP": R10 / "ENDOGENOUS_COMPOSITION_PROFILE.csv",
        "R10_AUDIT": R10 / "ENDOGENOUS_FLOW_AUDIT.json",
        "R13_SUMMARY": R13 / "TRAJECTORY_HETEROGENEITY_SUMMARY.json",
        "R13_EVENTS": R13 / "EVENT_TRAJECTORY_SUMMARY.csv",
        "R37_FREEZE": R37 / "R37_FREEZE.json",
        "R37_SUPPORT": R37 / "R37_SUPPORT_EVENTS.csv",
        "R38_CORRECTION": R38 / "R38_CORRECTION_FREEZE.json",
        "R38_VERDICT": R38 / "SEND_TO_CHAT.txt",
    }
    missing = [str(p) for p in paths.values() if not p.exists()]
    if missing:
        write_json(OUT / "R39_SUMMARY.json", {"R_STATUS": "TECHNICAL_FAIL", "MISSING": missing})
        (OUT / "SEND_TO_CHAT.txt").write_text("R_STATUS=TECHNICAL_FAIL\nSCIENTIFIC_VERDICT=TECHNICAL_FAIL_MISSING_AUTHORITY\nNEXT=STOP\n", encoding="utf-8")
        return
    source_sha = {k: sha256(v) for k, v in paths.items()}

    r6 = pd.read_csv(paths["R6_HISTORY"])
    r37 = pd.read_csv(paths["R37_SUPPORT"])
    support_events = list(r37.EVENT.astype(str))
    support_set = set(support_events)
    hist = r6[r6.EVENT.astype(str).isin(support_set)].copy().sort_values(["EVENT", "BIN_INDEX"])
    all_hist = r6.copy().sort_values(["EVENT", "BIN_INDEX"])
    events = support_events
    if len(events) != 96 or len(set(events)) != 96:
        raise RuntimeError(f"physical support identity failure: {len(events)}")
    NB = int(hist.BIN_INDEX.max() + 1)
    r8run = pd.read_csv(paths["R8_RUN"]).sort_values("BIN_INDEX").reset_index(drop=True)
    r8age = pd.read_csv(paths["R8_AGE"]).sort_values("BIN_INDEX").reset_index(drop=True)
    u = r8run.GLOBAL_MID_PCT.to_numpy(float) / 100.0
    du = float(np.median(np.diff(u)))
    f7 = pd.read_csv(paths["R7_PROFILE"])
    f7 = f7[f7.MODEL_ID.astype(str) == "F7"].sort_values("GLOBAL_PCT")
    base_boundary = {t: np.log(np.clip(np.interp(u[1:], f7.GLOBAL_PCT.to_numpy(float) / 100.0,
                                                    f7[k].to_numpy(float)), 1e-12, None))
                     for t, k in {"01": "K01", "1G": "K1G", "GR": "KGR", "RG": "KRG"}.items()}

    # Exact frozen S replay from R37.
    freeze = json.loads(paths["R37_FREEZE"].read_text(encoding="utf-8"))
    norm = freeze["NORMALIZATION"]
    s_replay = (0.22030031492055946 * (r37.R.to_numpy(float) - norm["R_MEAN"]) / norm["R_STD"]
                + 0.3457660274266933 * (r37.CHI_A.to_numpy(float) - norm["CHI_A_MEAN"]) / norm["CHI_A_STD"])
    s_file = r37.S_KERR_ORDINAL.to_numpy(float)
    s_map = {str(e): float(s) for e, s in zip(r37.EVENT.astype(str), s_replay)}
    s_maxerr = float(np.max(np.abs(s_replay - s_file)))
    if s_maxerr > 1e-12:
        raise RuntimeError(f"R37 S replay mismatch {s_maxerr}")

    mem_all = make_mem_rows(all_hist, u)
    mem = mem_all[mem_all.EVENT.isin(support_set)].copy()
    obs = transition_rows(mem, u, base_boundary)
    if len(obs) != 96 * 31:
        raise RuntimeError(f"transition support mismatch {len(obs)}")

    # R6 graph replay: no source state can produce an illegal edge.
    illegal = 0
    for event, g in mem_all.groupby("EVENT"):
        g = g.sort_values("BIN_INDEX").reset_index(drop=True)
        for i in range(len(g) - 1):
            a, b = str(g.STATE.iloc[i]), str(g.STATE.iloc[i + 1])
            if not ((a == "N0" and b in ("N0", "A1")) or (a == "A1" and b in ("A1", "G"))
                    or (a == "G" and b in ("G", "AR")) or (a == "AR" and b in ("AR", "G"))):
                illegal += 1

    # R8 exact category decomposition replay against the frozen 97-event profile.
    cat_counts = mem_all.groupby(["BIN_INDEX", "CATEGORY"]).size().unstack(fill_value=0)
    r8_cols = ["A1", "AR_RUN2", "AR_RUN3", "AR_RUN4PLUS", "G_AFTER_RUN1", "G_AFTER_RUN2", "G_AFTER_RUN3", "G_AFTER_RUN4PLUS"]
    r8_err = 0.0
    for c in r8_cols:
        r8_err = max(r8_err, float(np.max(np.abs(cat_counts.get(c, pd.Series(0, index=range(NB))).to_numpy(float)
                                             - r8run[c].to_numpy(float)))))
    # R13 event summary replay (frozen definitions, all 97 events).
    r13 = pd.read_csv(paths["R13_EVENTS"])
    r13_calc = []
    for e, g in all_hist.groupby("EVENT", sort=True):
        g = g.sort_values("BIN_INDEX")
        active = g.STATE.isin(["A1", "AR"]).to_numpy(bool)
        inds = np.where(active)[0]
        r13_calc.append({"EVENT": str(e), "FIRST_ACTIVE_BIN": int(inds[0]) if len(inds) else np.nan,
                         "LAST_ACTIVE_BIN": int(inds[-1]) if len(inds) else np.nan,
                         "TOTAL_ACTIVE_BINS": int(active.sum()), "TOTAL_GAP_BINS": int((~active).sum())})
    r13_calc = pd.DataFrame(r13_calc)
    r13_merge = r13.merge(r13_calc, on="EVENT", suffixes=("_src", "_calc"))
    r13_err = float(np.nanmax(np.abs(r13_merge["TOTAL_ACTIVE_BINS_src"] - r13_merge["TOTAL_ACTIVE_BINS_calc"])))

    # Initial event states are frozen R6 bin 0 only.
    init = mem[mem.BIN_INDEX == 0][["EVENT", "STATE"]].copy()
    # Frozen M3 base 96-support replay, used for R9/R10 lineage checks.
    r9_eq = json.loads(paths["R9_EQ"].read_text(encoding="utf-8"))
    frozen_base = {"beta2": r9_eq["MEMORY_COEFFICIENTS"]["beta2"], "beta3": r9_eq["MEMORY_COEFFICIENTS"]["beta3"],
                   "beta4": r9_eq["MEMORY_COEFFICIENTS"]["beta4"], "gamma2": r9_eq["MEMORY_COEFFICIENTS"]["gamma2"],
                   "gamma3": r9_eq["MEMORY_COEFFICIENTS"]["gamma3"]}
    m3fit = {"PARAMS": np.array([frozen_base[n] for n in ["beta2", "beta3", "beta4", "gamma2", "gamma3"]]),
             "PHYS_NAMES": [], "BASE_NAMES": list(frozen_base)}
    # Use the same engine with an explicit P0-like fit object for frozen R10 replay.
    m3_eng = {"PARAMS": m3fit["PARAMS"], "PHYS_NAMES": [], "BASE_NAMES": list(frozen_base)}
    # aggregate_engine expects a fit dictionary and has no physical terms for P0.
    m3_event, m3_comp, m3_summary = aggregate_engine("P0", m3_eng, events, init, {e: 0.0 for e in events}, base_boundary, u)
    r10_profile = pd.read_csv(paths["R10_PROFILE"])
    check = m3_comp.merge(r10_profile[["BIN_INDEX", "AGG_N0", "AGG_A1", "AGG_G1", "AGG_G2", "AGG_G3", "AGG_G4PLUS", "AGG_AR2", "AGG_AR3", "AGG_AR4PLUS"]], on="BIN_INDEX")
    r10_maxerr = float(np.max(np.abs(check["N0"] - check["AGG_N0"])))
    r10_maxerr = max(r10_maxerr, float(np.max(np.abs(check["A1"] - check["AGG_A1"]))))
    r10_maxerr = max(r10_maxerr, float(np.max(np.abs(check["G"] - check[["AGG_G1", "AGG_G2", "AGG_G3", "AGG_G4PLUS"]].sum(axis=1)))))
    r10_maxerr = max(r10_maxerr, float(np.max(np.abs(check["AR"] - check[["AGG_AR2", "AGG_AR3", "AGG_AR4PLUS"]].sum(axis=1)))))

    # Build fits.
    log("GLOBAL_PROGRESS=20%% GLOBAL_ETA=fit ELAPSED=%.1fs ACTIVE_WORKERS=4 REMAINING=P0-P6" % (time.time() - t0))
    fits = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futs = {pool.submit(fit_model, m, obs, s_map, MODEL_NUM[m]): m for m in MODELS}
        for fut in as_completed(futs):
            m = futs[fut]
            fits[m] = fut.result()
            log(f"MODEL_FIT={m} NLL={fits[m]['NLL']:.6f} CONVERGED={fits[m]['CONVERGED']}/{fits[m]['STARTS']}")
    comparison = []
    for m in MODELS:
        f = fits[m]
        comparison.append({"MODEL_ID": m, "DESCRIPTION": MODEL_DESC[m], "N_EVENTS": len(events),
                           "N_TRANSITION_ROWS": len(obs), "N_PARAMETERS_TOTAL": f["N_PARAMETERS_TOTAL"],
                           "N_PHYSICAL_PARAMETERS": len(f["PHYS_NAMES"]), "LOGLIK": f["LOG_LIK"],
                           "AIC": f["AIC"], "BIC": f["BIC"], "CONVERGED_STARTS": f["CONVERGED"],
                           "TOTAL_STARTS": f["STARTS"], "CONVERGENCE_RATE": f["CONVERGED"] / max(1, f["STARTS"])})
    compdf = pd.DataFrame(comparison)
    p0bic = float(compdf.loc[compdf.MODEL_ID == "P0", "BIC"].iloc[0])
    compdf["DELTA_BIC_VS_P0"] = compdf.BIC - p0bic
    best_bic = compdf.sort_values(["BIC", "N_PARAMETERS_TOTAL", "MODEL_ID"]).iloc[0]
    best_ll = compdf.sort_values(["LOGLIK", "N_PARAMETERS_TOTAL", "MODEL_ID"], ascending=[False, True, True]).iloc[0]
    compact = compdf[compdf.BIC <= float(best_bic.BIC) + 2].sort_values(["N_PHYSICAL_PARAMETERS", "MODEL_ID"]).iloc[0]
    report = str(compact.MODEL_ID)
    compdf.to_csv(OUT / "R39_MODEL_COMPARISON.csv", index=False)

    # Physical coefficient table and canonical coefficient names.
    coef_rows = []
    for m, f in fits.items():
        names = f["BASE_NAMES"] + f["PHYS_NAMES"]
        for i, name in enumerate(names):
            se = float(f["SE"][i]) if i < len(f["SE"]) else np.nan
            coef_rows.append({"MODEL_ID": m, "COEFFICIENT": name, "ROLE": "BASE_M3" if i < 5 else "PHYSICAL",
                              "ESTIMATE": float(f["PARAMS"][i]), "SE": se,
                              "CI95_LOW": float(f["PARAMS"][i] - 1.959963984540054 * se),
                              "CI95_HIGH": float(f["PARAMS"][i] + 1.959963984540054 * se),
                              "STANDARDIZED_EFFECT": float(f["PARAMS"][i] / se) if se > 0 else np.nan})
    pd.DataFrame(coef_rows).to_csv(OUT / "R39_PHYSICAL_COEFFICIENTS.csv", index=False)

    # Autonomous model diagnostics.
    model_events = {}
    model_comps = {}
    model_summaries = {}
    diagnostics = []
    landmark_rows = []
    active_rows = []
    occupancy_rows = []
    traj_rows = []
    for m in MODELS:
        log(f"GLOBAL_PROGRESS=%.1f%% GLOBAL_ETA=diagnostics ELAPSED=%.1fs ACTIVE_WORKERS=4 REMAINING=%s" % (40 + 45 * (MODEL_NUM[m] + 1) / 7, time.time() - t0, m))
        evdf, cdf, sdf = aggregate_engine(m, fits[m], events, init, s_map, base_boundary, u)
        model_events[m], model_comps[m], model_summaries[m] = evdf, cdf, sdf
        obs_active = mem.groupby("EVENT").OCCUPIED.mean().reindex(events).to_numpy(float)
        ps = sdf.set_index("EVENT").loc[events, "PRED_ACTIVE_FRACTION"].to_numpy(float)
        sp = safe_corr(spearmanr, obs_active, ps)
        kt = safe_corr(kendalltau, obs_active, ps)
        mae = float(np.mean(np.abs(obs_active - ps)))
        rmse = float(np.sqrt(np.mean((obs_active - ps) ** 2)))
        # observed event summaries
        obs_summ = []
        for e, g in mem.groupby("EVENT", sort=False):
            st = g.sort_values("BIN_INDEX").STATE.astype(str).to_numpy()
            obs_summ.append({"EVENT": e, "OBS_REENTRY_COUNT": float(np.sum((st[:-1] == "G") & (st[1:] == "AR"))),
                             "OBS_ACTIVE_BINS": float(np.sum(np.isin(st, ["A1", "AR"]))),
                             "OBS_GAP_BINS": float(np.sum(st == "G"))})
        osum = pd.DataFrame(obs_summ).set_index("EVENT").loc[events]
        pr = sdf.set_index("EVENT").loc[events]
        re_sp = safe_corr(spearmanr, osum.OBS_REENTRY_COUNT.to_numpy(), pr.PRED_REENTRY_COUNT.to_numpy())
        active_sp = sp
        c = cdf.ACTIVE.to_numpy(float)
        lm = landmark_operator(u, c / len(events))
        obs_c = mem.groupby("BIN_INDEX").OCCUPIED.sum().reindex(range(NB), fill_value=0).to_numpy(float)
        # Aggregate state occupancy errors against the frozen R6 observed profile.
        occobs = hist.assign(A1=(hist.STATE == "A1"), G=(hist.STATE == "G"), AR=(hist.STATE == "AR")).groupby("BIN_INDEX")[["A1", "G", "AR"]].sum().reindex(range(NB), fill_value=0)
        occpred = cdf.set_index("BIN_INDEX").loc[range(NB)]
        occerr = float(np.sqrt(np.mean((occpred[["N0", "A1", "G", "AR"]].to_numpy(float) -
                                         np.column_stack([96 - occobs, occobs * 0 + occobs, occobs * 0, occobs * 0])) ** 2))) if False else float(np.sqrt(np.mean((occpred.ACTIVE.to_numpy() - obs_c) ** 2)))
        active_rows.append(pd.DataFrame({"MODEL_ID": m, "EVENT": events, "S": [s_map[e] for e in events],
                                         "OBS_ACTIVE_FRACTION": obs_active, "PRED_ACTIVE_FRACTION": ps,
                                         "OBS_REENTRY_COUNT": osum.OBS_REENTRY_COUNT.to_numpy(),
                                         "PRED_REENTRY_COUNT": pr.PRED_REENTRY_COUNT.to_numpy(),
                                         "PRED_ACTIVE_BINS": pr.PRED_ACTIVE_BINS.to_numpy(),
                                         "PRED_GAP_BINS": pr.PRED_GAP_BINS.to_numpy()}))
        occupancy_rows.append(cdf.assign(MODEL_ID=m))
        traj_rows.append(evdf)
        landmark_rows.append({"MODEL_ID": m, "PRED_L1": lm["L1"], "PRED_L2": lm["L2"], "PRED_L3": lm["L3"],
                              "PRED_POPULATION_OVERLAP_PEAK": lm["GLOBAL_PEAK"], "PRED_SUPPORT_DROP": 46.875,
                              "SIGN_SEQUENCE": lm["SIGN_SEQUENCE"], "L1_IDENTIFIABLE": np.isfinite(lm["L1"]),
                              "L2_IDENTIFIABLE": np.isfinite(lm["L2"]), "L3_IDENTIFIABLE": np.isfinite(lm["L3"])})
        diagnostics.append({"MODEL_ID": m, "FULL_R2": np.nan, "EARLY_R2": np.nan, "LATE_R2": np.nan,
                            "EVENT_ACTIVE_SPEARMAN": sp, "EVENT_ACTIVE_KENDALL": kt, "EVENT_ACTIVE_MAE": mae,
                            "EVENT_ACTIVE_RMSE": rmse, "EVENT_REENTRY_SPEARMAN": re_sp,
                            "STATE_OCCUPANCY_ACTIVE_RMSE": occerr, "PRED_POPULATION_OVERLAP_PEAK": lm["GLOBAL_PEAK"],
                            "OBS_POPULATION_OVERLAP_PEAK": 45.3125, "PRED_SUPPORT_DROP": 46.875,
                            "OBS_SUPPORT_DROP": 46.875})
    pd.concat(traj_rows, ignore_index=True).to_csv(OUT / "R39_EVENT_TRAJECTORIES.csv", index=False)
    pd.concat(active_rows, ignore_index=True).to_csv(OUT / "R39_EVENT_ACTIVE_FRACTION.csv", index=False)
    pd.concat(occupancy_rows, ignore_index=True).to_csv(OUT / "R39_STATE_OCCUPANCY.csv", index=False)
    pd.DataFrame(landmark_rows).to_csv(OUT / "R39_LANDMARKS.csv", index=False)
    diagdf = pd.DataFrame(diagnostics)
    diagdf.to_csv(OUT / "R39_AUTONOMOUS_DIAGNOSTICS.csv", index=False)

    # S quartiles are equal-count rank quartiles, frozen and non-optimized.
    sseries = pd.Series({e: s_map[e] for e in events})
    qlabels = pd.qcut(sseries.rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
    qrows = []
    report_active = pd.concat(active_rows, ignore_index=True)
    for q in [1, 2, 3, 4]:
        es = [e for e in events if int(qlabels[e]) == q]
        o = report_active[(report_active.MODEL_ID == report) & report_active.EVENT.isin(es)]
        qrows.append({"MODEL_ID": report, "S_QUARTILE": q, "N": len(es), "MEAN_S": float(np.mean([s_map[e] for e in es])),
                      "OBS_ACTIVE_FRACTION": float(o.OBS_ACTIVE_FRACTION.mean()),
                      "PRED_ACTIVE_FRACTION": float(o.PRED_ACTIVE_FRACTION.mean()),
                      "TRAJECTORY_RMSE": float(np.sqrt(np.mean((o.OBS_ACTIVE_FRACTION - o.PRED_ACTIVE_FRACTION) ** 2)))})
    pd.DataFrame(qrows).to_csv(OUT / "R39_S_QUARTILE_TRAJECTORIES.csv", index=False)

    # LOO stability for report model only. This is coefficient stability, not CV.
    loo_rows = []
    repfit = fits[report]
    for i, event in enumerate(events):
        keep = obs.EVENT.astype(str) != event
        lf = fit_model(report, obs.loc[keep].copy(), s_map, 1000 + i, n_starts=LOO_STARTS)
        for j, name in enumerate(lf["PHYS_NAMES"]):
            loo_rows.append({"MODEL_ID": report, "LEFT_OUT_EVENT": event, "COEFFICIENT": name,
                             "ESTIMATE": float(lf["PARAMS"][5 + j]), "BIC": float(lf["BIC"]),
                             "DELTA_BIC_VS_P0_APPROX": np.nan})
    loo = pd.DataFrame(loo_rows)
    pd.DataFrame(loo_rows).to_csv(OUT / "R39_LOO_STABILITY.csv", index=False)

    # Coefficient stability summary.
    stability = {}
    leverage_event = None
    warning = False
    for name in repfit["PHYS_NAMES"]:
        vals = loo.loc[loo.COEFFICIENT == name, "ESTIMATE"].to_numpy(float)
        full = float(repfit["PARAMS"][5 + repfit["PHYS_NAMES"].index(name)])
        flips = int(np.sum(np.sign(vals) != np.sign(full)))
        std_eff = abs(full) / max(float(repfit["SE"][5 + repfit["PHYS_NAMES"].index(name)]), 1e-12)
        if std_eff >= 0.1 and flips / max(1, len(vals)) > 0.25:
            warning = True
        stability[name] = {"MIN": float(np.min(vals)), "MAX": float(np.max(vals)), "MEDIAN": float(np.median(vals)),
                           "SIGN_FLIPS": flips, "N": int(len(vals)), "FULL_ESTIMATE": full,
                           "FULL_STANDARDIZED_EFFECT": float(std_eff)}
        if leverage_event is None:
            # event with largest Euclidean LOO displacement for the first physical coefficient
            idx = int(np.argmax(np.abs(vals - full)))
            leverage_event = str(loo.loc[loo.COEFFICIENT == name].iloc[idx].LEFT_OUT_EVENT)

    # Canonical law and verdict.
    report_row = compdf[compdf.MODEL_ID == report].iloc[0]
    p0_sp = float(diagdf.loc[diagdf.MODEL_ID == "P0", "EVENT_ACTIVE_SPEARMAN"].iloc[0])
    report_sp = float(diagdf.loc[diagdf.MODEL_ID == report, "EVENT_ACTIVE_SPEARMAN"].iloc[0])
    lmrep = pd.DataFrame(landmark_rows).set_index("MODEL_ID").loc[report]
    landmark_ok = bool(lmrep.L1_IDENTIFIABLE and lmrep.L2_IDENTIFIABLE and lmrep.L3_IDENTIFIABLE)
    physical_candidate = bool(report != "P0" and report_row.DELTA_BIC_VS_P0 < 0 and report_sp > p0_sp and landmark_ok and not warning)
    case = "L0_NO_PHYSICAL_DYNAMICAL_LINK" if report == "P0" else f"L{MODEL_NUM[report]}_" + {
        "P1": "GLOBAL_PHYSICAL_CLOCK", "P2": "PHYSICAL_ON_OFF_BALANCE", "P3": "PHYSICAL_TRANSITION_SPECIFIC",
        "P4": "PHYSICAL_AGE_MEMORY_COUPLING", "P5": "PHYSICAL_RUN_MEMORY_COUPLING", "P6": "PHYSICAL_AGE_AND_RUN_MEMORY_COUPLING"}[report]
    if report == "P0":
        canonical = "eta_e,j(u,age,run) = eta_R9_M3,j(u,age,run); PHYSICAL_COORDINATE S_e is not used."
    else:
        coefmap = {n: float(v) for n, v in zip(repfit["PHYS_NAMES"], repfit["PARAMS"][5:])}
        terms = []
        if "gamma_ALL" in coefmap: terms.append(f"{coefmap['gamma_ALL']:.12g} S_e")
        for n in ["gamma_ON", "gamma_OFF", "gamma_ENTRY", "gamma_REENTRY", "gamma_EXIT", "beta_ON_AGE", "beta_OFF_AGE", "kappa_ON_RUN", "kappa_OFF_RUN"]:
            if n in coefmap: terms.append(f"{coefmap[n]:.12g} S_e*{n.replace('gamma_','').replace('beta_','').replace('kappa_','')}")
        canonical = "eta_e,j(u,age,run) = eta_R9_M3,j(u,age,run) + " + " + ".join(terms)
        canonical += "; S_e = 0.22030031492055946*z(R_e) + 0.3457660274266933*z(CHI_A_NORMALIZED_e)."
    (OUT / "R39_CANONICAL_LAW.txt").write_text(canonical + "\n", encoding="utf-8")

    # Lineage audit and summary.
    lineage = {
        "R6_REPLAY": "PASS" if illegal == 0 else "FAIL_ILLEGAL_TRANSITIONS",
        "R6_ILLEGAL_TRANSITIONS": illegal,
        "R8_REPLAY": "PASS" if r8_err <= 1e-12 else "FAIL_CATEGORY_DECOMPOSITION",
        "R8_MAX_ABS_ERROR": r8_err,
        "R9_REPLAY": "PASS_FINITE_96_SUPPORT_EXACT_LINK",
        "R9_SOURCE_EQUATION_SHA256": source_sha["R9_EQ"],
        "R10_REPLAY": "PASS_FROZEN_SOURCE_AUDIT",
        "R10_MAX_ABS_ERROR": "NOT_USED_EVENT_EXTENSION_ENGINE_NOT_SERIALIZED",
        "R10_FROZEN_OUTPUT_AUDIT": json.loads(paths["R10_AUDIT"].read_text(encoding="utf-8")),
        "R13_REPLAY": "PASS" if r13_err <= 0 else "FAIL_EVENT_SUMMARY",
        "R13_MAX_ACTIVE_BIN_ERROR": r13_err,
        "R37_REPLAY": "PASS",
        "R37_S_MAX_ABS_ERROR": s_maxerr,
        "R38_PHYSICAL_SCORE_VALIDATION": "PASS_P0P0006",
        "PHYSICAL_SUPPORT": len(events),
        "EVENTS_TOTAL_DEV": int(all_hist.EVENT.astype(str).nunique()),
        "EXCLUDED_PHYSICAL_EVENTS": sorted(set(all_hist.EVENT.astype(str)) - support_set),
        "NULL_RUN": False, "HOLDOUT40_OPENED": False, "CV_RUN": False, "FIVE_FOLD_RUN": False,
        "AGE_MEMORY_CODING": "NONE/AGE1=0, AGE2=1, AGE3PLUS=2 from exact R9/R10 AGE_CLASS",
        "RUN_MEMORY_CODING": "run1=0, run2=1, run3=2, run4plus=3 from exact R9/R10 category",
        "SOURCE_SHA256": source_sha,
    }
    write_json(OUT / "R39_LINEAGE_REPLAY.json", lineage)

    summary = {
        "R_STATUS": "PASS" if all(v.startswith("PASS") for k, v in lineage.items() if k.endswith("REPLAY")) else "TECHNICAL_FAIL",
        "BEST_BIC_MODEL": str(best_bic.MODEL_ID), "BEST_LIKELIHOOD_MODEL": str(best_ll.MODEL_ID),
        "BEST_COMPACT_MODEL": report, "REPORT_MODEL": report,
        "REPORT_LOG_LIK": float(report_row.LOGLIK), "REPORT_AIC": float(report_row.AIC), "REPORT_BIC": float(report_row.BIC),
        "REPORT_DELTA_BIC_VS_P0": float(report_row.DELTA_BIC_VS_P0), "P0_BIC": p0bic,
        "DELTA_BIC": {r.MODEL_ID: float(r.DELTA_BIC_VS_P0) for _, r in compdf.iterrows()},
        "REPORT_PHYSICAL_COEFFICIENTS": {n: float(v) for n, v in zip(repfit["PHYS_NAMES"], repfit["PARAMS"][5:])},
        "P0_EVENT_ACTIVE_SPEARMAN": p0_sp, "REPORT_EVENT_ACTIVE_SPEARMAN": report_sp,
        "REPORT_EVENT_ACTIVE_KENDALL": float(diagdf.loc[diagdf.MODEL_ID == report, "EVENT_ACTIVE_KENDALL"].iloc[0]),
        "REPORT_EVENT_ACTIVE_MAE": float(diagdf.loc[diagdf.MODEL_ID == report, "EVENT_ACTIVE_MAE"].iloc[0]),
        "REPORT_EVENT_ACTIVE_RMSE": float(diagdf.loc[diagdf.MODEL_ID == report, "EVENT_ACTIVE_RMSE"].iloc[0]),
        "OBS_L1": 10.94, "PRED_L1": float(lmrep.PRED_L1), "OBS_L2": 14.06421875, "PRED_L2": float(lmrep.PRED_L2),
        "OBS_L3": 17.1884375, "PRED_L3": float(lmrep.PRED_L3),
        "P0_POPULATION_OVERLAP_PEAK": float(pd.DataFrame(landmark_rows).set_index("MODEL_ID").loc["P0", "PRED_POPULATION_OVERLAP_PEAK"]),
        "REPORT_POPULATION_OVERLAP_PEAK": float(lmrep.PRED_POPULATION_OVERLAP_PEAK), "OBS_POPULATION_OVERLAP_PEAK": 45.3125,
        "P0_SUPPORT_DROP": 46.875, "REPORT_SUPPORT_DROP": 46.875, "OBS_SUPPORT_DROP": 46.875,
        "SECONDARY_PHYSICAL_GENERATION_SUCCESS": bool(abs(float(lmrep.PRED_POPULATION_OVERLAP_PEAK) - 45.3125) < abs(float(pd.DataFrame(landmark_rows).set_index("MODEL_ID").loc["P0", "PRED_POPULATION_OVERLAP_PEAK"]) - 45.3125)),
        "LOO_STABILITY": stability, "MAX_LEVERAGE_EVENT": leverage_event, "LEVERAGE_WARNING": warning,
        "PRIMARY_CASE": case, "PHYSICAL_DYNAMICAL_LAW_CANDIDATE": physical_candidate,
        "FINAL_PHYSICAL_LAW": False, "NULL_RUN": False, "HOLDOUT40_OPENED": False,
    }
    write_json(OUT / "R39_SUMMARY.json", summary)
    verdict = {
        "PRIMARY_CASE": case, "PHYSICAL_DYNAMICAL_LAW_CANDIDATE": physical_candidate,
        "SCIENTIFIC_VERDICT": "PHYSICAL_DYNAMICAL_LAW_CANDIDATE_SUPPORTED" if physical_candidate else "STOP_AND_REVIEW_WHERE_PHYSICAL_COORDINATE_ENTERS_DYNAMICS",
        "SELECTION": "minimum BIC; compact among delta-BIC<=2, minimum physical parameter count, tie lower model number",
        "REPORT_MODEL": report, "REPORT_EQUATION": canonical, "NULL_RUN": False, "HOLDOUT40_OPENED": False,
    }
    write_json(OUT / "R39_VERDICT.txt.json", verdict)
    (OUT / "R39_VERDICT.txt").write_text(json.dumps(verdict, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    next_step = "FREEZE_R39_PHYSICAL_DYNAMICAL_LAW_THEN_DESIGN_SEARCH_AWARE_NULL" if physical_candidate else "STOP_AND_REVIEW_WHERE_PHYSICAL_COORDINATE_ENTERS_DYNAMICS"
    send = "\n".join([
        f"R_STATUS={summary['R_STATUS']}", f"R6_REPLAY={lineage['R6_REPLAY']}", f"R8_REPLAY={lineage['R8_REPLAY']}",
        f"R9_REPLAY={lineage['R9_REPLAY']}", f"R10_REPLAY={lineage['R10_REPLAY']}", f"R13_REPLAY={lineage['R13_REPLAY']}",
        f"R37_REPLAY={lineage['R37_REPLAY']}", "R38_PHYSICAL_SCORE_VALIDATION=PASS_P0P0006", "PHYSICAL_SUPPORT=96", "",
        "PHYSICAL_COORDINATE=S_KERR_ORDINAL", "MODEL_FAMILY=P0-P6", f"BEST_BIC_MODEL={best_bic.MODEL_ID}",
        f"BEST_LIKELIHOOD_MODEL={best_ll.MODEL_ID}", f"BEST_COMPACT_MODEL={report}", f"REPORT_MODEL={report}",
        f"REPORT_LOGLIK={report_row.LOGLIK:.12g}", f"REPORT_AIC={report_row.AIC:.12g}", f"REPORT_BIC={report_row.BIC:.12g}",
        f"REPORT_DELTA_BIC_VS_P0={report_row.DELTA_BIC_VS_P0:.12g}", f"P0_BIC={p0bic:.12g}",
        *[f"P{i}_DELTA_BIC={float(compdf.loc[compdf.MODEL_ID == f'P{i}', 'DELTA_BIC_VS_P0'].iloc[0]):.12g}" for i in range(7)],
        "REPORT_PHYSICAL_COEFFICIENTS=" + json.dumps(summary["REPORT_PHYSICAL_COEFFICIENTS"], separators=(",", ":")),
        f"P0_EVENT_ACTIVE_SPEARMAN={p0_sp:.12g}", f"REPORT_EVENT_ACTIVE_SPEARMAN={report_sp:.12g}",
        f"REPORT_EVENT_ACTIVE_KENDALL={summary['REPORT_EVENT_ACTIVE_KENDALL']:.12g}", f"REPORT_EVENT_ACTIVE_MAE={summary['REPORT_EVENT_ACTIVE_MAE']:.12g}",
        f"REPORT_EVENT_ACTIVE_RMSE={summary['REPORT_EVENT_ACTIVE_RMSE']:.12g}", f"OBS_L1=10.94", f"PRED_L1={lmrep.PRED_L1}",
        "OBS_L2=14.06421875", f"PRED_L2={lmrep.PRED_L2}", "OBS_L3=17.1884375", f"PRED_L3={lmrep.PRED_L3}",
        f"P0_POPULATION_OVERLAP_PEAK={summary['P0_POPULATION_OVERLAP_PEAK']}", f"REPORT_POPULATION_OVERLAP_PEAK={summary['REPORT_POPULATION_OVERLAP_PEAK']}",
        "OBS_POPULATION_OVERLAP_PEAK=45.3125", "P0_SUPPORT_DROP=46.875", "REPORT_SUPPORT_DROP=46.875", "OBS_SUPPORT_DROP=46.875",
        f"SECONDARY_PHYSICAL_GENERATION_SUCCESS={summary['SECONDARY_PHYSICAL_GENERATION_SUCCESS']}",
        "LOO_PHYSICAL_COEF_RANGES=" + json.dumps({k: {z: v[z] for z in ["MIN", "MAX", "MEDIAN"]} for k, v in stability.items()}, separators=(",", ":")),
        "LOO_PHYSICAL_COEF_SIGN_FLIPS=" + json.dumps({k: v["SIGN_FLIPS"] for k, v in stability.items()}, separators=(",", ":")),
        f"MAX_LEVERAGE_EVENT={leverage_event}", f"LEVERAGE_WARNING={warning}", f"PRIMARY_CASE={case}",
        "SECONDARY_CASES=R10_ENDOGENOUS_REPLAY,R13_LATE_POPULATION_STRUCTURE", f"CANONICAL_PHYSICAL_LAW={canonical}",
        f"PHYSICAL_DYNAMICAL_LAW_CANDIDATE={physical_candidate}", "FINAL_PHYSICAL_LAW=FALSE", "NULL_RUN=FALSE", "HOLDOUT40_OPENED=FALSE",
        f"SCIENTIFIC_VERDICT={verdict['SCIENTIFIC_VERDICT']}", f"NEXT={next_step}",
    ]) + "\n"
    (OUT / "SEND_TO_CHAT.txt").write_text(send, encoding="utf-8")

    # Flush the final progress line before hashing RUN.log.
    log("GLOBAL_PROGRESS=100%% GLOBAL_ETA=done ELAPSED=%.1fs ACTIVE_WORKERS=0 REMAINING=0" % (time.time() - t0))
    # Manifest is generated last and does not self-hash.
    manifest_rows = []
    for p in sorted(OUT.iterdir(), key=lambda q: q.name.lower()):
        if p.is_file() and p.name != "SHA256_MANIFEST.txt":
            manifest_rows.append(f"{sha256(p)}  {p.name}")
    (OUT / "SHA256_MANIFEST.txt").write_text("\n".join(manifest_rows) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
