import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr


ROOT = Path(r"E:\RIUD_ACTIVE_20260808")
OUT = ROOT / "RIUD_FREQUENCY_FAMILY_K1_K2_K5_ABC_GEOMETRY_CROSS_AUDIT_R0_20260826"

ABC = ROOT / "RIUD_ABC_INTEGRATED_MAP_LAW_LEDGER_R0_20260825" / "ABC_96_EVENT_INTEGRATED_LEDGER.csv"
FREQ = ROOT / "RIUD_DEV99_FREQUENCY_MAG_SHAPE_CENSUS_R0_20260824" / "07_FREQ_MAG_SHAPE_ASSIGNMENTS.csv"
GEOM = ROOT / "RIUD_DEV99_DYNAMICS_REPRESENTATION_FREEZE_R10J0R2_PCA90_FIX_PAR16_20260811" / "01_FREEZE" / "R10J0R2_EVENT_DYNAMICS_FEATURES.csv"
R40 = ROOT / "RIUD_DEV99_PHYSICAL_DYNAMICAL_LAW_FREEZE_R40_20260815" / "R40_SUPPORT_EVENTS.csv"
R39 = ROOT / "RIUD_DEV99_PHYSICAL_DYNAMICAL_LAW_DISCOVERY_R39_20260815" / "R39_EVENT_ACTIVE_FRACTION.csv"
K2 = ROOT / "RIUD_PIV_SXS_GR_RELEASE_R1_20260826" / "SXS_GR" / "RIUD_EARLYMAXFLOW16_MATCHED_PURE_GR_FULL_SYSTEM_TEST_R0_20260824" / "06_INDEPENDENT_PHYSICAL_AXIS" / "OBS16_S_EVENT_SCORES.csv"
K2T = ROOT / "RIUD_PIV_SXS_GR_RELEASE_R1_20260826" / "SXS_GR" / "RIUD_EARLYMAXFLOW16_MATCHED_PURE_GR_FULL_SYSTEM_TEST_R0_20260824" / "06_INDEPENDENT_PHYSICAL_AXIS" / "OBS16_DYNAMIC_TARGETS.csv"
K1 = ROOT / "RIUD_PIV_SXS_GR_RELEASE_R1_20260826" / "SXS_GR" / "RIUD_EARLYMAXFLOW16_MATCHED_PURE_GR_FULL_SYSTEM_TEST_R0_20260824" / "06_INDEPENDENT_PHYSICAL_AXIS" / "GR16_S_EVENT_SCORES.csv"
K1T = ROOT / "RIUD_PIV_SXS_GR_RELEASE_R1_20260826" / "SXS_GR" / "RIUD_EARLYMAXFLOW16_MATCHED_PURE_GR_FULL_SYSTEM_TEST_R0_20260824" / "06_INDEPENDENT_PHYSICAL_AXIS" / "GR16_DYNAMIC_TARGETS.csv"
AONLY = ROOT / "RIUD_A_ONLY_TRUE_PHYSICAL_S_DISCOVERY_RATE_REBUILD_R0_20260824" / "A_ONLY_S_A_EVENT_VALUES.csv"
COMMON_PHYS = ROOT / "RIUD_PIV_SXS_GR_RELEASE_R1_20260826" / "SXS_GR" / "RIUD_EARLYMAXFLOW16_MATCHED_PURE_GR_FULL_SYSTEM_TEST_R0_20260824" / "06_INDEPENDENT_PHYSICAL_AXIS" / "COMMON_PHYSICAL_CANDIDATE_TABLE.csv"


def sha(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def numeric(s):
    return pd.to_numeric(s, errors="coerce")


def corr(x, y):
    z = pd.DataFrame({"x": numeric(x), "y": numeric(y)}).dropna()
    if len(z) < 3 or z.x.nunique() < 2 or z.y.nunique() < 2:
        return {"n": int(len(z)), "pearson_r": np.nan, "pearson_p": np.nan, "spearman_rho": np.nan, "spearman_p": np.nan}
    pr, pp = pearsonr(z.x, z.y)
    sr, sp = spearmanr(z.x, z.y)
    return {"n": int(len(z)), "pearson_r": float(pr), "pearson_p": float(pp), "spearman_rho": float(sr), "spearman_p": float(sp)}


def zscore(s):
    x = numeric(s).astype(float)
    sd = x.std(ddof=0)
    return (x - x.mean()) / sd if sd > 0 and np.isfinite(sd) else pd.Series(np.zeros(len(x)), index=x.index)


def design_categorical(df, col):
    if col not in df:
        return pd.DataFrame(index=df.index)
    d = pd.get_dummies(df[col].fillna("MISSING").astype(str), prefix=col, drop_first=True, dtype=float)
    return d


def ols_metrics(y, X):
    y = numeric(y).astype(float)
    X = X.astype(float)
    keep = np.isfinite(y.to_numpy()) & np.isfinite(X.to_numpy()).all(axis=1)
    y = y.loc[keep]
    X = X.loc[keep]
    n = len(y)
    p = X.shape[1]
    if n <= p or n < 4:
        return {"n": n, "p": p, "df_resid": n - p, "r2": np.nan, "adj_r2": np.nan, "rmse": np.nan, "bic": np.nan, "aic": np.nan}
    A = np.column_stack([np.ones(n), X.to_numpy()])
    p_total = A.shape[1]
    beta, *_ = np.linalg.lstsq(A, y.to_numpy(), rcond=None)
    pred = A @ beta
    resid = y.to_numpy() - pred
    sse = float(np.dot(resid, resid))
    sst = float(np.dot(y.to_numpy() - y.mean(), y.to_numpy() - y.mean()))
    r2 = 1.0 - sse / sst if sst > 0 else np.nan
    df_resid = n - p_total
    sigma2 = sse / df_resid
    bic = n * math.log(max(sse / n, 1e-300)) + p_total * math.log(n)
    aic = n * math.log(max(sse / n, 1e-300)) + 2 * p_total
    adj = 1.0 - (1.0 - r2) * (n - 1) / df_resid if np.isfinite(r2) else np.nan
    return {"n": n, "p": p_total, "df_resid": df_resid, "r2": r2, "adj_r2": adj, "rmse": math.sqrt(sse / n), "bic": bic, "aic": aic}


def group_stats(df, axis_name, axis_col, group_col, score_col, target_col=None):
    rows = []
    for group, g in df.groupby(group_col, dropna=False):
        score = numeric(g[score_col]).dropna()
        row = {"AXIS": axis_name, "GROUP_FIELD": group_col, "GROUP": group, "N": int(len(score)), "SCORE_MEAN": score.mean(), "SCORE_MEDIAN": score.median(), "SCORE_STD": score.std(ddof=1)}
        if target_col and target_col in g:
            t = numeric(g[target_col]).dropna()
            row.update({"TARGET_MEAN": t.mean(), "TARGET_MEDIAN": t.median(), "TARGET_STD": t.std(ddof=1)})
        rows.append(row)
    return rows


def load_inputs():
    abc = pd.read_csv(ABC).rename(columns={"EVENT_ID": "EVENT"})
    freq = pd.read_csv(FREQ)
    geom = pd.read_csv(GEOM).rename(columns={"event": "EVENT"})
    r40 = pd.read_csv(R40).rename(columns={"EVENT": "EVENT"})
    r39 = pd.read_csv(R39)
    r39p1 = r39[r39.MODEL_ID.eq("P1")].copy().rename(columns={"EVENT": "EVENT"})
    # R40 and R39 P1 are retained side-by-side to verify that the frozen K5 value is identical.
    k5 = r40[["EVENT", "S_KERR_ORDINAL", "R", "CHI_A", "z_R", "z_CHI_A"]].merge(r39p1[["EVENT", "S", "OBS_ACTIVE_FRACTION", "OBS_REENTRY_COUNT"]], on="EVENT", how="outer")
    k5["K5_SCORE"] = numeric(k5["S_KERR_ORDINAL"])
    k5["K5_R39_S"] = numeric(k5["S"])
    k5["K5_SCORE_DIFF_R40_MINUS_R39"] = k5.K5_SCORE - k5.K5_R39_S
    k2 = pd.read_csv(K2)[["EVENT_ID", "S_BRANCH", "TARGET_BRANCH"]].rename(columns={"EVENT_ID": "EVENT", "S_BRANCH": "K2_SCORE", "TARGET_BRANCH": "K2_TARGET_BRANCH"})
    k1 = pd.read_csv(K1)[["EVENT_ID", "S_BRANCH", "TARGET_BRANCH"]].rename(columns={"EVENT_ID": "EVENT", "S_BRANCH": "K1_SCORE", "TARGET_BRANCH": "K1_TARGET_BRANCH"})
    k2t = pd.read_csv(K2T)
    k1t = pd.read_csv(K1T)
    dyn = ["ACTIVE_FRACTION", "REENTRY_FRACTION", "TRANSITION_DENSITY", "GAIN_FRACTION", "LOSS_FRACTION"]
    for d in (k2t, k1t):
        d["DYNAMIC_TARGET_RAW"] = d[dyn].apply(numeric, axis=0).mean(axis=1)
        d["DYNAMIC_TARGET_ZMEAN"] = d[dyn].apply(lambda c: (numeric(c) - numeric(c).mean()) / numeric(c).std(ddof=0), axis=0).mean(axis=1)
    k2 = k2.merge(k2t[["EVENT_ID", "DYNAMIC_TARGET_RAW", "DYNAMIC_TARGET_ZMEAN", "ACTIVE_FRACTION", "REENTRY_FRACTION", "TRANSITION_DENSITY", "GAIN_FRACTION", "LOSS_FRACTION"]].rename(columns={"EVENT_ID": "EVENT", "DYNAMIC_TARGET_RAW": "K2_TARGET_RAW", "DYNAMIC_TARGET_ZMEAN": "K2_TARGET_ZMEAN"}), on="EVENT", how="left")
    k1 = k1.merge(k1t[["EVENT_ID", "DYNAMIC_TARGET_RAW", "DYNAMIC_TARGET_ZMEAN", "ACTIVE_FRACTION", "REENTRY_FRACTION", "TRANSITION_DENSITY", "GAIN_FRACTION", "LOSS_FRACTION"]].rename(columns={"EVENT_ID": "EVENT", "DYNAMIC_TARGET_RAW": "K1_TARGET_RAW", "DYNAMIC_TARGET_ZMEAN": "K1_TARGET_ZMEAN"}), on="EVENT", how="left")
    a = pd.read_csv(AONLY).rename(columns={"EVENT": "EVENT"})
    if "S_A" in a:
        a = a[["EVENT", "S_A"]].rename(columns={"S_A": "K5_A_ONLY_SCORE"})
    common_phys = pd.read_csv(COMMON_PHYS).rename(columns={"EVENT_ID": "EVENT"})
    base = freq.merge(abc, on="EVENT", how="outer", suffixes=("", "_ABC")).merge(geom, on="EVENT", how="outer", suffixes=("", "_GEOM"))
    base = base.merge(common_phys, on="EVENT", how="left", suffixes=("", "_PHYS"))
    base = base.merge(k5, on="EVENT", how="left").merge(k1, on="EVENT", how="left").merge(k2, on="EVENT", how="left").merge(a, on="EVENT", how="left")
    return base, {"abc": abc, "freq": freq, "geom": geom, "k5": k5, "k1": k1, "k2": k2, "a_only": a}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df, src = load_inputs()
    df.to_csv(OUT / "FREQUENCY_K_AXIS_EVENT_TABLE.csv", index=False)
    # Fixed geometry fields are descriptive inputs; no feature selection is performed here.
    geom_cols = ["path_nodes", "time_span_s", "f_directness", "f_turns"]
    for c in geom_cols:
        df[c] = numeric(df[c])
    group_rows = []
    for axis, score, target in [("K5_GLOBAL", "K5_SCORE", "OBS_ACTIVE_FRACTION"), ("K5_A_ONLY", "K5_A_ONLY_SCORE", None), ("K1_GR16", "K1_SCORE", "K1_TARGET_ZMEAN"), ("K2_OBS16", "K2_SCORE", "K2_TARGET_ZMEAN")]:
        sub = df[numeric(df[score]).notna()].copy()
        for g in ["FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY", "ABC_CLASS"]:
            group_rows += group_stats(sub, axis, score, g, score, target if axis != "K5_GLOBAL" else target)
        for g in ["path_nodes", "time_span_s", "f_directness", "f_turns", "frequency_span_hz", "transition_count"]:
            if g in sub:
                c = corr(sub[score], sub[g])
                group_rows.append({"AXIS": axis, "GROUP_FIELD": "NUMERIC_GEOMETRY", "GROUP": g, "N": c["n"], "SCORE_MEAN": np.nan, "SCORE_MEDIAN": np.nan, "SCORE_STD": np.nan, "PEARSON_R": c["pearson_r"], "PEARSON_P": c["pearson_p"], "SPEARMAN_RHO": c["spearman_rho"], "SPEARMAN_P": c["spearman_p"]})
    pd.DataFrame(group_rows).to_csv(OUT / "K_AXIS_FAMILY_ABC_GEOMETRY_SUMMARY.csv", index=False)
    # First-stage physical audit: raw physical candidates, kept separate from derived K scores.
    physical_rows = []
    physical_tests = []
    raw_phys = ["M_DET", "MC_DET", "Q", "ETA", "CHI_EFF", "CHI_P", "SPIN1Z", "SPIN2Z", "R", "CHI_A"]
    for fam_field in ["FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY", "FREQ_MAG_FAMILY", "ABC_CLASS"]:
        if fam_field not in df:
            continue
        fam_fields = [fam_field] if fam_field != "FREQ_MAG_FAMILY" else ["FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY"]
        for var in raw_phys:
            if var not in df:
                continue
            vals = numeric(df[var])
            keep = vals.notna() & df[fam_field].notna()
            sub = df.loc[keep, [fam_field, var]].copy()
            if sub.empty:
                continue
            for group, g in sub.groupby(fam_field, dropna=False):
                v = numeric(g[var]).dropna()
                physical_rows.append({"FAMILY_FIELD": fam_field, "PHYSICAL_VARIABLE": var, "FAMILY": group, "N": len(v), "MEAN": v.mean(), "MEDIAN": v.median(), "STD": v.std(ddof=1), "MIN": v.min(), "MAX": v.max()})
            groups = [numeric(g[var]).dropna().to_numpy() for _, g in sub.groupby(fam_field, dropna=False)]
            if len(groups) >= 2 and sum(len(x) for x in groups) >= 4:
                from scipy.stats import kruskal
                try:
                    h, p = kruskal(*groups)
                except ValueError:
                    h, p = np.nan, np.nan
            else:
                h, p = np.nan, np.nan
            physical_tests.append({"FAMILY_FIELD": fam_field, "PHYSICAL_VARIABLE": var, "N": len(sub), "GROUPS": sub[fam_field].nunique(), "KRUSKAL_H": h, "KRUSKAL_P": p})
    # remove duplicated MAG loop rows while keeping the explicit joint family below
    pr = pd.DataFrame(physical_rows).drop_duplicates()
    pr.to_csv(OUT / "FREQUENCY_FAMILY_PHYSICAL_ASSOCIATION.csv", index=False)
    physical_test_df = pd.DataFrame(physical_tests).drop_duplicates()
    physical_test_df.to_csv(OUT / "FREQUENCY_FAMILY_PHYSICAL_TESTS.csv", index=False)
    # Score/target association on each axis, keeping branch-native targets separate.
    assocs = []
    for axis, score, target in [("K5_GLOBAL", "K5_SCORE", "OBS_ACTIVE_FRACTION"), ("K1_GR16", "K1_SCORE", "K1_TARGET_ZMEAN"), ("K2_OBS16", "K2_SCORE", "K2_TARGET_ZMEAN")]:
        sub = df[[score, target]].copy()
        c = corr(sub[score], sub[target])
        c.update({"AXIS": axis, "SCORE_FIELD": score, "TARGET_FIELD": target})
        assocs.append(c)
    pd.DataFrame(assocs).to_csv(OUT / "K_AXIS_TARGET_ASSOCIATIONS.csv", index=False)
    # Deterministic nested explanatory comparison. Context = frozen labels + fixed geometry block.
    model_rows = []
    for axis, score, target in [("K5_GLOBAL", "K5_SCORE", "OBS_ACTIVE_FRACTION"), ("K1_GR16", "K1_SCORE", "K1_TARGET_ZMEAN"), ("K2_OBS16", "K2_SCORE", "K2_TARGET_ZMEAN")]:
        sub = df[numeric(df[score]).notna() & numeric(df[target]).notna()].copy()
        if len(sub) == 0:
            continue
        freq_x = pd.concat([design_categorical(sub, "FREQ_MAG_FAMILY"), design_categorical(sub, "FREQ_SHAPE_FAMILY")], axis=1)
        abc_x = design_categorical(sub, "ABC_CLASS")
        geom_x = pd.DataFrame({c: zscore(sub[c]) for c in geom_cols if c in sub})
        k_x = pd.DataFrame({score: zscore(sub[score])})
        blocks = {"INTERCEPT_ONLY": pd.DataFrame(index=sub.index), "K_ONLY": k_x, "FREQ_ONLY": freq_x, "ABC_ONLY": abc_x, "GEOMETRY_ONLY": geom_x, "CONTEXT_FREQ_ABC_GEOMETRY": pd.concat([freq_x, abc_x, geom_x], axis=1), "CONTEXT_PLUS_K": pd.concat([freq_x, abc_x, geom_x, k_x], axis=1)}
        context = None
        for name, X in blocks.items():
            m = ols_metrics(sub[target], X)
            m.update({"AXIS": axis, "MODEL": name, "TARGET": target, "SCORE": score})
            model_rows.append(m)
            if name == "CONTEXT_FREQ_ABC_GEOMETRY":
                context = m
        plus = next((x for x in model_rows[::-1] if x["AXIS"] == axis and x["MODEL"] == "CONTEXT_PLUS_K"), None)
        if context and plus and np.isfinite(context["bic"]) and np.isfinite(plus["bic"]):
            model_rows.append({"AXIS": axis, "MODEL": "K_INCREMENT_OVER_CONTEXT", "TARGET": target, "SCORE": score, "n": plus["n"], "p": plus["p"], "df_resid": plus["df_resid"], "r2": plus["r2"] - context["r2"], "adj_r2": plus["adj_r2"] - context["adj_r2"], "rmse": plus["rmse"] - context["rmse"], "bic": plus["bic"] - context["bic"], "aic": plus["aic"] - context["aic"]})
    pd.DataFrame(model_rows).to_csv(OUT / "K_AXIS_INCREMENTAL_MODEL_COMPARISON.csv", index=False)
    # Frozen formula/provenance summary.
    formulas = {
        "K5_GLOBAL": "0.22030031492055946*z(R) + 0.3457660274266933*z(CHI_A_NORMALIZED); source R40 S_KERR_ORDINAL / R39 P1 S",
        "K1_GR16": "0.22727260016061515*z_BRANCH(CHI_P); source GR16 selected candidate",
        "K2_OBS16": "2.2539666336842394*z_BRANCH(M_DET) - 1.9356907205819978*z_BRANCH(MC_DET); source OBS16 selected candidate",
        "K5_A_ONLY_DIAGNOSTIC": "0.26368072470484993*z_A(R) + 0.19053949293019626*z_A(CHI_A_NORMALIZED); source A-only frozen branch"
    }
    counts = []
    for axis, score in [("K5_GLOBAL", "K5_SCORE"), ("K1_GR16", "K1_SCORE"), ("K2_OBS16", "K2_SCORE"), ("K5_A_ONLY", "K5_A_ONLY_SCORE")]:
        s = df[numeric(df[score]).notna()]
        counts.append({"AXIS": axis, "N_SCORE": len(s), "N_FREQ": s.FREQ_MAG_FAMILY.notna().sum(), "N_ABC": s.ABC_CLASS.notna().sum(), "N_GEOMETRY": s.path_nodes.notna().sum()})
    pd.DataFrame(counts).to_csv(OUT / "K_AXIS_JOIN_COUNTS.csv", index=False)
    summary = []
    summary.append("R_STATUS=PASS_EXPLORATORY_CROSS_AUDIT")
    summary.append("PURPOSE=Frequency family x K1/K2/K5 x ABC x geometry; axes kept separate")
    summary.append("NO_SCORE_AVERAGING=TRUE")
    summary.append("NO_MAP_OR_PATH_REBUILD=TRUE")
    summary.append("K1_SCOPE=GR16 branch-local, N=16")
    summary.append("K2_SCOPE=OBS16 branch-local, N=16")
    summary.append("K5_SCOPE=global R40/R39 P1, N=96")
    summary.append("K5_R40_R39_MAX_ABS_SCORE_DIFF=%.16g" % numeric(df["K5_SCORE_DIFF_R40_MINUS_R39"]).abs().max())
    for row in counts:
        summary.append("%s_N_SCORE=%s" % (row["AXIS"], row["N_SCORE"]))
    for row in assocs:
        summary.append("%s_SCORE_TARGET_SPEARMAN=%.12g" % (row["AXIS"], row["spearman_rho"] if np.isfinite(row["spearman_rho"]) else np.nan))
        summary.append("%s_SCORE_TARGET_PEARSON=%.12g" % (row["AXIS"], row["pearson_r"] if np.isfinite(row["pearson_r"]) else np.nan))
    inc = pd.DataFrame(model_rows)
    if not inc.empty:
        for axis in ["K5_GLOBAL", "K1_GR16", "K2_OBS16"]:
            z = inc[(inc.AXIS == axis) & (inc.MODEL == "K_INCREMENT_OVER_CONTEXT")]
            if len(z):
                q = z.iloc[0]
                summary.append("%s_INCREMENTAL_DELTA_R2=%.12g" % (axis, q.r2))
                summary.append("%s_INCREMENTAL_DELTA_BIC=%.12g" % (axis, q.bic))
    # Compact, explicit first-stage readout: frequency family versus available raw physical variables.
    for ff, var in [("FREQ_MAG_FAMILY", "CHI_A"), ("FREQ_SHAPE_FAMILY", "CHI_A"), ("FREQ_MAG_FAMILY", "R"), ("FREQ_SHAPE_FAMILY", "R"), ("FREQ_MAG_FAMILY", "M_DET"), ("FREQ_SHAPE_FAMILY", "M_DET")]:
        q = physical_test_df[(physical_test_df.FAMILY_FIELD == ff) & (physical_test_df.PHYSICAL_VARIABLE == var)]
        if len(q):
            x = q.iloc[0]
            summary.append("FAMILY_PHYSICAL_TEST=%s|%s|N=%s|Kruskal_H=%s|p=%s" % (ff, var, x.N, x.KRUSKAL_H, x.KRUSKAL_P))
    for famfield in ["FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY"]:
        for fam in sorted(df[famfield].dropna().unique()):
            q = df[df[famfield] == fam]
            summary.append("%s_%s_N=%d_K5_MEAN=%.12g_K5_MEDIAN=%.12g" % (famfield, fam, len(q), numeric(q.K5_SCORE).mean(), numeric(q.K5_SCORE).median()))
    summary += ["INTERPRETATION=Descriptive cross-axis comparison; K1/K2 branch-local and not pooled with K5", "PHYSICAL_VARIABLE_COVERAGE_NOTE=M_DET/MC_DET/Q/ETA/CHI_EFF/CHI_P/SPIN1Z/SPIN2Z are available only on the exact 16-event K1/K2 source intersection; R/CHI_A are available on the 96-event K5 source", "CAUSAL_CLAIM=FALSE", "NEW_K_LAW_FIT=FALSE", "HOLDOUT30_ACCESSED=FALSE"]
    (OUT / "SUMMARY.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    prov = {"inputs": {str(p): sha(p) for p in [ABC, FREQ, GEOM, R40, R39, K1, K1T, K2, K2T, AONLY, COMMON_PHYS]}, "formulas": formulas, "rules": {"event_join": "exact EVENT ID", "score_averaging": False, "new_map": False, "new_path": False, "new_law_fit": False, "holdout30": False}, "outputs": {}}
    (OUT / "PROVENANCE.json").write_text(json.dumps(prov, indent=2), encoding="utf-8")
    for p in sorted(OUT.iterdir()):
        if p.is_file() and p.name != "SHA256_MANIFEST.txt":
            prov["outputs"][p.name] = sha(p)
    (OUT / "PROVENANCE.json").write_text(json.dumps(prov, indent=2), encoding="utf-8")
    manifest = [f"{sha(p)}  {p.name}" for p in sorted(OUT.iterdir()) if p.is_file() and p.name != "SHA256_MANIFEST.txt"]
    (OUT / "SHA256_MANIFEST.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    send = [
        "R_STATUS=PASS_EXPLORATORY_CROSS_AUDIT",
        "N_FREQUENCY_EVENTS=%d" % df.FREQ_MAG_FAMILY.notna().sum(),
        "N_ABC_EVENTS=%d" % df.ABC_CLASS.notna().sum(),
        "K1_GR16_N=16; K2_OBS16_N=16; K5_GLOBAL_N=96",
        "K1_FORMULA=" + formulas["K1_GR16"],
        "K2_FORMULA=" + formulas["K2_OBS16"],
        "K5_FORMULA=" + formulas["K5_GLOBAL"],
        "SCORE_AVERAGING=FALSE",
        "INTERPRETATION=Use K-axis-specific tables and incremental model rows; do not pool K1/K2/K5 into one mean score",
        "HOLDOUT30_ACCESSED=FALSE"
    ]
    (OUT / "SEND_TO_CHAT.txt").write_text("\n".join(send) + "\n", encoding="utf-8")
    print("OUT", OUT)
    print("ROWS", len(df))
    print("COUNTS", counts)


if __name__ == "__main__":
    main()
