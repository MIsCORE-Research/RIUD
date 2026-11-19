import os, csv, ast, inspect, traceback, time, statistics, math
from pathlib import Path
from collections import Counter

ROOT=Path("/mnt/c/Users/민재현/Desktop/prism")
A2_SRC=ROOT/"PRISM_2P5A2_SELECTED29_4S_PRISM_SMOKE_REPLAY_20260709/RUN_2P5A2_SELECTED29_4S_PRISM_SMOKE.py"
INVENTORY=ROOT/"PRISM_2P5B7B_FULL_LOCAL_4S_NATIVE_BASELINE_PREP_20260709/01_inventory/PRISM_2P5B7B_FULL_LOCAL_4S_EVENT_INVENTORY.csv"
B5B=ROOT/"PRISM_2P5B5B_CLEAN_PRIORITY_LOCK_20260709/01_tables/PRISM_2P5B5B_CLEAN_PRIORITY_LEDGER.csv"
OUT=ROOT/"PRISM_2P5B7B1_FULL_LOCAL_4S_NATIVE_BASELINE_RUN_20260709"

RESULTS=OUT/"01_results/PRISM_2P5B7B1_FULL_LOCAL_NATIVE_BASELINE_RESULTS.csv"
EVENT_SUMMARY=OUT/"01_results/PRISM_2P5B7B1_EVENT_LEVEL_BEST_SUMMARY.csv"
REPORT=OUT/"03_reports/PRISM_2P5B7B1_FULL_LOCAL_NATIVE_BASELINE_REPORT.txt"
SEND=OUT/"send/SEND_TO_CHAT.txt"
STATUS=OUT/"03_reports/PRISM_2P5B7B1_STATUS.tsv"

for d in ["01_results","02_logs","03_reports","send"]:
    (OUT/d).mkdir(parents=True,exist_ok=True)

def read_csv(p):
    with open(p,newline="",encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def fnum(x):
    try:
        s=str(x).strip().replace(",","")
        if s in ["","--","nan","None","NA"]:
            return None
        return float(s)
    except Exception:
        return None

def clean_nums(xs):
    return [x for x in xs if x is not None and not (isinstance(x,float) and math.isnan(x))]

def pct_rank(score, scores):
    scores=clean_nums(scores)
    if score is None or not scores:
        return None
    return sum(1 for x in scores if x <= score)/len(scores)

def qtile(xs,q):
    xs=sorted(clean_nums(xs))
    if not xs:
        return None
    if len(xs)==1:
        return xs[0]
    pos=(len(xs)-1)*q
    lo=math.floor(pos)
    hi=math.ceil(pos)
    if lo==hi:
        return xs[lo]
    return xs[lo]*(hi-pos)+xs[hi]*(pos-lo)

# ------------------------------------------------------------
# Load A2 scorer safely: imports + top-level assigns + functions only.
# This avoids executing selected29 hardcoded loop.
# ------------------------------------------------------------
src=A2_SRC.read_text(encoding="utf-8",errors="ignore")
tree=ast.parse(src)

allowed=[]
for node in tree.body:
    if isinstance(node,(ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign, ast.FunctionDef)):
        allowed.append(node)

mod=ast.Module(body=allowed, type_ignores=[])
ast.fix_missing_locations(mod)

ns={"__file__":str(A2_SRC)}
exec(compile(mod, str(A2_SRC), "exec"), ns)

event_best=ns.get("event_best")
if event_best is None:
    raise RuntimeError("A2 event_best function not found")

sig=inspect.signature(event_best)
param_names=list(sig.parameters.keys())

def call_event_best(event, path, inv_row):
    """
    Try to call A2 event_best robustly.
    Supports common forms:
    - event_best(path)
    - event_best(event, path)
    - event_best(row)
    """
    tries=[]
    if len(param_names)==1:
        name=param_names[0].lower()
        if "row" in name or name in ["r","rec","record"]:
            tries.append((inv_row,))
        elif "event" in name or name in ["ev"]:
            tries.append((event,))
        else:
            tries.append((path,))
            tries.append((inv_row,))
    elif len(param_names)==2:
        tries.append((event,path))
        tries.append((path,event))
        tries.append((inv_row,path))
    elif len(param_names)==3:
        tries.append((event,path,inv_row))
    else:
        tries.append((path,))

    last=None
    for args in tries:
        try:
            return event_best(*args)
        except Exception as e:
            last=e
    raise last

def normalize_result(res):
    """
    Convert A2 return value into standard columns.
    """
    out={
        "status":"OK",
        "best_score":None,
        "best_f_hz":None,
        "best_width_s":None,
        "best_center_s":None,
        "raw_amp":None,
        "verdict":"",
        "raw_return_repr":"",
    }
    out["raw_return_repr"]=repr(res)[:500]

    if isinstance(res, dict):
        for k in list(out.keys()):
            if k in res:
                out[k]=res[k]
        # possible aliases
        aliases={
            "best_score":["score","native_score","z","zscore"],
            "best_f_hz":["f","freq","frequency","f0","best_f"],
            "best_width_s":["width","best_width"],
            "best_center_s":["center","best_center"],
            "raw_amp":["amp","raw","amplitude"],
            "verdict":["band","class"],
        }
        for ok,alts in aliases.items():
            if out.get(ok) in [None,""]:
                for a in alts:
                    if a in res:
                        out[ok]=res[a]
                        break
        return out

    if isinstance(res,(list,tuple)):
        vals=list(res)
        # A2 likely returns: best_score, best_f, best_width, best_center, raw_amp
        if len(vals)>=1: out["best_score"]=vals[0]
        if len(vals)>=2: out["best_f_hz"]=vals[1]
        if len(vals)>=3: out["best_width_s"]=vals[2]
        if len(vals)>=4: out["best_center_s"]=vals[3]
        if len(vals)>=5: out["raw_amp"]=vals[4]
        if len(vals)>=6: out["verdict"]=str(vals[5])
        return out

    # single numeric
    try:
        out["best_score"]=float(res)
    except Exception:
        out["status"]="UNKNOWN_RETURN"
    return out

def score_band(x):
    x=fnum(x)
    if x is None:
        return "NO_SCORE"
    if x>=8:
        return "VERY_STRONG"
    if x>=5:
        return "STRONG"
    if x>=2.5:
        return "PASS"
    return "FAIL"

# labels from B5B
labels={}
for r in read_csv(B5B):
    ev=r.get("event","").strip()
    if ev:
        labels[ev]=r

inventory=read_csv(INVENTORY)

result_rows=[]
summary_rows=[]
status_rows=[]

start_all=time.time()

print("RUNTIME_START_B7B1")
print("A2_SRC=", A2_SRC)
print("INVENTORY=", INVENTORY)
print("N_EVENTS=", len(inventory))
print("EVENT_BEST_SIGNATURE=", str(sig), "params=", param_names)

with open(STATUS,"w",encoding="utf-8") as sf:
    sf.write("event\tstatus\tseconds\tn_paths\tbest_score\n")

for idx,row in enumerate(inventory,1):
    ev=row.get("event","").strip()
    paths=[p for p in str(row.get("local_paths","")).split(";") if p.strip()]
    t0=time.time()

    print(f"===== EVENT {idx}/{len(inventory)} {ev} paths={len(paths)} =====", flush=True)

    ev_path_rows=[]
    for p_i,path in enumerate(paths,1):
        rr={
            "event":ev,
            "path_rank":p_i,
            "path":path,
            "path_status":"INIT",
            "best_score":"",
            "best_f_hz":"",
            "best_width_s":"",
            "best_center_s":"",
            "raw_amp":"",
            "score_band":"",
            "verdict":"",
            "error":"",
            "raw_return_repr":"",
        }
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(path)
            res=call_event_best(ev,path,row)
            nr=normalize_result(res)
            rr["path_status"]=nr.get("status","OK") or "OK"
            rr["best_score"]=nr.get("best_score")
            rr["best_f_hz"]=nr.get("best_f_hz")
            rr["best_width_s"]=nr.get("best_width_s")
            rr["best_center_s"]=nr.get("best_center_s")
            rr["raw_amp"]=nr.get("raw_amp")
            rr["verdict"]=nr.get("verdict","")
            rr["score_band"]=score_band(rr["best_score"])
            rr["raw_return_repr"]=nr.get("raw_return_repr","")
        except Exception as e:
            rr["path_status"]="FAIL"
            rr["error"]=repr(e)
            rr["raw_return_repr"]=traceback.format_exc()[-800:]
        result_rows.append(rr)
        ev_path_rows.append(rr)

    scored=[r for r in ev_path_rows if fnum(r.get("best_score")) is not None]
    if scored:
        best=max(scored, key=lambda r:fnum(r.get("best_score")))
        ev_status="OK"
    else:
        best=ev_path_rows[0] if ev_path_rows else {}
        ev_status="NO_SCORE"

    lab=labels.get(ev,{})
    sec=time.time()-t0

    summary={
        "event":ev,
        "event_status":ev_status,
        "n_paths":len(paths),
        "n_scored_paths":len(scored),
        "best_score":best.get("best_score",""),
        "best_f_hz":best.get("best_f_hz",""),
        "best_width_s":best.get("best_width_s",""),
        "best_center_s":best.get("best_center_s",""),
        "best_path":best.get("path",""),
        "score_band":score_band(best.get("best_score","")),
        "b5b_priority":row.get("b5b_priority",""),
        "b5b_score":row.get("b5b_score",""),
        "network_snr":row.get("network_snr",""),
        "distance_mpc":row.get("distance_mpc",""),
        "q":row.get("q",""),
        "mass1":row.get("mass1",""),
        "mass2":row.get("mass2",""),
        "chi_eff":row.get("chi_eff",""),
        "run":row.get("run",""),
        "release":row.get("release",""),
        "seconds":round(sec,3),
    }
    summary_rows.append(summary)

    with open(STATUS,"a",encoding="utf-8") as sf:
        sf.write(f"{ev}\t{ev_status}\t{sec:.3f}\t{len(paths)}\t{summary['best_score']}\n")

    print(f"EVENT_DONE {ev} status={ev_status} best={summary['best_score']} band={summary['score_band']} seconds={sec:.2f}", flush=True)

    # checkpoint every 25 events
    if idx % 25 == 0:
        with open(EVENT_SUMMARY,"w",newline="",encoding="utf-8") as f:
            cols=list(summary_rows[0].keys())
            w=csv.DictWriter(f,fieldnames=cols)
            w.writeheader()
            w.writerows(summary_rows)

# write path-level results
with open(RESULTS,"w",newline="",encoding="utf-8") as f:
    cols=list(result_rows[0].keys()) if result_rows else ["event"]
    w=csv.DictWriter(f,fieldnames=cols)
    w.writeheader()
    w.writerows(result_rows)

# event-level summary
scores=clean_nums([fnum(r.get("best_score")) for r in summary_rows])
for r in summary_rows:
    s=fnum(r.get("best_score"))
    r["full_baseline_percentile_leq"]=pct_rank(s,scores)
    r["full_baseline_rank_desc"]=""
ranked=sorted([r for r in summary_rows if fnum(r.get("best_score")) is not None], key=lambda r:fnum(r.get("best_score")), reverse=True)
for i,r in enumerate(ranked,1):
    r["full_baseline_rank_desc"]=i

with open(EVENT_SUMMARY,"w",newline="",encoding="utf-8") as f:
    cols=list(summary_rows[0].keys())
    w=csv.DictWriter(f,fieldnames=cols)
    w.writeheader()
    w.writerows(summary_rows)

cnt_band=Counter(r["score_band"] for r in summary_rows)
cnt_priority=Counter(r["b5b_priority"] for r in summary_rows)
cnt_status=Counter(r["event_status"] for r in summary_rows)

# selected priority top/ranks
selected_rows=[r for r in summary_rows if r["b5b_priority"] in ["P1","P2","CONTROL","NEGATIVE_CONTROL","ANCHOR","UNTESTED"]]
p1_rows=[r for r in summary_rows if r["b5b_priority"]=="P1"]
p2_rows=[r for r in summary_rows if r["b5b_priority"]=="P2"]

with open(REPORT,"w",encoding="utf-8") as f:
    f.write("PRISM 2.5B7B1 FULL LOCAL 4S NATIVE BASELINE RUN\n")
    f.write("============================================================\n\n")
    f.write("Purpose:\n")
    f.write("- Run A2-native scorer logic over all local 4s events.\n")
    f.write("- Establish full baseline distribution for selected36/P1/P2.\n\n")
    f.write(f"A2_SRC={A2_SRC}\n")
    f.write(f"EVENT_BEST_SIGNATURE={sig}\n")
    f.write(f"TOTAL_EVENTS={len(summary_rows)}\n")
    f.write(f"PATH_LEVEL_ROWS={len(result_rows)}\n")
    f.write(f"TOTAL_SECONDS={time.time()-start_all:.2f}\n\n")

    f.write("Event status counts:\n")
    for k,v in sorted(cnt_status.items()):
        f.write(f"- {k}: {v}\n")
    f.write("\nScore band counts:\n")
    for k,v in sorted(cnt_band.items()):
        f.write(f"- {k}: {v}\n")
    f.write("\nB5B priority counts in full baseline:\n")
    for k,v in sorted(cnt_priority.items()):
        f.write(f"- {k}: {v}\n")

    f.write("\nScore distribution:\n")
    f.write(f"- n={len(scores)}\n")
    f.write(f"- median={statistics.median(scores) if scores else ''}\n")
    f.write(f"- q90={qtile(scores,0.90)}\n")
    f.write(f"- q95={qtile(scores,0.95)}\n")
    f.write(f"- q99={qtile(scores,0.99)}\n")
    f.write(f"- max={max(scores) if scores else ''}\n")

    f.write("\nTop 40 full baseline events:\n")
    for r in ranked[:40]:
        f.write(
            f"- rank={r['full_baseline_rank_desc']} {r['event']} "
            f"score={r['best_score']} band={r['score_band']} "
            f"priority={r['b5b_priority']} f={r['best_f_hz']} w={r['best_width_s']} "
            f"snr={r['network_snr']} dist={r['distance_mpc']} q={r['q']} "
            f"pct={r['full_baseline_percentile_leq']}\n"
        )

    f.write("\nP1/P2 ranks:\n")
    for r in sorted(p1_rows+p2_rows, key=lambda x: fnum(x.get("best_score")) or -999, reverse=True):
        f.write(
            f"- {r['b5b_priority']} {r['event']} rank={r['full_baseline_rank_desc']} "
            f"score={r['best_score']} pct={r['full_baseline_percentile_leq']} "
            f"f={r['best_f_hz']} w={r['best_width_s']}\n"
        )

    f.write("\nLocked verdict:\n")
    f.write("PRISM_2P5B7B1_FULL_LOCAL_NATIVE_BASELINE_RUN_DONE__REVIEW_PERCENTILES_NEXT\n")

with open(SEND,"w",encoding="utf-8") as f:
    f.write("R_STATUS=PRISM_2P5B7B1_FULL_LOCAL_NATIVE_BASELINE_RUN_DONE\n")
    f.write(f"OUT={OUT}\n")
    f.write(f"RESULTS={RESULTS}\n")
    f.write(f"EVENT_SUMMARY={EVENT_SUMMARY}\n")
    f.write(f"REPORT={REPORT}\n")
    f.write(f"STATUS={STATUS}\n")
    f.write(f"TOTAL_EVENTS={len(summary_rows)}\n")
    f.write(f"PATH_LEVEL_ROWS={len(result_rows)}\n")

    f.write("\n===== EVENT STATUS COUNTS =====\n")
    for k,v in sorted(cnt_status.items()):
        f.write(f"{k}={v}\n")

    f.write("\n===== SCORE BAND COUNTS =====\n")
    for k,v in sorted(cnt_band.items()):
        f.write(f"{k}={v}\n")

    f.write("\n===== SCORE DISTRIBUTION =====\n")
    f.write(f"N_SCORED={len(scores)}\n")
    f.write(f"MEDIAN={statistics.median(scores) if scores else ''}\n")
    f.write(f"Q90={qtile(scores,0.90)}\n")
    f.write(f"Q95={qtile(scores,0.95)}\n")
    f.write(f"Q99={qtile(scores,0.99)}\n")
    f.write(f"MAX={max(scores) if scores else ''}\n")

    f.write("\n===== TOP 40 FULL BASELINE =====\n")
    for r in ranked[:40]:
        f.write(
            f"rank={r['full_baseline_rank_desc']}\t{r['event']}"
            f"\tscore={r['best_score']}\tband={r['score_band']}"
            f"\tpriority={r['b5b_priority']}\tf={r['best_f_hz']}\tw={r['best_width_s']}"
            f"\tsnr={r['network_snr']}\tdist={r['distance_mpc']}\tq={r['q']}"
            f"\tpct={r['full_baseline_percentile_leq']}\n"
        )

    f.write("\n===== P1 P2 FULL BASELINE RANKS =====\n")
    for r in sorted(p1_rows+p2_rows, key=lambda x: fnum(x.get("best_score")) or -999, reverse=True):
        f.write(
            f"{r['b5b_priority']}\t{r['event']}"
            f"\trank={r['full_baseline_rank_desc']}"
            f"\tscore={r['best_score']}"
            f"\tpct={r['full_baseline_percentile_leq']}"
            f"\tf={r['best_f_hz']}\tw={r['best_width_s']}"
            f"\tsnr={r['network_snr']}\tdist={r['distance_mpc']}\tq={r['q']}\n"
        )

    f.write("\nLOCKED_VERDICT=PRISM_2P5B7B1_FULL_LOCAL_NATIVE_BASELINE_RUN_DONE__REVIEW_PERCENTILES_NEXT\n")

print(open(SEND,encoding="utf-8").read())
