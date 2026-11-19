import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(r"E:\RIUD_ACTIVE_20260808")
SOURCE = ROOT / "RIUD_FREQUENCY_FAMILY_K1_K2_K5_ABC_GEOMETRY_CROSS_AUDIT_R0_20260826" / "FREQUENCY_K_AXIS_EVENT_TABLE.csv"
OUT = ROOT / "RIUD_FREQUENCY_FAMILY_K1_K2_K5_ABC_GEOMETRY_FREE_EXPLORATION_R1_20260826"
COMMON = ROOT / "RIUD_PIV_SXS_GR_RELEASE_R1_20260826" / "SXS_GR" / "RIUD_EARLYMAXFLOW16_MATCHED_PURE_GR_FULL_SYSTEM_TEST_R0_20260824" / "06_INDEPENDENT_PHYSICAL_AXIS" / "COMMON_PHYSICAL_CANDIDATE_TABLE.csv"
ABC = ROOT / "RIUD_ABC_INTEGRATED_MAP_LAW_LEDGER_R0_20260825" / "ABC_96_EVENT_INTEGRATED_LEDGER.csv"
FREQ = ROOT / "RIUD_DEV99_FREQUENCY_MAG_SHAPE_CENSUS_R0_20260824" / "07_FREQ_MAG_SHAPE_ASSIGNMENTS.csv"
GEOM = ROOT / "RIUD_DEV99_DYNAMICS_REPRESENTATION_FREEZE_R10J0R2_PCA90_FIX_PAR16_20260811" / "01_FREEZE" / "R10J0R2_EVENT_DYNAMICS_FEATURES.csv"
R40 = ROOT / "RIUD_DEV99_PHYSICAL_DYNAMICAL_LAW_FREEZE_R40_20260815" / "R40_SUPPORT_EVENTS.csv"


def sha(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def num(s):
    return pd.to_numeric(s, errors="coerce")


def qstats(s):
    x = num(s).dropna()
    if x.empty:
        return {"N": 0, "MEAN": np.nan, "MEDIAN": np.nan, "STD": np.nan, "Q25": np.nan, "Q75": np.nan, "MIN": np.nan, "MAX": np.nan}
    return {"N": len(x), "MEAN": x.mean(), "MEDIAN": x.median(), "STD": x.std(ddof=1), "Q25": x.quantile(.25), "Q75": x.quantile(.75), "MIN": x.min(), "MAX": x.max()}


def corr(x, y):
    from scipy.stats import pearsonr, spearmanr
    z = pd.DataFrame({"x": num(x), "y": num(y)}).dropna()
    if len(z) < 3 or z.x.nunique() < 2 or z.y.nunique() < 2:
        return len(z), np.nan, np.nan, np.nan, np.nan
    pr, pp = pearsonr(z.x, z.y)
    sr, sp = spearmanr(z.x, z.y)
    return len(z), pr, pp, sr, sp


def _esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _svg_shell(w, h, title, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="white"/><text x="20" y="24" font-family="Arial" font-size="16" font-weight="bold">{_esc(title)}</text>{body}</svg>'


def _extent(values):
    x = np.asarray([v for v in values if np.isfinite(v)], dtype=float)
    if len(x) == 0:
        return 0.0, 1.0
    lo, hi = float(x.min()), float(x.max())
    if lo == hi:
        lo -= 1.0; hi += 1.0
    pad = 0.06 * (hi - lo)
    return lo - pad, hi + pad


def _px(v, lo, hi, a, b):
    return a + (float(v) - lo) / (hi - lo) * (b - a)


def write_scatter(path, data, x, y, group, title, xlabel, ylabel, width=760, height=460):
    d = data[[x, y] + ([group] if group else [])].copy()
    d[x] = num(d[x]); d[y] = num(d[y]); d = d.replace([np.inf, -np.inf], np.nan).dropna(subset=[x, y])
    ml, mr, mt, mb = 72, 160, 48, 55
    xlo, xhi = _extent(d[x]); ylo, yhi = _extent(d[y])
    body = [f'<line x1="{ml}" y1="{height-mb}" x2="{width-mr}" y2="{height-mb}" stroke="black"/><line x1="{ml}" y1="{mt}" x2="{ml}" y2="{height-mb}" stroke="black"/>']
    cats = sorted(d[group].astype(str).unique()) if group else ["all"]
    colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e", "#17becf"]
    cmap = {c: colors[i % len(colors)] for i, c in enumerate(cats)}
    for _, r in d.iterrows():
        c = str(r[group]) if group else "all"
        body.append(f'<circle cx="{_px(r[x],xlo,xhi,ml,width-mr):.2f}" cy="{_px(r[y],ylo,yhi,height-mb,mt):.2f}" r="3.5" fill="{cmap[c]}" fill-opacity="0.72"><title>{_esc(c)}: {float(r[x]):.6g}, {float(r[y]):.6g}</title></circle>')
    for i, c in enumerate(cats):
        yy = mt + 22 + 20*i
        body.append(f'<circle cx="{width-mr+16}" cy="{yy-5}" r="4" fill="{cmap[c]}"/><text x="{width-mr+26}" y="{yy}" font-family="Arial" font-size="11">{_esc(c)}</text>')
    body += [f'<text x="{(ml+width-mr)//2}" y="{height-12}" text-anchor="middle" font-family="Arial" font-size="12">{_esc(xlabel)}</text>', f'<text x="16" y="{(mt+height-mb)//2}" transform="rotate(-90 16 {(mt+height-mb)//2})" text-anchor="middle" font-family="Arial" font-size="12">{_esc(ylabel)}</text>']
    path.write_text(_svg_shell(width, height, title, "".join(body)), encoding="utf-8")


def write_heatmap(path, data, row_field, col_field, title, width=760, height=420):
    t = pd.crosstab(data[row_field], data[col_field], dropna=False)
    rows, cols = list(t.index.astype(str)), list(t.columns.astype(str))
    ml, mt, cellw, cellh = 120, 60, 90, 42
    maxv = max(1, int(t.to_numpy().max()) if t.size else 1)
    body = []
    for i, rr in enumerate(rows):
        body.append(f'<text x="{ml-8}" y="{mt+i*cellh+cellh//2+4}" text-anchor="end" font-family="Arial" font-size="11">{_esc(rr)}</text>')
        for j, cc in enumerate(cols):
            v = int(t.loc[t.index[i], t.columns[j]])
            shade = int(245 - 180*v/maxv)
            body.append(f'<rect x="{ml+j*cellw}" y="{mt+i*cellh}" width="{cellw-2}" height="{cellh-2}" fill="rgb({shade},{shade+min(10,255-shade)},{255})"/><text x="{ml+j*cellw+cellw/2}" y="{mt+i*cellh+cellh//2+4}" text-anchor="middle" font-family="Arial" font-size="12">{v}</text>')
    for j, cc in enumerate(cols):
        body.append(f'<text x="{ml+j*cellw+cellw/2}" y="{mt-12}" text-anchor="middle" font-family="Arial" font-size="11">{_esc(cc)}</text>')
    path.write_text(_svg_shell(width, height, title, "".join(body)), encoding="utf-8")


def write_category_strip(path, data, category, value, title, ylabel, width=900, height=500):
    d = data[[category, value]].copy(); d[value] = num(d[value]); d = d.dropna(); cats = sorted(d[category].astype(str).unique())
    ml, mr, mt, mb = 70, 40, 52, 60; xlo, xhi = -0.6, max(0.6, len(cats)-0.4); ylo, yhi = _extent(d[value])
    body = [f'<line x1="{ml}" y1="{height-mb}" x2="{width-mr}" y2="{height-mb}" stroke="black"/><line x1="{ml}" y1="{mt}" x2="{ml}" y2="{height-mb}" stroke="black"/>']
    for i, c in enumerate(cats):
        vals = d.loc[d[category].astype(str) == c, value].to_numpy(dtype=float)
        for j, v in enumerate(vals):
            jitter = ((j % 9) - 4) * 0.045
            body.append(f'<circle cx="{_px(i+jitter,xlo,xhi,ml,width-mr):.2f}" cy="{_px(v,ylo,yhi,height-mb,mt):.2f}" r="3" fill="#1f77b4" fill-opacity="0.55"/>')
        med = float(np.median(vals))
        body.append(f'<line x1="{_px(i-.25,xlo,xhi,ml,width-mr):.2f}" y1="{_px(med,ylo,yhi,height-mb,mt):.2f}" x2="{_px(i+.25,xlo,xhi,ml,width-mr):.2f}" y2="{_px(med,ylo,yhi,height-mb,mt):.2f}" stroke="#d62728" stroke-width="3"/>')
        body.append(f'<text x="{_px(i,xlo,xhi,ml,width-mr):.2f}" y="{height-mb+20}" text-anchor="middle" font-family="Arial" font-size="11">{_esc(c)}</text>')
    body.append(f'<text x="16" y="{(mt+height-mb)//2}" transform="rotate(-90 16 {(mt+height-mb)//2})" text-anchor="middle" font-family="Arial" font-size="12">{_esc(ylabel)}</text>')
    path.write_text(_svg_shell(width, height, title, "".join(body)), encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    d = pd.read_csv(SOURCE)
    d.to_csv(OUT / "EXPLORATION_EVENT_TABLE.csv", index=False)
    family_cols = ["FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY"]
    # Keep the stored physical S column as its own axis even where it is
    # numerically associated with the K5 implementation.
    score_cols = {"S_GLOBAL": "S", "K5_GLOBAL": "K5_SCORE", "K5_A_ONLY": "K5_A_ONLY_SCORE", "K1_GR16": "K1_SCORE", "K2_OBS16": "K2_SCORE"}
    physical_cols = ["M_DET", "MC_DET", "Q", "ETA", "CHI_EFF", "CHI_P", "SPIN1Z", "SPIN2Z", "R", "CHI_A"]
    geometry_cols = ["path_nodes", "transition_count", "time_span_s", "frequency_span_hz", "f_total_variation_hz", "f_directness", "f_turns", "transition_entropy", "network_z_median"]

    # Exploratory rank bins only. They are descriptive partitions, not new scientific thresholds.
    bin_cols = {}
    for axis, score in score_cols.items():
        b = axis + "_RANK_BIN"
        x = num(d[score])
        rank = x.rank(method="first")
        d[b] = pd.qcut(rank, q=min(3, int(rank.notna().sum())), labels=["Q1_LOW", "Q2_MID", "Q3_HIGH"][:min(3, int(rank.notna().sum()))]) if rank.notna().sum() >= 3 else np.nan
        bin_cols[axis] = b
    geom_bin_cols = {}
    for variable in geometry_cols:
        if variable not in d:
            continue
        b = "GEOM_" + variable + "_RANK_BIN"
        x = num(d[variable]); rank = x.rank(method="first")
        d[b] = pd.qcut(rank, q=min(3, int(rank.notna().sum())), labels=["Q1_LOW", "Q2_MID", "Q3_HIGH"][:min(3, int(rank.notna().sum()))]) if rank.notna().sum() >= 3 else np.nan
        geom_bin_cols[variable] = b

    # Every categorical cross-tab requested, retaining empty/low-n cells rather than suppressing them.
    count_rows = []
    for a, b in [("FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY"), ("FREQ_MAG_FAMILY", "ABC_CLASS"), ("FREQ_SHAPE_FAMILY", "ABC_CLASS")]:
        t = pd.crosstab(d[a], d[b], dropna=False)
        for i, row in t.iterrows():
            for j, value in row.items():
                count_rows.append({"FIELD_A": a, "VALUE_A": i, "FIELD_B": b, "VALUE_B": j, "N": int(value)})
    for axis, score in score_cols.items():
        available = d[num(d[score]).notna()]
        for a, b in [("FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY"), ("FREQ_MAG_FAMILY", "ABC_CLASS"), ("FREQ_SHAPE_FAMILY", "ABC_CLASS")]:
            t = pd.crosstab(available[a], available[b], dropna=False)
            for i, row in t.iterrows():
                for j, value in row.items():
                    count_rows.append({"FIELD_A": f"{axis}:{a}", "VALUE_A": i, "FIELD_B": b, "VALUE_B": j, "N": int(value)})
    pd.DataFrame(count_rows).to_csv(OUT / "CATEGORICAL_CROSSTABS_ALL_COMBINATIONS.csv", index=False)

    # K scores conditioned on each family/ABC label.
    score_rows = []
    for axis, score in score_cols.items():
        for group_field in ["FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY", "ABC_CLASS"]:
            for group, g in d.groupby(group_field, dropna=False):
                st = qstats(g[score])
                score_rows.append({"AXIS": axis, "SCORE_FIELD": score, "GROUP_FIELD": group_field, "GROUP": group, **st})
    pd.DataFrame(score_rows).to_csv(OUT / "K_SCORE_BY_FAMILY_ABC_SUMMARY.csv", index=False)

    # Raw physical-variable distributions by the two frequency families and ABC.
    phys_rows = []
    for group_field in family_cols + ["ABC_CLASS"]:
        for variable in physical_cols + list(score_cols.values()):
            if variable not in d:
                continue
            for group, g in d.groupby(group_field, dropna=False):
                st = qstats(g[variable])
                phys_rows.append({"GROUP_FIELD": group_field, "GROUP": group, "VARIABLE": variable, **st})
    pd.DataFrame(phys_rows).to_csv(OUT / "PHYSICAL_AND_SCORE_BY_FAMILY_ABC.csv", index=False)

    # Geometry profiles by family/ABC, plus frequency-family joint cell profiles.
    geo_rows = []
    for group_fields in family_cols + ["ABC_CLASS", ["FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY", "ABC_CLASS"]]:
        if isinstance(group_fields, str):
            group_fields = [group_fields]
        for group, g in d.groupby(group_fields, dropna=False):
            if not isinstance(group, tuple):
                group = (group,)
            base = {"GROUP_FIELDS": "|".join(group_fields), "GROUP": "|".join(map(str, group))}
            for variable in geometry_cols:
                st = qstats(g[variable])
                geo_rows.append({**base, "VARIABLE": variable, **st})
    pd.DataFrame(geo_rows).to_csv(OUT / "GEOMETRY_BY_FAMILY_ABC_COMBINATIONS.csv", index=False)

    # All numeric pairwise correlations among the requested physical, K, S, and geometry values.
    numeric_cols = [c for c in physical_cols + list(score_cols.values()) + geometry_cols if c in d]
    pair_rows = []
    for a, b in itertools.combinations(numeric_cols, 2):
        n, pr, pp, sr, sp = corr(d[a], d[b])
        pair_rows.append({"VARIABLE_A": a, "VARIABLE_B": b, "N": n, "PEARSON_R": pr, "PEARSON_P": pp, "SPEARMAN_RHO": sr, "SPEARMAN_P": sp})
    pd.DataFrame(pair_rows).sort_values("SPEARMAN_P", na_position="last").to_csv(OUT / "NUMERIC_PAIRWISE_CORRELATIONS.csv", index=False)

    # Conditional score/geometry correlations: no pooled score and no model fit.
    cond_rows = []
    for axis, score in score_cols.items():
        for condition_field in ["FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY", "ABC_CLASS"]:
            for condition, g in d.groupby(condition_field, dropna=False):
                for variable in physical_cols + geometry_cols:
                    if variable not in d:
                        continue
                    n, pr, pp, sr, sp = corr(g[score], g[variable])
                    cond_rows.append({"AXIS": axis, "SCORE_FIELD": score, "CONDITION_FIELD": condition_field, "CONDITION": condition, "VARIABLE": variable, "N": n, "PEARSON_R": pr, "PEARSON_P": pp, "SPEARMAN_RHO": sr, "SPEARMAN_P": sp})
    pd.DataFrame(cond_rows).to_csv(OUT / "CONDITIONAL_K_SCORE_PHYSICAL_GEOMETRY_CORRELATIONS.csv", index=False)

    # Four-way and five-way exploratory combination ledgers.
    combo_rows = []
    for axis, score in score_cols.items():
        b = bin_cols[axis]
        for keys in [["FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY", "ABC_CLASS", b], ["FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY", "ABC_CLASS", b, geom_bin_cols["path_nodes"]], ["FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY", "ABC_CLASS", b, geom_bin_cols["frequency_span_hz"]]]:
            q = d[d[b].notna()].groupby(keys, dropna=False).size().reset_index(name="N")
            for _, row in q.iterrows():
                out = {"AXIS": axis, "COMBINATION_FIELDS": "|".join(keys), "N": int(row["N"])}
                for k in keys:
                    out[k] = row[k]
                combo_rows.append(out)
    # Exact common 16: all three branch scores jointly, with the same family/ABC/geometry fields.
    common16 = d[d.K1_SCORE.notna() & d.K2_SCORE.notna() & d.K5_SCORE.notna()].copy()
    keys = ["FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY", "ABC_CLASS", bin_cols["K1_GR16"], bin_cols["K2_OBS16"], bin_cols["K5_GLOBAL"], geom_bin_cols["path_nodes"], geom_bin_cols["frequency_span_hz"]]
    q = common16.groupby(keys, dropna=False).size().reset_index(name="N")
    for _, row in q.iterrows():
        out = {"AXIS": "K1_K2_K5_COMMON16", "COMBINATION_FIELDS": "|".join(keys), "N": int(row["N"])}
        for k in keys:
            out[k] = row[k]
        combo_rows.append(out)
    pd.DataFrame(combo_rows).to_csv(OUT / "FOUR_WAY_AND_COMMON16_COMBINATION_COUNTS.csv", index=False)

    enrichment_rows = []
    for axis, score in score_cols.items():
        b = bin_cols[axis]
        sub = d[d[b].notna()].copy()
        for family_field in ["FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY", "ABC_CLASS"]:
            total = sub[family_field].value_counts(dropna=False)
            for bin_name, g in sub.groupby(b, dropna=False):
                counts = g[family_field].value_counts(dropna=False)
                for group in total.index:
                    n = int(counts.get(group, 0)); den = int(len(g)); base = int(total[group])
                    enrichment_rows.append({"AXIS": axis, "RANK_BIN": bin_name, "GROUP_FIELD": family_field, "GROUP": group, "N_BIN": den, "N_GROUP_IN_BIN": n, "BIN_FRACTION": n/den if den else np.nan, "OVERALL_GROUP_FRACTION": base/len(sub) if len(sub) else np.nan, "ENRICHMENT_RATIO": (n/den)/(base/len(sub)) if den and base and len(sub) else np.nan})
    pd.DataFrame(enrichment_rows).to_csv(OUT / "K_RANK_BIN_FAMILY_ABC_ENRICHMENT.csv", index=False)

    # Simple rank of descriptive contrasts, explicitly labelled exploratory.
    contrast_rows = []
    for group_field in family_cols + ["ABC_CLASS"]:
        for variable in physical_cols + list(score_cols.values()) + geometry_cols:
            if variable not in d:
                continue
            groups = [(str(k), num(g[variable]).dropna()) for k, g in d.groupby(group_field, dropna=False)]
            groups = [(k, x) for k, x in groups if len(x) >= 2]
            for (ga, xa), (gb, xb) in itertools.combinations(groups, 2):
                pooled = math_sqrt((xa.var(ddof=1) + xb.var(ddof=1)) / 2) if xa.var(ddof=1) + xb.var(ddof=1) > 0 else np.nan
                contrast_rows.append({"GROUP_FIELD": group_field, "VARIABLE": variable, "GROUP_A": ga, "GROUP_B": gb, "N_A": len(xa), "N_B": len(xb), "MEAN_A": xa.mean(), "MEAN_B": xb.mean(), "MEDIAN_A": xa.median(), "MEDIAN_B": xb.median(), "ABS_MEAN_DIFF": abs(xa.mean() - xb.mean()), "STANDARDIZED_MEAN_DIFF": abs(xa.mean() - xb.mean()) / pooled if np.isfinite(pooled) and pooled > 0 else np.nan})
    pd.DataFrame(contrast_rows).sort_values("STANDARDIZED_MEAN_DIFF", ascending=False, na_position="last").to_csv(OUT / "DESCRIPTIVE_CONTRAST_RANKING.csv", index=False)

    plots = OUT / "plots"
    plots.mkdir(exist_ok=True)
    # SVG plots are generated with the standard library so the audit does not depend on a plotting package.
    write_scatter(plots / "frequency_mag_vs_chi_a.svg", d, "K5_SCORE", "CHI_A", "FREQ_MAG_FAMILY", "K5 global S vs CHI_A by FREQ_MAG", "K5 global S", "CHI_A")
    write_scatter(plots / "frequency_shape_vs_chi_a.svg", d, "K5_SCORE", "CHI_A", "FREQ_SHAPE_FAMILY", "K5 global S vs CHI_A by FREQ_SHAPE", "K5 global S", "CHI_A")
    write_heatmap(plots / "frequency_mag_x_abc.svg", d, "FREQ_MAG_FAMILY", "ABC_CLASS", "FREQ_MAG x ABC counts")
    write_heatmap(plots / "frequency_shape_x_abc.svg", d, "FREQ_SHAPE_FAMILY", "ABC_CLASS", "FREQ_SHAPE x ABC counts")
    write_category_strip(plots / "k5_by_frequency_mag.svg", d[d.K5_SCORE.notna()], "FREQ_MAG_FAMILY", "K5_SCORE", "K5 global S by FREQ_MAG", "K5 global S")
    write_category_strip(plots / "k5_by_frequency_shape.svg", d[d.K5_SCORE.notna()], "FREQ_SHAPE_FAMILY", "K5_SCORE", "K5 global S by FREQ_SHAPE", "K5 global S")
    write_category_strip(plots / "s_by_frequency_mag.svg", d[d.S.notna()], "FREQ_MAG_FAMILY", "S", "Stored S by FREQ_MAG", "S")
    write_category_strip(plots / "s_by_frequency_shape.svg", d[d.S.notna()], "FREQ_SHAPE_FAMILY", "S", "Stored S by FREQ_SHAPE", "S")
    write_scatter(plots / "k5_vs_path_nodes.svg", d, "path_nodes", "K5_SCORE", "FREQ_MAG_FAMILY", "K5 global S vs path geometry", "path nodes", "K5 global S")
    write_scatter(plots / "k5_vs_time_span.svg", d, "time_span_s", "K5_SCORE", "FREQ_MAG_FAMILY", "K5 global S vs time span", "time span (s)", "K5 global S")
    write_scatter(plots / "s_vs_path_nodes.svg", d, "path_nodes", "S", "FREQ_MAG_FAMILY", "Stored S vs path geometry", "path nodes", "S")
    common = d[d.K1_SCORE.notna() & d.K2_SCORE.notna() & d.K5_SCORE.notna()].copy()
    write_scatter(plots / "k1_vs_k2_by_shape_family.svg", common, "K1_SCORE", "K2_SCORE", "FREQ_SHAPE_FAMILY", "K1 vs K2 on exact common 16", "K1 GR16 score", "K2 OBS16 score")
    prof = d.groupby(["FREQ_MAG_FAMILY", "FREQ_SHAPE_FAMILY"])[geometry_cols].median(numeric_only=True)
    if not prof.empty:
        p = prof.reset_index(); p["CELL"] = p.FREQ_MAG_FAMILY.astype(str) + "|" + p.FREQ_SHAPE_FAMILY.astype(str)
        long = p.melt(id_vars=["CELL"], value_vars=["path_nodes", "time_span_s", "frequency_span_hz", "f_directness", "f_turns"], var_name="VARIABLE", value_name="VALUE")
        for variable, g in long.groupby("VARIABLE"):
            safe = str(variable).replace("/", "_")
            write_category_strip(plots / f"joint_family_{safe}.svg", g, "CELL", "VALUE", f"joint frequency-family geometry: {variable}", "median value")

    # Summary.
    summary = [
        "R_STATUS=PASS_FREE_EXPLORATORY_CROSS_AUDIT",
        "MODE=FREE_EXPLORATION_NO_INTEGRATED_REGRESSION",
        "N_EVENT_ROWS=%d" % len(d),
        "N_FREQUENCY_ROWS=%d" % d.FREQ_MAG_FAMILY.notna().sum(),
        "N_ABC_ROWS=%d" % d.ABC_CLASS.notna().sum(),
        "N_K5_GLOBAL=%d" % d.K5_SCORE.notna().sum(),
        "N_K5_A_ONLY=%d" % d.K5_A_ONLY_SCORE.notna().sum(),
        "N_K1_GR16=%d" % d.K1_SCORE.notna().sum(),
        "N_K2_OBS16=%d" % d.K2_SCORE.notna().sum(),
        "RAW_PHYSICAL_COVERAGE=R/CHI_A on 96-event K5 source; M_DET/MC_DET/Q/ETA/CHI_EFF/CHI_P/SPIN1Z/SPIN2Z on exact 16-event K1/K2 source",
        "SCORE_AVERAGING=FALSE",
        "NEW_MAP=FALSE",
        "NEW_PATH=FALSE",
        "NEW_K_LAW=FALSE",
        "CAUSAL_CLAIM=FALSE",
        "HOLDOUT30_ACCESSED=FALSE",
        "NOTE=Contrasts and plots are discovery-oriented descriptions; no p-value or regression is promoted as a law",
        "PLOTS=SVG standard-library plots in plots/; no matplotlib dependency",
        "RANK_BINS=Exploratory within-axis rank terciles only; not scientific thresholds",
    ]
    for field in family_cols + ["ABC_CLASS"]:
        summary.append("COUNTS_%s=%s" % (field, d[field].value_counts(dropna=False).to_dict()))
    if len(common) >= 3:
        from scipy.stats import spearmanr
        for a, b, label in [("K1_SCORE", "K2_SCORE", "K1_X_K2_COMMON16"), ("K1_SCORE", "K5_SCORE", "K1_X_K5_COMMON16"), ("K2_SCORE", "K5_SCORE", "K2_X_K5_COMMON16")]:
            rr, pp = spearmanr(common[a], common[b])
            summary.append("%s_SPEARMAN_RHO=%.12g|p=%.12g|N=%d" % (label, rr, pp, len(common)))
    summary += [
        "DERIVED_AXIS_WARNING=K1 is frozen linear CHI_P branch score; K5 includes frozen R and CHI_A; these constructional correlations are not independent discoveries",
        "COMMON16_ABC_SCOPE=K1/K2 common branch contains B=5,C=10,OTHER=1 and no A events",
    ]
    (OUT / "SUMMARY.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    inputs = [SOURCE, COMMON, ABC, FREQ, GEOM, R40]
    prov = {"inputs": {str(p): sha(p) for p in inputs}, "design": {"exact_event_join": True, "all_pairwise_descriptions": True, "no_score_averaging": True, "no_new_fit": True, "no_new_map": True, "no_new_path": True, "holdout30": False}, "outputs": {}}
    (OUT / "PROVENANCE.json").write_text(json.dumps(prov, indent=2), encoding="utf-8")
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name != "SHA256_MANIFEST.txt":
            prov["outputs"][str(p.relative_to(OUT))] = sha(p)
    (OUT / "PROVENANCE.json").write_text(json.dumps(prov, indent=2), encoding="utf-8")
    (OUT / "SHA256_MANIFEST.txt").write_text("\n".join(f"{sha(p)}  {p.relative_to(OUT)}" for p in sorted(OUT.rglob("*")) if p.is_file() and p.name != "SHA256_MANIFEST.txt") + "\n", encoding="utf-8")
    send = [
        "R_STATUS=PASS_FREE_EXPLORATORY_CROSS_AUDIT",
        "N_EVENT_ROWS=%d" % len(d),
        "K5_GLOBAL_N=96; K5_A_ONLY_N=73; K1_GR16_N=16; K2_OBS16_N=16",
        "FIRST_PHYSICAL_LOOK=FREQ_MAG has strongest visible CHI_A split; FREQ_SHAPE is not visibly separated by CHI_A in the frozen descriptive tables",
        "INTERACTION_MODE=All pairwise/joint tables and plots saved; no single integrated law selected",
        "SCORE_AVERAGING=FALSE",
        "CAUSAL_CLAIM=FALSE",
        "HOLDOUT30_ACCESSED=FALSE",
    ]
    (OUT / "SEND_TO_CHAT.txt").write_text("\n".join(send) + "\n", encoding="utf-8")
    print("OUT", OUT)
    print("ROWS", len(d), "PLOTS", len(list(plots.glob("*.svg"))))


def math_sqrt(x):
    return float(np.sqrt(x))


if __name__ == "__main__":
    main()
