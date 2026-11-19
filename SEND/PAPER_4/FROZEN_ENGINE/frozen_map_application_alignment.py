"""Pre-merger-priority affine alignment of the existing frozen DEV99 paths.

The input is the already materialized frozen A2 path support, bound to the
canonical DEV99 97-event cohort.  It is not a raw re-extraction and it is not
the candidate-bank expansion.  All stored nodes are retained, including
post-merger nodes through +0.03 s when present.

Alignment uses a positive affine map with a free offset.  tau=0 is a value in
the coordinate system, never an endpoint or an anchor.  The pre-merger
segment (tau<0) is given fixed priority; post-merger nodes are included only
as part of the same alignment and are reported separately.

This is read-only diagnostic work: no PATH rerun, law fit, null, Holdout, or
morphology input.
"""

from __future__ import annotations

import gzip
import hashlib
import itertools
import json
import math
import os
from collections import defaultdict, deque
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

# One global process pool; numerical libraries stay single-threaded inside a
# worker so the 16-way outer parallelism does not become nested parallelism.
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import numpy as np
import pandas as pd


WORKSPACE = Path(__file__).resolve().parent
COHORT_FILE = Path(
    r"E:\RIUD_ACTIVE_20260808\RIUD_DEV99_N4H3CR1_DISTINCT_BLOCK_3WAY4WAY_MULTIGATE_NULL_EMPTYSET_FIX_PAR16_20260812\01_FREEZE\N4H3CR1_PAIRED_97_EVENT_COHORT.csv"
)
FROZEN_PATH_ROOT = Path(
    r"E:\RIUD_ACTIVE_20260808\RIUD_DEV99_PATH_ONLY_CPU_ADAPTIVE_R10G_20260811\03_OUTPUT\RUNTIME_EXPORT"
)
PATH_FILENAME = "EXPANDED_A2_POSITION_FREE_PATH.csv"
CURRENT_PRIORITY = Path(
    r"E:\RIUD_ACTIVE_20260808\RIUD_DEV99_LATENT_COORDINATE_COMPOSITION_AUDIT_R1_20260814\OUTPUT\PAIRWISE_BEST_SCALE_EDGES.csv"
)
OUT = Path(
    r"E:\RIUD_ACTIVE_20260808\RIUD_DEV99_PREMERGER_PRIORITY_NODE_SUPPORT_SCALE_ALIGNMENT_R1_20260814\OUTPUT"
)

ALPHAS = np.asarray([0.0625, 0.0884, 0.125, 0.1768, 0.25, 0.3536, 0.5, 0.7071, 1.0, 1.4142, 2.0, 2.8284, 4.0, 5.6569, 8.0])
FEATURES = ["frequency_hz", "width_s", "robust_network_z", "width_persistence_count"]
MIN_MATCHES = 3
MIN_TARGET_COVERAGE = 0.50
MIN_REF_SPAN = 0.25
LOG_SCALE_TOL = math.log(1.5)
NODE_INDEX_TOL = 0.25
PREMERGER_WEIGHT = 0.75
POSTMERGER_WEIGHT = 0.25
MAX_WORKERS = 16

_WORKER_PATHS = None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_nodes() -> tuple[dict[str, dict[str, np.ndarray]], pd.DataFrame, list[str]]:
    cohort = pd.read_csv(COHORT_FILE)
    if "event" not in cohort.columns:
        raise RuntimeError("COHORT_EVENT_COLUMN_MISSING")
    events = [str(x) for x in cohort["event"].tolist()]
    if len(events) != 97 or len(set(events)) != 97:
        raise RuntimeError(f"DEV99_COHORT_BINDING_FAIL count={len(events)} unique={len(set(events))}")

    paths = {}
    manifest = []
    required = {"tau_s", *FEATURES}
    for event in events:
        path = FROZEN_PATH_ROOT / event / "output" / event / PATH_FILENAME
        if not path.exists():
            raise FileNotFoundError(f"FROZEN_PATH_MISSING={path}")
        df = pd.read_csv(path)
        missing = required - set(df.columns)
        if missing:
            raise RuntimeError(f"FROZEN_PATH_COLUMNS_MISSING event={event} missing={sorted(missing)}")
        g = df.copy()
        g["tau_s"] = pd.to_numeric(g["tau_s"], errors="coerce")
        for col in FEATURES:
            g[col] = pd.to_numeric(g[col], errors="coerce")
        g = g.sort_values(["tau_s", "path_index"], kind="mergesort")
        arr = {"time_s": g["tau_s"].to_numpy(float)}
        arr.update({col: g[col].to_numpy(float) for col in FEATURES})
        keep = np.ones(len(g), dtype=bool)
        for col in arr:
            keep &= np.isfinite(arr[col])
        if int(keep.sum()) < 2:
            raise RuntimeError(f"FROZEN_PATH_TOO_SHORT event={event} rows={int(keep.sum())}")
        arr = {k: v[keep] for k, v in arr.items()}
        if np.any(np.diff(arr["time_s"]) < 0):
            raise RuntimeError(f"TIME_ORDER_FAIL={event}")
        paths[event] = arr
        pre = arr["time_s"] < 0.0
        post = arr["time_s"] > 0.0
        manifest.append({
            "EVENT": event,
            "SOURCE_PATH": str(path),
            "SOURCE_SHA256": sha256_file(path),
            "N_NODES": int(len(arr["time_s"])),
            "PREMERGER_NODES": int(pre.sum()),
            "ZERO_NODES": int((arr["time_s"] == 0.0).sum()),
            "POSTMERGER_NODES": int(post.sum()),
            "TIME_MIN_S": float(arr["time_s"].min()),
            "TIME_MAX_S": float(arr["time_s"].max()),
        })
    return paths, pd.DataFrame(manifest), events


def load_priority():
    if not CURRENT_PRIORITY.exists():
        return {}
    df = pd.read_csv(CURRENT_PRIORITY)
    out = {}
    for i, r in df.iterrows():
        out[(str(r["TARGET_EVENT"]), str(r["REFERENCE_EVENT"]))] = int(i + 1)
    return out


def candidate_betas(tt, tr, alpha):
    # Offset candidates are the complete deterministic node-to-node affine
    # anchor grid for this fixed positive alpha.  No morphology or result-
    # driven candidate subset is used.
    vals = (tr[:, None] - alpha * tt[None, :]).ravel()
    vals = np.unique(np.round(vals, 12))
    return vals


def nearest_indices(values, ref_times):
    pos = np.searchsorted(ref_times, values, side="left")
    pos = np.clip(pos, 0, len(ref_times) - 1)
    left = np.clip(pos - 1, 0, len(ref_times) - 1)
    choose_left = np.abs(values - ref_times[left]) <= np.abs(values - ref_times[pos])
    return np.where(choose_left, left, pos).astype(int)


def align_pair(target, reference, alpha, beta):
    tt = target["time_s"]
    tr = reference["time_s"]
    mapped = alpha * tt + beta
    keep = (mapped >= tr[0]) & (mapped <= tr[-1])
    if int(keep.sum()) < max(MIN_MATCHES, int(math.ceil(MIN_TARGET_COVERAGE * len(tt)))):
        return None
    ti = np.flatnonzero(keep)
    ri = nearest_indices(mapped[keep], tr)
    span_fraction = float((mapped[keep].max() - mapped[keep].min()) / max(tr[-1] - tr[0], 1e-12))
    if span_fraction < MIN_REF_SPAN:
        return None
    is_pre_target = tt[ti] < 0.0
    is_post_target = tt[ti] > 0.0
    pre_target_n = int((tt < 0.0).sum())
    post_target_n = int((tt > 0.0).sum())
    pre_count = int(is_pre_target.sum())
    post_count = int(is_post_target.sum())

    def errors_for(mask):
        if not np.any(mask):
            return [0.0] * len(FEATURES), 0.0
        errors = []
        for col in FEATURES:
            x = target[col][ti[mask]]
            y = reference[col][ri[mask]]
            pooled = np.concatenate([target[col], reference[col]])
            scale = max(float(np.nanmax(pooled) - np.nanmin(pooled)), 1e-12)
            errors.append(float(np.nanmedian(np.abs(x - y)) / scale))
        return errors, float(np.mean(errors))

    pre_errors, pre_error = errors_for(is_pre_target)
    post_errors, post_error = errors_for(is_post_target)
    total_errors, total_error = errors_for(np.ones(len(ti), dtype=bool))
    pre_cov = float(pre_count / pre_target_n) if pre_target_n else 0.0
    post_cov = float(post_count / post_target_n) if post_target_n else float("nan")
    pre_ref = tr[tr < 0.0]
    pre_mapped = mapped[ti][is_pre_target]
    if len(pre_ref) >= 2 and len(pre_mapped) >= 2:
        pre_span_fraction = float((pre_mapped.max() - pre_mapped.min()) / max(pre_ref[-1] - pre_ref[0], 1e-12))
    else:
        pre_span_fraction = 0.0
    pre_quality = float(math.exp(-pre_error) * (0.5 + 0.5 * pre_cov) * (0.5 + 0.5 * min(1.0, pre_span_fraction))) if pre_count else 0.0
    post_quality = float(math.exp(-post_error) * (0.5 + 0.5 * post_cov)) if post_count else 1.0
    score = float(PREMERGER_WEIGHT * pre_quality + POSTMERGER_WEIGHT * post_quality)
    order_ok = bool(np.all(np.diff(ri) >= 0))
    return {
        "alpha": float(alpha),
        "beta": float(beta),
        "score": score,
        "feature_error": total_error,
        "frequency_error": total_errors[0],
        "width_error": total_errors[1],
        "coherence_error": total_errors[2],
        "persistence_error": total_errors[3],
        "premerger_feature_error": pre_error,
        "postmerger_feature_error": post_error,
        "premerger_frequency_error": pre_errors[0],
        "postmerger_frequency_error": post_errors[0],
        "premerger_node_count": pre_count,
        "postmerger_node_count": post_count,
        "premerger_coverage_fraction": pre_cov,
        "postmerger_coverage_fraction": post_cov,
        "premerger_reference_span_fraction": pre_span_fraction,
        "premerger_priority_score": pre_quality,
        "postmerger_extension_score": post_quality,
        "coverage": int(len(ti)),
        "coverage_fraction": float(len(ti) / len(tt)),
        "reference_span_fraction": span_fraction,
        "time_residual_median": float(np.median(np.abs(mapped[keep] - tr[ri]))),
        "order_ok": order_ok,
        "target_indices": ti,
        "reference_indices": ri,
        "mapped_time": mapped[keep],
    }


def best_pair(target, reference):
    best = None
    for alpha in ALPHAS:
        for beta in candidate_betas(target["time_s"], reference["time_s"], float(alpha)):
            cur = align_pair(target, reference, float(alpha), float(beta))
            if cur is None:
                continue
            key = (cur["premerger_priority_score"], cur["score"], cur["premerger_coverage_fraction"], cur["coverage_fraction"], cur["reference_span_fraction"], -abs(math.log(cur["alpha"])), -abs(cur["beta"]), -cur["alpha"], -cur["beta"])
            if best is None or key > best[0]:
                best = (key, cur)
    return best[1] if best else None


def _init_worker(paths):
    global _WORKER_PATHS
    _WORKER_PATHS = paths


def _best_pair_worker(pair):
    target, reference = pair
    cur = best_pair(_WORKER_PATHS[target], _WORKER_PATHS[reference])
    return target, reference, cur


def _edge_row(target, reference, cur, priority, paths):
    if cur is None:
        return {"EVENT_A": target, "EVENT_B": reference, "STATUS": "NO_VALID_AFFINE_ALIGNMENT", "CURRENT_END_ANCHORED_PRIORITY": priority.get((target, reference))}, None
    row = {
            "EVENT_A": target,
            "EVENT_B": reference,
            "STATUS": "VALID_AFFINE_ALIGNMENT",
            "ALPHA_A_TO_B": cur["alpha"],
            "BETA_A_TO_B": cur["beta"],
            "ALIGNMENT_SCORE": cur["score"],
            "FEATURE_ERROR": cur["feature_error"],
            "FREQUENCY_ERROR": cur["frequency_error"],
            "WIDTH_ERROR": cur["width_error"],
            "ROBUST_NETWORK_Z_ERROR": cur["coherence_error"],
            "PERSISTENCE_ERROR": cur["persistence_error"],
            "PREMERGER_FEATURE_ERROR": cur["premerger_feature_error"],
            "POSTMERGER_FEATURE_ERROR": cur["postmerger_feature_error"],
            "PREMERGER_MATCH_COUNT": cur["premerger_node_count"],
            "POSTMERGER_MATCH_COUNT": cur["postmerger_node_count"],
            "PREMERGER_COVERAGE_FRACTION": cur["premerger_coverage_fraction"],
            "POSTMERGER_COVERAGE_FRACTION": cur["postmerger_coverage_fraction"],
            "PREMERGER_REFERENCE_SPAN_FRACTION": cur["premerger_reference_span_fraction"],
            "PREMERGER_PRIORITY_SCORE": cur["premerger_priority_score"],
            "POSTMERGER_EXTENSION_SCORE": cur["postmerger_extension_score"],
            "MATCH_COUNT": cur["coverage"],
            "TARGET_NODE_COUNT": len(paths[target]["time_s"]),
            "REFERENCE_NODE_COUNT": len(paths[reference]["time_s"]),
            "TARGET_COVERAGE_FRACTION": cur["coverage_fraction"],
            "REFERENCE_SPAN_FRACTION": cur["reference_span_fraction"],
            "TIME_RESIDUAL_MEDIAN": cur["time_residual_median"],
            "ORDER_PRESERVED": cur["order_ok"],
            "CURRENT_END_ANCHORED_PRIORITY": priority.get((target, reference)),
        }
    edge = {**row, "target_indices": cur["target_indices"], "reference_indices": cur["reference_indices"], "mapped_time": cur["mapped_time"]}
    return row, edge


def edge_rows(paths, priority):
    events = sorted(paths)
    pairs = list(itertools.permutations(events, 2))
    rows = []
    edges = {}
    total = len(pairs)
    done = 0
    print(f"GLOBAL_WORKERS={MAX_WORKERS} NESTED_POOL=False NUMERICAL_THREADS=1", flush=True)
    with ProcessPoolExecutor(max_workers=MAX_WORKERS, initializer=_init_worker, initargs=(paths,)) as pool:
        futures = [pool.submit(_best_pair_worker, pair) for pair in pairs]
        for fut in as_completed(futures):
            target, reference, cur = fut.result()
            row, edge = _edge_row(target, reference, cur, priority, paths)
            rows.append(row)
            if edge is not None:
                edges[(target, reference)] = edge
            done += 1
            if done % 200 == 0:
                print(f"GLOBAL_PROGRESS={done}/{total} EDGE_PAIRS ETA=estimating PREMERGER_PRIORITY=True ACTIVE_WORKERS={MAX_WORKERS}", flush=True)
    rows.sort(key=lambda r: (str(r.get("EVENT_A")), str(r.get("EVENT_B"))))
    return pd.DataFrame(rows), edges


def reciprocal_audit(edges):
    rows = []
    for a, b in sorted({tuple(sorted(k)) for k in edges if tuple(reversed(k)) in edges}):
        eab, eba = edges[(a, b)], edges[(b, a)]
        aa, ba = float(eab["ALPHA_A_TO_B"]), float(eab["BETA_A_TO_B"])
        ab, bb = float(eba["ALPHA_A_TO_B"]), float(eba["BETA_A_TO_B"])
        scale_resid = math.log(aa * ab)
        back = ab * (aa * eab["mapped_time"] + ba) + bb
        time_resid = float(np.median(np.abs(back - eab["mapped_time"])))
        rows.append({"EVENT_A": a, "EVENT_B": b, "ALPHA_A_TO_B": aa, "BETA_A_TO_B": ba, "ALPHA_B_TO_A": ab, "BETA_B_TO_A": bb, "LOG_RECIPROCAL_SCALE_RESIDUAL": scale_resid, "RECIPROCAL_TIME_RESIDUAL_MEDIAN": time_resid, "RECIPROCAL_SCALE_OK_TOL_1P5": abs(scale_resid) <= LOG_SCALE_TOL})
    return pd.DataFrame(rows)


def triad_audit(edges, paths):
    events = sorted(paths)
    rows = []
    for a, b, c in itertools.permutations(events, 3):
        eab, ebc, eac = edges.get((a, b)), edges.get((b, c)), edges.get((a, c))
        if eab is None or ebc is None or eac is None:
            continue
        a1, b1 = float(eab["ALPHA_A_TO_B"]), float(eab["BETA_A_TO_B"])
        a2, b2 = float(ebc["ALPHA_A_TO_B"]), float(ebc["BETA_A_TO_B"])
        a3, b3 = float(eac["ALPHA_A_TO_B"]), float(eac["BETA_A_TO_B"])
        scale_resid = math.log(a3) - math.log(a2 * a1)
        beta_expected = a2 * b1 + b2
        beta_resid = b3 - beta_expected
        node_errs = []
        exact = 0
        within = 0
        tt_a, tt_c = paths[a]["time_s"], paths[c]["time_s"]
        tt_b = paths[b]["time_s"]
        direct = a3 * tt_a + b3
        keep = (direct >= tt_c[0]) & (direct <= tt_c[-1])
        if keep.any():
            ia = np.flatnonzero(keep)
            ib_time = a1 * tt_a[ia] + b1
            ib = nearest_indices(ib_time, tt_b)
            composed = a2 * tt_b[ib] + b2
            ic_direct = nearest_indices(direct[ia], tt_c)
            ic_comp = nearest_indices(composed, tt_c)
            for x, y in zip(ic_direct, ic_comp):
                err = abs(int(x) - int(y)) / max(1, len(tt_c) - 1)
                node_errs.append(err)
                exact += int(x == y)
                within += int(err <= NODE_INDEX_TOL)
        rows.append({"EVENT_A": a, "EVENT_B": b, "EVENT_C": c, "ALPHA_AB": a1, "ALPHA_BC": a2, "ALPHA_AC": a3, "BETA_AB": b1, "BETA_BC": b2, "BETA_AC": b3, "LOG_SCALE_COMPOSITION_RESIDUAL": scale_resid, "OFFSET_COMPOSITION_RESIDUAL": beta_resid, "SCALE_COMPOSITION_OK_TOL_1P5": abs(scale_resid) <= LOG_SCALE_TOL, "NODE_COMPOSITION_COUNT": len(node_errs), "NODE_COMPOSITION_EXACT_FRACTION": exact / len(node_errs) if node_errs else np.nan, "NODE_COMPOSITION_WITHIN_025_FRACTION": within / len(node_errs) if node_errs else np.nan, "NODE_COMPOSITION_MEDIAN_NORMALIZED_INDEX_ERROR": float(np.median(node_errs)) if node_errs else np.nan})
    return pd.DataFrame(rows)


def components(edges):
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    seen = set(); out = []
    for root in sorted(adj):
        if root in seen: continue
        q = deque([root]); seen.add(root); comp = []
        while q:
            u = q.popleft(); comp.append(u)
            for v in sorted(adj[u]):
                if v not in seen: seen.add(v); q.append(v)
        out.append(sorted(comp))
    return out


def global_affine_coordinate(edges):
    comps = components(edges)
    rows, comp_rows = [], []
    for ci, comp in enumerate(comps):
        idx = {e: i for i, e in enumerate(comp)}
        rel = [(u, v, r) for (u, v), r in edges.items() if u in idx and v in idx]
        A = []; y = []
        for u, v, r in rel:
            row = np.zeros(len(comp)); row[idx[v]] = 1; row[idx[u]] = -1
            A.append(row); y.append(math.log(float(r["ALPHA_A_TO_B"])))
        anchor = np.zeros(len(comp)); anchor[0] = 1; A.append(anchor); y.append(0.0)
        log_a = np.linalg.lstsq(np.asarray(A), np.asarray(y), rcond=None)[0]
        A2 = []; y2 = []
        for u, v, r in rel:
            row = np.zeros(len(comp)); row[idx[v]] = 1; row[idx[u]] = -float(r["ALPHA_A_TO_B"])
            A2.append(row); y2.append(float(r["BETA_A_TO_B"]))
        anchor2 = np.zeros(len(comp)); anchor2[0] = 1; A2.append(anchor2); y2.append(0.0)
        offset = np.linalg.lstsq(np.asarray(A2), np.asarray(y2), rcond=None)[0]
        comp_rows.append({"COMPONENT_ID": ci, "N_EVENTS": len(comp), "N_EDGES": len(rel), "EVENTS": "|".join(comp)})
        for u, v, r in rel:
            pred_scale = log_a[idx[v]] - log_a[idx[u]]
            pred_offset = offset[idx[v]] - float(r["ALPHA_A_TO_B"]) * offset[idx[u]]
            rows.append({"COMPONENT_ID": ci, "EVENT_A": u, "EVENT_B": v, "LOG_ALPHA_OBSERVED": math.log(float(r["ALPHA_A_TO_B"])), "LOG_ALPHA_COORDINATE": pred_scale, "GLOBAL_SCALE_RESIDUAL": math.log(float(r["ALPHA_A_TO_B"])) - pred_scale, "BETA_OBSERVED": float(r["BETA_A_TO_B"]), "BETA_COORDINATE": pred_offset, "GLOBAL_OFFSET_RESIDUAL": float(r["BETA_A_TO_B"]) - pred_offset})
    return pd.DataFrame(rows), pd.DataFrame(comp_rows)


def describe(df):
    if len(df) == 0: return {"N": 0}
    def q(col, p):
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        return float(s.quantile(p)) if len(s) else None
    return {"N": int(len(df)), "MEDIAN": q("LOG_RECIPROCAL_SCALE_RESIDUAL" if "LOG_RECIPROCAL_SCALE_RESIDUAL" in df else "LOG_SCALE_COMPOSITION_RESIDUAL", .5), "Q05": q("LOG_RECIPROCAL_SCALE_RESIDUAL" if "LOG_RECIPROCAL_SCALE_RESIDUAL" in df else "LOG_SCALE_COMPOSITION_RESIDUAL", .05), "Q95": q("LOG_RECIPROCAL_SCALE_RESIDUAL" if "LOG_RECIPROCAL_SCALE_RESIDUAL" in df else "LOG_SCALE_COMPOSITION_RESIDUAL", .95), "WITHIN_TOL": float(df["RECIPROCAL_SCALE_OK_TOL_1P5"].mean()) if "RECIPROCAL_SCALE_OK_TOL_1P5" in df else float(df["SCALE_COMPOSITION_OK_TOL_1P5"].mean())}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if not COHORT_FILE.exists(): raise FileNotFoundError(COHORT_FILE)
    if not FROZEN_PATH_ROOT.exists(): raise FileNotFoundError(FROZEN_PATH_ROOT)
    paths, manifest, cohort_events = load_nodes()
    priority = load_priority()
    manifest["MORPHOLOGY_INPUT_USED"] = False
    manifest.to_csv(OUT / "FULL_WINDOW_NODE_SUPPORT_MANIFEST.csv", index=False)
    edges_df, edges = edge_rows(paths, priority)
    edges_df.to_csv(OUT / "FULL_WINDOW_PAIRWISE_BEST_EDGES.csv", index=False)
    reciprocal = reciprocal_audit(edges)
    reciprocal.to_csv(OUT / "FULL_WINDOW_RECIPROCAL_AUDIT.csv", index=False)
    triads = triad_audit(edges, paths)
    with gzip.open(OUT / "FULL_WINDOW_TRIAD_COMPOSITION_AUDIT.csv.gz", "wt", encoding="utf-8", newline="") as f:
        triads.to_csv(f, index=False)
    global_df, comps = global_affine_coordinate(edges)
    global_df.to_csv(OUT / "FULL_WINDOW_GLOBAL_AFFINE_COORDINATE_AUDIT.csv", index=False)
    comps.to_csv(OUT / "FULL_WINDOW_COORDINATE_COMPONENTS.csv", index=False)

    rec_ok = float(reciprocal["RECIPROCAL_SCALE_OK_TOL_1P5"].mean()) if len(reciprocal) else 0.0
    tri_ok = float(triads["SCALE_COMPOSITION_OK_TOL_1P5"].mean()) if len(triads) else 0.0
    node_d = triads[triads["NODE_COMPOSITION_COUNT"] > 0]
    node_ok = float(node_d["NODE_COMPOSITION_WITHIN_025_FRACTION"].median()) if len(node_d) else 0.0
    largest = int(comps["N_EVENTS"].max()) if len(comps) else 0
    coordinate_status = "FULL_WINDOW_ONE_COORDINATE_DESCRIPTIVELY_COMPATIBLE" if largest >= math.ceil(.8 * len(paths)) and rec_ok >= .5 and tri_ok >= .5 and node_ok >= .5 else "FULL_WINDOW_PAIRWISE_NETWORK_REMAINS_INCONSISTENT"
    node_rows = int(sum(len(p["time_s"]) for p in paths.values()))
    time_min = float(min(p["time_s"].min() for p in paths.values()))
    time_max = float(max(p["time_s"].max() for p in paths.values()))
    status = {"R_STATUS": "PASS", "STAGE": "RIUD_DEV99_PREMERGER_PRIORITY_NODE_SUPPORT_SCALE_ALIGNMENT_R1", "COHORT_FILE": str(COHORT_FILE), "FROZEN_PATH_ROOT": str(FROZEN_PATH_ROOT), "PATH_FILENAME": PATH_FILENAME, "EVENTS": len(paths), "COHORT_EVENTS": len(cohort_events), "NODE_ROWS": node_rows, "TIME_SUPPORT_MIN_S": time_min, "TIME_SUPPORT_MAX_S": time_max, "EXPECTED_SUPPORT_WINDOW_S": [-0.12, 0.03], "TIME_ZERO_ANCHOR_USED": False, "AFFINE_RULE": "t_reference=alpha*t_target+beta; alpha>0; no reversal", "ALPHA_GRID": [float(x) for x in ALPHAS], "OFFSET_RULE": "all deterministic node-to-node offsets for each alpha", "PREMERGER_PRIORITY": True, "PREMERGER_WEIGHT": PREMERGER_WEIGHT, "POSTMERGER_WEIGHT": POSTMERGER_WEIGHT, "FEATURES_USED": FEATURES, "CURRENT_RESULT_PRIORITY_USED_FOR_AUDIT_ORDER_ONLY": True, "RECIPROCAL_METRICS": describe(reciprocal), "TRIAD_METRICS": describe(triads), "NODE_COMPOSITION_MEDIAN_WITHIN_025": node_ok, "LARGEST_COORDINATE_COMPONENT": largest, "N_COMPONENTS": int(len(comps)), "GLOBAL_HIDDEN_COORDINATE_STATUS": coordinate_status, "MORPHOLOGY_INPUT_USED": False, "NODE_COUNT_AS_EXPLANATORY_INPUT": False, "NEW_PATH_SEARCH": False, "NEW_LAW_FIT": False, "NEW_NULL": False, "HOLDOUT10_READ": False, "HOLDOUT30_READ": False, "HOLDOUT40_READ": False, "FINAL_FREEZE": False, "NEXT": "USER_REVIEW_PREMERGER_PRIORITY_ALIGNMENT"}
    (OUT / "R_STATUS.json").write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = ["STAGE=RIUD_DEV99_PREMERGER_PRIORITY_NODE_SUPPORT_SCALE_ALIGNMENT_R1", "R_STATUS=PASS", f"EVENTS={len(paths)}", f"NODE_ROWS={node_rows}", f"TIME_SUPPORT_S={time_min}..{time_max}", "EXPECTED_SUPPORT_WINDOW_S=-0.12..0.03", "TIME_ZERO_ANCHOR_USED=False", "PREMERGER_PRIORITY=True", f"PREMERGER_WEIGHT={PREMERGER_WEIGHT}", f"POSTMERGER_WEIGHT={POSTMERGER_WEIGHT}", f"RECIPROCAL_SCALE_SUPPORT={json.dumps(describe(reciprocal))}", f"TRIAD_SCALE_COMPOSITION_SUPPORT={json.dumps(describe(triads))}", f"NODE_COMPOSITION_MEDIAN_WITHIN_025={node_ok}", f"LARGEST_COORDINATE_COMPONENT={largest}", f"GLOBAL_HIDDEN_COORDINATE_STATUS={coordinate_status}", "CURRENT_RESULT_PRIORITY_USED_FOR_AUDIT_ORDER_ONLY=True", "MORPHOLOGY_INPUT_USED=False", "NODE_COUNT_AS_EXPLANATORY_INPUT=False", "NEW_PATH_SEARCH=False", "NEW_LAW_FIT=False", "NEW_NULL=False", "HOLDOUT10_READ=False", "HOLDOUT30_READ=False", "HOLDOUT40_READ=False", "FINAL_FREEZE=False", "NEXT=USER_REVIEW_PREMERGER_PRIORITY_ALIGNMENT"]
    (OUT / "SEND_TO_CHAT.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    hashes = []
    for f in sorted(OUT.iterdir()):
        if f.name == "SHA256SUMS.txt" or not f.is_file(): continue
        hashes.append(f"{sha256_file(f)}  {f.name}")
    (OUT / "SHA256SUMS.txt").write_text("\n".join(hashes) + "\n", encoding="utf-8")
    print(json.dumps({"OUT": str(OUT), "EVENTS": len(paths), "NODE_ROWS": node_rows, "TIME": [time_min, time_max], "RECIPROCAL": describe(reciprocal), "TRIADS": describe(triads), "NODE_WITHIN_025": node_ok, "COMPONENT": largest, "STATUS": coordinate_status}, indent=2))


if __name__ == "__main__":
    main()
