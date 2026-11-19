
import ast
import hashlib
import importlib.util
import json
import math
import os
import re
import sys
import traceback
import types
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

STAGE="RIUD_R26C42G_EXACT_SELECTOR_AWARE_COMPLEX_PHASE_NULL_R8_EVENTWISE_TAU_FRAME_EQUIVALENCE_20260801"
PRISM=Path("/mnt/c/Users/민재현/Desktop/prism")
HERE=Path(__file__).resolve().parent
OUT=HERE/"output"
WORK=HERE/"work"
LOGS=HERE/"logs"
for p in (OUT,WORK,LOGS):
    p.mkdir(exist_ok=True)

R6=PRISM/"RIUD_R26C42F1_OFFSOURCE_CONTROL_ASSET_EXACT_RESOLUTION_R6_13EVENT_PARALLEL_HARDBIND_20260801"
R6_LOCK=R6/"output"/"EVENT_CONTROL_ASSET_LOCK.csv"

C42C=PRISM/"RIUD_R26C42C_FROZEN_REALDATA_DIRECT_COMPLEX_PHASE_STACK_R0_20260801"
C42C_SUM=C42C/"output"/"FINAL_SUMMARY.csv"

R36=PRISM/"RIUD_R26C36_RAW_FIXED_PATH_COHERENT_STACK_NOTCH_AUDIT_R2_20260731"
LOCK_ROOT=R36/"work"/"residual_locks"

DYNAMIC_ROOTS=[
    PRISM/"RIUD_R26C26B1_FAILED4_STRICT_COORD_MATCH_AND_16EVENT_MERGE_20260728",
    PRISM/"RIUD_R26C26A_11EVENT_FULL_DYNAMIC_NULL_FAMILY_SEARCH_R0_20260728",
]

EVENTS=[
"GW150914_095045","GW200129_065458","GW200224_222234","GW230824_033047",
"GW230831_015414","GW230904_051013","GW231206_233901","GW231221_135041",
"GW240629_145256","GW240919_061559","GW240920_124024","GW241006_015333",
"GW241231_054133"]

CANONICAL_ENGINE=(
    PRISM/
    "RIUD_R26C12R4_CANONICAL_13EVENT_MERGER_M120_P30_W5_20260728"/
    "engine"/
    "scripts"/
    "run_original_engine_wide5.py"
)

EVENT_WORKERS=13
CONTROL_THREADS_PER_EVENT=2
NULL_WORKERS=13
NULL_DRAWS=100000
BASE_SEED=4260001

EXPECTED_OBSERVED_REAL=0.3671572579932161
EXPECTED_OBSERVED_RESULTANT=0.36770363942899376
EXPECTED_OBSERVED_PHASE=0.05452149970951159

def say(x):
    print(x,flush=True)

def atomic_csv(df,path):
    path=Path(path)
    tmp=path.with_suffix(path.suffix+".tmp")
    df.to_csv(tmp,index=False)
    os.replace(tmp,path)

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()

def numeric_controls(d):
    pairs=[]
    for p in Path(d).glob("control_*.npz"):
        m=re.fullmatch(r"control_(\d+)\.npz",p.name)
        if m:
            pairs.append((int(m.group(1)),p))
    pairs.sort(key=lambda x:x[0])
    return pairs

def literal_assignments(tree):
    vals={}
    for node in tree.body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            try:
                vals[node.targets[0].id]=ast.literal_eval(node.value)
            except Exception:
                pass
        elif isinstance(node,ast.AnnAssign) and isinstance(node.target,ast.Name):
            try:
                vals[node.target.id]=ast.literal_eval(node.value)
            except Exception:
                pass
    return vals

def safe_function_module(path,name):
    text=Path(path).read_text(encoding="utf-8",errors="replace")
    tree=ast.parse(text)
    keep=[]
    for node in tree.body:
        if isinstance(node,(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
            keep.append(node)
    mod=types.ModuleType(name)
    mod.__file__=str(path)
    exec(compile(ast.Module(body=keep,type_ignores=[]),str(path),"exec"),mod.__dict__)
    for k,v in literal_assignments(tree).items():
        mod.__dict__.setdefault(k,v)
    return mod,text,literal_assignments(tree)

def full_import(path,name):
    spec=importlib.util.spec_from_file_location(name,str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"IMPORT_SPEC_FAIL={path}")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def resolve_dynamic_source():
    # No project-wide recursion. R26C26B1 is the authoritative/latest dynamic-null source.
    root=DYNAMIC_ROOTS[0]
    if not root.exists():
        raise RuntimeError(f"DYNAMIC_ROOT_MISSING={root}")

    fixed_candidates=[
        root/"run.py",
        root/"RUN.py",
        root/"scripts"/"run.py",
        root/"scripts"/"run_dynamic_null.py",
    ]
    candidates=[]
    for p in fixed_candidates:
        if p.is_file():
            candidates.append(p)

    # Immediate-directory fallback only. Never rglob across /mnt/c.
    for directory in (root,root/"scripts"):
        if directory.is_dir():
            for p in directory.glob("*.py"):
                if p not in candidates:
                    candidates.append(p)

    valid=[]
    for p in candidates:
        text=p.read_text(encoding="utf-8",errors="replace")
        if (
            "def make_control_builder" in text
            and "def family_maxima" in text
            and "def axes" in text
        ):
            valid.append(p)

    if len(valid)!=1:
        raise RuntimeError(
            f"DYNAMIC_SOURCE_RESOLUTION={len(valid)} "
            f"candidates={[str(x) for x in valid]} scanned={[str(x) for x in candidates]}"
        )
    return valid[0]

def resolve_rule_path(consts):
    rule_stage=consts.get("RULE_STAGE")
    if not isinstance(rule_stage,str) or not rule_stage:
        raise RuntimeError(f"RULE_STAGE_CONSTANT_MISSING keys={sorted(consts)}")

    base=PRISM/rule_stage
    candidates=[
        base/"engine"/"frozen"/"candidate_first_rule_frozen.py",
        base/"frozen"/"candidate_first_rule_frozen.py",
        base/"candidate_first_rule_frozen.py",
    ]
    valid=[p for p in candidates if p.is_file()]
    if len(valid)!=1:
        raise RuntimeError(
            f"RULE_HARDBIND={len(valid)} RULE_STAGE={rule_stage} "
            f"tried={[str(x) for x in candidates]} valid={[str(x) for x in valid]}"
        )
    return valid[0]

def resolve_canonical_engine_path():
    p=CANONICAL_ENGINE
    if not p.is_file():
        raise RuntimeError(f"CANONICAL_ENGINE_MISSING={p}")
    text=p.read_text(encoding="utf-8",errors="replace")
    required=[
        "def free_position_search",
        "candidate_bank",
        "path_node_indices",
    ]
    missing=[x for x in required if x not in text]
    if missing:
        raise RuntimeError(
            f"CANONICAL_ENGINE_CONTRACT_FAIL path={p} missing={missing}"
        )
    return p

def col(df,names):
    for n in names:
        if n in df.columns:
            return n
    low={str(c).lower():c for c in df.columns}
    for n in names:
        if n.lower() in low:
            return low[n.lower()]
    raise RuntimeError(f"COLUMN_NOT_FOUND names={names} columns={list(df.columns)}")

def frozen_nodes(event):
    p=LOCK_ROOT/f"{event}_RESIDUAL_COMPLEX_LOCK.csv"
    if not p.exists():
        raise RuntimeError(f"FROZEN_LOCK_MISSING={p}")
    df=pd.read_csv(p)
    tc=col(df,["tau_s","center_s","time_s"])
    fc=col(df,["frequency_hz","f_hz","frequency"])
    wc=col(df,["width_s","width"])
    pc=next((x for x in ["path_index","node_index","index"] if x in df.columns),None)
    if pc:
        df=df.sort_values(pc)
    nodes=[]
    for i,r in enumerate(df.itertuples(index=False)):
        nodes.append({
            "path_index":i,
            "tau_s":float(getattr(r,tc)),
            "frequency_hz":float(getattr(r,fc)),
            "width_s":float(getattr(r,wc)),
            "node_z":float("nan"),
            "node_p":float("nan"),
        })
    return nodes

def classify(dyn,nodes):
    try:
        return str(dyn.classify_path(nodes))
    except Exception:
        return str(dyn.classify_path(pd.DataFrame(nodes)))

def candidate_hyper(c,rule):
    h=c.get("hyper")
    if isinstance(h,dict):
        return h
    hi=c.get("hyper_index")
    if hi is not None:
        return rule.HYPERGRID[int(hi)]
    raise RuntimeError(f"CANDIDATE_HYPER_MISSING keys={list(c.keys())}")

def nodes_from_candidate(c,state,taus,freqs,widths,rule):
    h=candidate_hyper(c,rule)
    t_i,f_i,w_i,node_z,node_p,_=rule.candidate_arrays(
        state,float(h["candidate_z_threshold"]),False
    )
    nodes=[]
    for order,j in enumerate(c.get("path_node_indices",[])):
        j=int(j)
        nodes.append({
            "path_index":order,
            "tau_s":float(taus[int(t_i[j])]),
            "frequency_hz":float(freqs[int(f_i[j])]),
            "width_s":float(widths[int(w_i[j])]),
            "node_z":float(node_z[j]),
            "node_p":float(node_p[j]),
        })
    return nodes

def family_best(engine,dyn,rule,state,taus,freqs,widths,target_family):
    free=engine.free_position_search(state,taus,freqs,widths,rule,True)
    bank=list(free.get("candidate_bank",[]))

    # Fail-closed fallback for engines exposing only role winners.
    if not bank:
        for role,r in free.get("roles",{}).items():
            if r.get("status")=="PATH_FOUND":
                x=dict(r)
                x["role"]=role
                bank.append(x)

    best=None
    for order,c in enumerate(bank):
        inds=c.get("path_node_indices",[])
        if not inds:
            continue
        nodes=nodes_from_candidate(c,state,taus,freqs,widths,rule)
        fam=classify(dyn,nodes)
        if fam!=target_family:
            continue
        score=float(c.get("score",c.get("path_score",0.0)))
        if best is None or score>best["score"]:
            best={
                "score":score,
                "nodes":nodes,
                "candidate_order":order,
                "role":str(c.get("role","")),
            }
    return best

def coords(nodes):
    return np.asarray(
        [[x["tau_s"],x["frequency_hz"],x["width_s"]] for x in nodes],
        dtype=float
    )

def exact_path_match(a,b):
    aa=coords(a);bb=coords(b)
    return bool(
        aa.shape==bb.shape and
        np.allclose(aa,bb,rtol=0,atol=np.asarray([5e-10,5e-8,5e-10]))
    )

def constant_tau_frame_equivalence(selected,frozen):
    aa=coords(selected)
    bb=coords(frozen)
    result={
        "match":False,
        "mode":"NONE",
        "tau_shift_s":float("nan"),
        "max_tau_shift_residual_s":float("nan"),
    }
    if aa.shape!=bb.shape or aa.ndim!=2 or aa.shape[1]!=3:
        return result

    # Morphology coordinates must be identical.
    if not np.allclose(aa[:,1],bb[:,1],rtol=0,atol=5e-8):
        return result
    if not np.allclose(aa[:,2],bb[:,2],rtol=0,atol=5e-10):
        return result

    delta=aa[:,0]-bb[:,0]
    if not np.all(np.isfinite(delta)):
        return result
    shift=float(np.median(delta))
    residual=np.asarray(delta-shift,dtype=float)
    max_resid=float(np.max(np.abs(residual))) if residual.size else 0.0

    # All nodes must share one and only one tau translation.
    if max_resid>5e-10:
        return result

    # Node-to-node spacing and ordering must remain exact.
    if len(aa)>1:
        if not np.allclose(
            np.diff(aa[:,0]),np.diff(bb[:,0]),rtol=0,atol=5e-10
        ):
            return result

    result.update({
        "match":True,
        "mode":"EVENTWISE_CONSTANT_TAU_FRAME_EQUIVALENCE",
        "tau_shift_s":shift,
        "max_tau_shift_residual_s":max_resid,
    })
    return result

def load_control_matrices(control_dir):
    pairs=numeric_controls(control_dir)
    if [i for i,_ in pairs]!=list(range(200)):
        raise RuntimeError(f"CONTROL_IDS_NOT_000_199 dir={control_dir}")
    H=[];L=[]
    for _,p in pairs:
        with np.load(p,allow_pickle=False) as z:
            H.append(np.asarray(z["H1"],dtype=float).reshape(-1))
            L.append(np.asarray(z["L1"],dtype=float).reshape(-1))
    return np.stack(H,axis=0),np.stack(L,axis=0)

def resolve_builder(dyn,coord,taus,freqs,widths,H,L,observed_shape):
    attempts=[
        ("ROW_MAJOR",H,L),
        ("COLUMN_MAJOR",H.T,L.T),
    ]
    errors=[]
    for label,h,l in attempts:
        try:
            build=dyn.make_control_builder(coord,taus,freqs,widths,h,l)
            s=np.asarray(build(0))
            if s.shape==observed_shape:
                return label,build
            errors.append(f"{label}:shape={s.shape}")
        except Exception as e:
            errors.append(f"{label}:{e!r}")
    raise RuntimeError(f"CONTROL_BUILDER_BINDING_FAILED errors={errors}")

def locked_control_score(event,family):
    for root in DYNAMIC_ROOTS:
        p=root/"work"/"checkpoints"/event/"control_family_scores.csv"
        if not p.exists():
            continue
        df=pd.read_csv(p)
        q=df[(df["control_id"].astype(int)==0)&(df["pattern_family"].astype(str)==family)]
        if len(q)==1:
            return float(q.iloc[0]["family_max_score"]),str(p)
    return None,""

def event_preflight(event,lock_row,dynamic_source,engine_path,rule_path):
    say(f"EVENT_PREFLIGHT_START event={event}")
    dyn,_,_=safe_function_module(dynamic_source,f"dyn_pre_{event}_{os.getpid()}")
    engine=full_import(engine_path,f"engine_pre_{event}_{os.getpid()}")
    rule=full_import(rule_path,f"rule_pre_{event}_{os.getpid()}")

    state_path=Path(lock_row["state_path"])
    control_dir=Path(lock_row["control_dir"])
    if not state_path.is_file():
        raise RuntimeError(f"PREFLIGHT_STATE_MISSING event={event} path={state_path}")
    if not control_dir.is_dir():
        raise RuntimeError(f"PREFLIGHT_CONTROL_DIR_MISSING event={event} path={control_dir}")

    observed=np.load(state_path,allow_pickle=False)
    d=state_path.parent
    coord,taus,freqs,widths=dyn.axes(engine,d,observed)

    frozen=frozen_nodes(event)
    target_family=classify(dyn,frozen)
    observed_best=family_best(
        engine,dyn,rule,observed,taus,freqs,widths,target_family
    )
    if observed_best is None:
        raise RuntimeError(
            f"PREFLIGHT_OBSERVED_FAMILY_PATH_NOT_FOUND event={event} "
            f"family={target_family}"
        )
    exact_match=exact_path_match(observed_best["nodes"],frozen)
    frame_match=constant_tau_frame_equivalence(
        observed_best["nodes"],frozen
    )
    if not exact_match and not frame_match["match"]:
        raise RuntimeError(
            f"PREFLIGHT_FROZEN_PATH_REPRO_FAIL event={event} "
            f"family={target_family} "
            f"selected_nodes={len(observed_best['nodes'])} "
            f"frozen_nodes={len(frozen)} "
            f"selected={coords(observed_best['nodes']).tolist()} "
            f"frozen={coords(frozen).tolist()}"
        )
    path_match_mode=(
        "EXACT_COORDINATE_MATCH"
        if exact_match else frame_match["mode"]
    )
    tau_frame_shift_s=(
        0.0 if exact_match else float(frame_match["tau_shift_s"])
    )
    max_tau_shift_residual_s=(
        0.0 if exact_match
        else float(frame_match["max_tau_shift_residual_s"])
    )

    H,L=load_control_matrices(control_dir)
    builder_layout,build=resolve_builder(
        dyn,coord,taus,freqs,widths,H,L,tuple(observed.shape)
    )
    control0=np.asarray(build(0))
    if control0.shape!=observed.shape:
        raise RuntimeError(
            f"PREFLIGHT_CONTROL0_SHAPE event={event} "
            f"shape={control0.shape} expected={observed.shape}"
        )
    control0_best=family_best(
        engine,dyn,rule,control0,taus,freqs,widths,target_family
    )

    result={
        "event":event,
        "target_family":target_family,
        "frozen_nodes":len(frozen),
        "builder_layout":builder_layout,
        "path_match_mode":path_match_mode,
        "tau_frame_shift_s":tau_frame_shift_s,
        "max_tau_shift_residual_s":max_tau_shift_residual_s,
        "control0_status":"PATH_FOUND" if control0_best is not None else "NO_PATH",
        "status":"PASS",
    }
    say(
        f"EVENT_PREFLIGHT_PASS event={event} family={target_family} "
        f"frozen_nodes={len(frozen)} builder={builder_layout} "
        f"path_match={path_match_mode} "
        f"tau_shift_s={tau_frame_shift_s:+.6f} "
        f"tau_shift_residual_s={max_tau_shift_residual_s:.3e} "
        f"control0={result['control0_status']}"
    )
    return result

def one_event(event,lock_row,dynamic_source,engine_path,rule_path):
    say(f"EVENT_SELECTION_START event={event}")
    say(f"EVENT_ENGINE_LOCK event={event} path={engine_path}")
    event_out=WORK/event
    event_out.mkdir(parents=True,exist_ok=True)

    dyn,_,_=safe_function_module(dynamic_source,f"dyn_{event}")
    engine=full_import(engine_path,f"engine_{event}_{os.getpid()}")
    rule=full_import(rule_path,f"rule_{event}")

    state_path=Path(lock_row["state_path"])
    control_dir=Path(lock_row["control_dir"])
    observed=np.load(state_path,allow_pickle=False)

    d=state_path.parent
    coord,taus,freqs,widths=dyn.axes(engine,d,observed)
    H,L=load_control_matrices(control_dir)
    builder_layout,build=resolve_builder(
        dyn,coord,taus,freqs,widths,H,L,tuple(observed.shape)
    )

    frozen=frozen_nodes(event)
    target_family=classify(dyn,frozen)
    observed_best=family_best(
        engine,dyn,rule,observed,taus,freqs,widths,target_family
    )
    if observed_best is None:
        raise RuntimeError(f"OBSERVED_FAMILY_PATH_NOT_FOUND event={event} family={target_family}")
    exact_match=exact_path_match(observed_best["nodes"],frozen)
    frame_match=constant_tau_frame_equivalence(
        observed_best["nodes"],frozen
    )
    if not exact_match and not frame_match["match"]:
        raise RuntimeError(
            f"OBSERVED_FROZEN_PATH_REPRO_FAIL event={event} family={target_family} "
            f"selected_nodes={len(observed_best['nodes'])} frozen_nodes={len(frozen)} "
            f"selected={coords(observed_best['nodes']).tolist()} frozen={coords(frozen).tolist()}"
        )
    path_match_mode=(
        "EXACT_COORDINATE_MATCH"
        if exact_match else frame_match["mode"]
    )
    tau_frame_shift_s=(
        0.0 if exact_match else float(frame_match["tau_shift_s"])
    )
    max_tau_shift_residual_s=(
        0.0 if exact_match
        else float(frame_match["max_tau_shift_residual_s"])
    )

    def run_control(cid):
        state=np.asarray(build(int(cid)))
        if state.shape!=observed.shape:
            raise RuntimeError(f"CONTROL_STATE_SHAPE event={event} cid={cid} shape={state.shape}")
        best=family_best(
            engine,dyn,rule,state,taus,freqs,widths,target_family
        )
        return {
            "event":event,
            "control_id":int(cid),
            "family":target_family,
            "status":"PATH_FOUND" if best is not None else "NO_PATH",
            "score":float(best["score"]) if best is not None else 0.0,
            "path_nodes":int(len(best["nodes"])) if best is not None else 0,
        }

    rows=[]
    say(f"CONTROL_BATCH_START event={event} total=200 threads={CONTROL_THREADS_PER_EVENT}")
    with ThreadPoolExecutor(max_workers=CONTROL_THREADS_PER_EVENT) as ex:
        futs={ex.submit(run_control,cid):cid for cid in range(200)}
        for done,f in enumerate(as_completed(futs),1):
            cid=futs[f]
            try:
                row=f.result()
            except Exception:
                say(
                    f"CONTROL_FAILED event={event} control={cid:03d} "
                    f"done={done-1}/200 left={201-done}"
                )
                raise
            rows.append(row)
            status=row["status"]
            nodes=row["path_nodes"]
            say(
                f"CONTROL_PROGRESS event={event} control={cid:03d} "
                f"done={done}/200 left={200-done} "
                f"status={status} nodes={nodes}"
            )
            if done%10==0 or done==200:
                ck=pd.DataFrame(rows).sort_values("control_id").reset_index(drop=True)
                atomic_csv(ck,event_out/"CONTROL_PATH_SELECTION_CHECKPOINT.csv")
                say(
                    f"CONTROL_CHECKPOINT event={event} "
                    f"saved={done}/200 left={200-done}"
                )

    cdf=pd.DataFrame(rows).sort_values("control_id").reset_index(drop=True)
    atomic_csv(cdf,event_out/"CONTROL_PATH_SELECTION.csv")

    # Exact replay check against the previous dynamic-null ledger, when available.
    locked0,locked_path=locked_control_score(event,target_family)
    numerical_replay=True
    numerical_delta=float("nan")
    if locked0 is not None:
        got=float(cdf.loc[cdf["control_id"].eq(0),"score"].iloc[0])
        numerical_delta=got-locked0
        numerical_replay=bool(abs(numerical_delta)<=1e-9)
        if not numerical_replay:
            raise RuntimeError(
                f"CONTROL0_DYNAMIC_NULL_REPLAY_FAIL event={event} family={target_family} "
                f"got={got} locked={locked0} delta={numerical_delta} source={locked_path}"
            )

    out={
        "event":event,
        "engine_path":str(engine_path),
        "engine_sha256":sha256(engine_path),
        "target_family":target_family,
        "frozen_nodes":len(frozen),
        "observed_selected_nodes":len(observed_best["nodes"]),
        "observed_path_exact_reproduction":bool(exact_match),
        "observed_path_frame_equivalent_reproduction":bool(
            exact_match or frame_match["match"]
        ),
        "path_match_mode":path_match_mode,
        "tau_frame_shift_s":tau_frame_shift_s,
        "max_tau_shift_residual_s":max_tau_shift_residual_s,
        "builder_layout":builder_layout,
        "controls":len(cdf),
        "path_found_controls":int(cdf["path_nodes"].gt(0).sum()),
        "no_path_controls":int(cdf["path_nodes"].eq(0).sum()),
        "path_found_fraction":float(cdf["path_nodes"].gt(0).mean()),
        "median_positive_nodes":float(cdf.loc[cdf["path_nodes"].gt(0),"path_nodes"].median())
            if cdf["path_nodes"].gt(0).any() else float("nan"),
        "max_nodes":int(cdf["path_nodes"].max()),
        "control0_locked_score_available":locked0 is not None,
        "control0_numerical_replay_pass":numerical_replay,
        "control0_score_delta":numerical_delta,
    }
    pd.DataFrame([out]).to_csv(event_out/"EVENT_SELECTION_SUMMARY.csv",index=False)
    say(
        f"EVENT_SELECTION_DONE event={event} family={target_family} "
        f"found={out['path_found_controls']}/200 frozen_nodes={len(frozen)} "
        f"replay={numerical_replay}"
    )
    return out,cdf[["control_id","path_nodes","score"]].copy()

def phase_chunk(args):
    mode,node_matrix,positive_lists,n_draws,seed=args
    rng=np.random.default_rng(seed)
    stats=np.empty(n_draws,dtype=float)
    nevents=node_matrix.shape[0]
    ncontrols=node_matrix.shape[1]

    for d in range(n_draws):
        total=0.0
        for e in range(nevents):
            if mode=="CONDITIONAL":
                arr=positive_lists[e]
                n=int(arr[rng.integers(0,len(arr))])
            else:
                n=int(node_matrix[e,rng.integers(0,ncontrols)])
            if n>0:
                total += float(np.cos(rng.uniform(-math.pi,math.pi,n)).mean())
        stats[d]=total/nevents
    return stats

def run_phase_null(mode,node_matrix):
    positives=[row[row>0].astype(int) for row in node_matrix]
    if mode=="CONDITIONAL" and any(len(x)==0 for x in positives):
        missing=[EVENTS[i] for i,x in enumerate(positives) if len(x)==0]
        raise RuntimeError(f"NO_POSITIVE_PATH_CONTROLS events={missing}")

    base=NULL_DRAWS//NULL_WORKERS
    rem=NULL_DRAWS%NULL_WORKERS
    tasks=[]
    for i in range(NULL_WORKERS):
        n=base+(1 if i<rem else 0)
        tasks.append((mode,node_matrix,positives,n,BASE_SEED+(100000 if mode=="CONDITIONAL" else 0)+i))

    parts=[]
    with ProcessPoolExecutor(max_workers=NULL_WORKERS) as ex:
        futs=[ex.submit(phase_chunk,t) for t in tasks]
        for i,f in enumerate(as_completed(futs),1):
            parts.append(f.result())
            say(f"PHASE_NULL_WORKER_RETURNED mode={mode} worker={i}/{NULL_WORKERS}")
    x=np.concatenate(parts)
    if len(x)!=NULL_DRAWS:
        raise RuntimeError(f"NULL_DRAW_COUNT mode={mode} got={len(x)}")
    return x

def summarize_null(name,x,observed):
    exceed=int(np.sum(x>=observed-1e-15))
    return {
        "null_name":name,
        "draws":len(x),
        "observed_zero_direction_real":observed,
        "exceed":exceed,
        "empirical_p":float((exceed+1)/(len(x)+1)),
        "null_mean":float(np.mean(x)),
        "null_std":float(np.std(x,ddof=1)),
        "null_q95":float(np.quantile(x,0.95)),
        "null_q99":float(np.quantile(x,0.99)),
        "null_max":float(np.max(x)),
    }

def main():
    required=[R6_LOCK,C42C_SUM]
    for p in required:
        if not p.exists():
            raise RuntimeError(f"REQUIRED_FILE_MISSING={p}")

    lock=pd.read_csv(R6_LOCK)
    lock=lock.set_index("event").loc[EVENTS].reset_index()
    if len(lock)!=13:
        raise RuntimeError(f"R6_LOCK_ROWS={len(lock)}")

    csum=pd.read_csv(C42C_SUM).iloc[0]
    observed_real=float(csum["EQUAL_EVENT_COMPLEX_REAL"])
    observed_resultant=float(csum["EQUAL_EVENT_RESULTANT_LENGTH"])
    observed_phase=float(csum["EQUAL_EVENT_MEAN_PHASE_RAD"])
    if not np.isclose(observed_real,EXPECTED_OBSERVED_REAL,rtol=0,atol=1e-15):
        raise RuntimeError(f"OBSERVED_REAL_LOCK_FAIL got={observed_real}")
    if not np.isclose(observed_resultant,EXPECTED_OBSERVED_RESULTANT,rtol=0,atol=1e-15):
        raise RuntimeError(f"OBSERVED_RESULTANT_LOCK_FAIL got={observed_resultant}")
    if not np.isclose(observed_phase,EXPECTED_OBSERVED_PHASE,rtol=0,atol=1e-15):
        raise RuntimeError(f"OBSERVED_PHASE_LOCK_FAIL got={observed_phase}")

    say("SOURCE_BINDING_START=TRUE")
    dynamic_source=resolve_dynamic_source()
    say(f"DYNAMIC_SOURCE_LOCK={dynamic_source}")
    _,dynamic_text,consts=safe_function_module(dynamic_source,"dynamic_probe")
    engine_path=resolve_canonical_engine_path()
    rule_path=resolve_rule_path(consts)
    say(f"CANONICAL_ENGINE_LOCK={engine_path}")
    say(f"CANONICAL_ENGINE_SHA256={sha256(engine_path)}")
    say(f"RULE_SOURCE_LOCK={rule_path}")
    say(f"RULE_SOURCE_SHA256={sha256(rule_path)}")
    say("SOURCE_BINDINGS_LOCK=PASS")

    (OUT/"SOURCE_BINDINGS.json").write_text(json.dumps({
        "dynamic_source":str(dynamic_source),
        "dynamic_source_sha256":sha256(dynamic_source),
        "canonical_engine_path":str(engine_path),
        "canonical_engine_sha256":sha256(engine_path),
        "canonical_engine_load_mode":"FULL_IMPORT_EXACT",
        "rule_path":str(rule_path),
        "rule_sha256":sha256(rule_path),
        "R6_lock":str(R6_LOCK),
        "R6_lock_sha256":sha256(R6_LOCK),
        "C42C_summary":str(C42C_SUM),
        "C42C_summary_sha256":sha256(C42C_SUM),
    },indent=2),encoding="utf-8")

    # Import the canonical engine and rule once before worker launch.
    pre_engine=full_import(engine_path,"canonical_engine_preflight")
    pre_rule=full_import(rule_path,"canonical_rule_preflight")
    required_engine_names=[
        "CENTERS","FREQS","WIDTHS","free_position_search",
        "coord_template","control_state",
    ]
    missing_engine=[x for x in required_engine_names if not hasattr(pre_engine,x)]
    if missing_engine:
        raise RuntimeError(f"CANONICAL_ENGINE_IMPORT_MISSING={missing_engine}")
    if not hasattr(pre_rule,"candidate_arrays"):
        raise RuntimeError("RULE_IMPORT_NO_CANDIDATE_ARRAYS")
    say("ENGINE_LOAD_MODE=FULL_IMPORT_EXACT")
    say(
        "CANONICAL_ENGINE_IMPORT=PASS "
        f"CENTERS={len(pre_engine.CENTERS)} "
        f"FREQS={len(pre_engine.FREQS)} "
        f"WIDTHS={len(pre_engine.WIDTHS)}"
    )
    say("RULE_IMPORT=PASS")

    # All 13 events must pass observed/control0 preflight before 2,600 control runs.
    say(f"ALL_EVENT_PREFLIGHT_STARTED={EVENT_WORKERS}")
    preflight_rows=[]
    preflight_errors=[]
    with ProcessPoolExecutor(max_workers=EVENT_WORKERS) as ex:
        pfuts={}
        for r in lock.to_dict(orient="records"):
            e=str(r["event"])
            pfuts[ex.submit(
                event_preflight,e,r,dynamic_source,engine_path,rule_path
            )]=e
        for i,f in enumerate(as_completed(pfuts),1):
            e=pfuts[f]
            try:
                preflight_rows.append(f.result())
                say(f"EVENT_PREFLIGHT_RETURNED={i}/13 event={e}")
            except Exception:
                tb=traceback.format_exc()
                preflight_errors.append({"event":e,"traceback":tb})
                say(f"EVENT_PREFLIGHT_FAILED event={e}")
                print(tb,flush=True)

    atomic_csv(pd.DataFrame(preflight_rows),OUT/"EVENT_PREFLIGHT_PASS.csv")
    atomic_csv(pd.DataFrame(preflight_errors),OUT/"EVENT_PREFLIGHT_ERRORS.csv")
    if preflight_errors:
        raise RuntimeError(f"EVENT_PREFLIGHT_ERRORS={len(preflight_errors)}")
    say("ALL_EVENT_PREFLIGHT=PASS 13/13")

    rows=[]
    matrices={}
    errors=[]
    say(f"EVENT_WORKERS_STARTED={EVENT_WORKERS}")
    with ProcessPoolExecutor(max_workers=EVENT_WORKERS) as ex:
        futs={}
        for r in lock.to_dict(orient="records"):
            e=str(r["event"])
            futs[ex.submit(
                one_event,e,r,dynamic_source,engine_path,rule_path
            )]=e
        for i,f in enumerate(as_completed(futs),1):
            e=futs[f]
            try:
                summary,cdf=f.result()
                rows.append(summary)
                matrices[e]=cdf
                say(f"EVENT_WORKER_RETURNED={i}/13 event={e}")
            except Exception:
                tb=traceback.format_exc()
                errors.append({"event":e,"traceback":tb})
                say(f"EVENT_WORKER_FAILED event={e}")
                print(tb,flush=True)

    atomic_csv(pd.DataFrame(errors),OUT/"EVENT_ERRORS.csv")
    if errors:
        raise RuntimeError(f"EVENT_ERRORS={len(errors)}")

    ev=pd.DataFrame(rows).set_index("event").loc[EVENTS].reset_index()
    ev.to_csv(OUT/"EVENT_SELECTION_AWARE_SUMMARY.csv",index=False)

    node_matrix=np.stack([
        matrices[e].sort_values("control_id")["path_nodes"].to_numpy(int)
        for e in EVENTS
    ],axis=0)
    score_matrix=np.stack([
        matrices[e].sort_values("control_id")["score"].to_numpy(float)
        for e in EVENTS
    ],axis=0)
    np.save(OUT/"CONTROL_SELECTED_PATH_NODE_COUNTS.npy",node_matrix)
    np.save(OUT/"CONTROL_SELECTED_PATH_SCORES.npy",score_matrix)

    all_control_rows=[]
    for e in EVENTS:
        x=matrices[e].copy()
        x.insert(0,"event",e)
        all_control_rows.append(x)
    pd.concat(all_control_rows,ignore_index=True).to_csv(
        OUT/"ALL_EVENT_CONTROL_SELECTED_PATHS.csv",index=False
    )

    conditional=run_phase_null("CONDITIONAL",node_matrix)
    joint=run_phase_null("JOINT",node_matrix)
    np.save(OUT/"CONDITIONAL_SELECTOR_AWARE_PHASE_NULL.npy",conditional)
    np.save(OUT/"JOINT_SELECTOR_PHASE_NULL.npy",joint)

    summaries=[
        summarize_null(
            "EXACT_SELECTOR_AWARE_PHASE_GIVEN_SAME_FAMILY_PATH_PRESENT",
            conditional,observed_real
        ),
        summarize_null(
            "EXACT_SELECTOR_PLUS_PATH_EXISTENCE_JOINT_PHASE_NULL",
            joint,observed_real
        ),
    ]
    ns=pd.DataFrame(summaries)
    ns.to_csv(OUT/"NULL_SUMMARY.csv",index=False)

    primary=ns.iloc[0]
    pass05=bool(float(primary["empirical_p"])<=0.05)
    pass01=bool(float(primary["empirical_p"])<=0.01)

    out={
        "R_STATUS":"PASS",
        "STAGE":STAGE,
        "ANALYSIS_CLASS":"EXACT_SELECTOR_AWARE_COMPLEX_PHASE_NULL",
        "EVENT_WORKERS":EVENT_WORKERS,
        "CONTROL_THREADS_PER_EVENT":CONTROL_THREADS_PER_EVENT,
        "NULL_WORKERS":NULL_WORKERS,
        "EVENTS_COMPLETE":len(ev),
        "CONTROLS_PER_EVENT":200,
        "TOTAL_CONTROL_SELECTION_RUNS":int(len(ev)*200),
        "OBSERVED_FROZEN_PATH_REPRODUCED_EVENTS":int(
            ev["observed_path_frame_equivalent_reproduction"].sum()
        ),
        "OBSERVED_FROZEN_PATH_EXACT_EVENTS":int(
            ev["observed_path_exact_reproduction"].sum()
        ),
        "OBSERVED_FROZEN_PATH_FRAME_EQUIVALENT_EVENTS":int(
            ev["observed_path_frame_equivalent_reproduction"].sum()
            - ev["observed_path_exact_reproduction"].sum()
        ),
        "MAX_ABS_EVENTWISE_TAU_SHIFT_S":float(
            ev["tau_frame_shift_s"].abs().max()
        ),
        "MAX_TAU_SHIFT_RESIDUAL_S":float(
            ev["max_tau_shift_residual_s"].max()
        ),
        "CONTROL0_NUMERICAL_REPLAY_EVENTS_AVAILABLE":int(ev["control0_locked_score_available"].sum()),
        "CONTROL0_NUMERICAL_REPLAY_EVENTS_PASS":int(ev["control0_numerical_replay_pass"].sum()),
        "OBSERVED_ZERO_DIRECTION_REAL":observed_real,
        "OBSERVED_RESULTANT_LENGTH":observed_resultant,
        "OBSERVED_MEAN_PHASE_RAD":observed_phase,
        "PRIMARY_NULL_CLASS":"EXACT_SELECTOR_AWARE_PHASE_GIVEN_SAME_FAMILY_PATH_PRESENT",
        "PRIMARY_NULL_DRAWS":int(primary["draws"]),
        "PRIMARY_NULL_EXCEED":int(primary["exceed"]),
        "PRIMARY_EMPIRICAL_P":float(primary["empirical_p"]),
        "PRIMARY_NULL_Q99":float(primary["null_q99"]),
        "PRIMARY_NULL_MAX":float(primary["null_max"]),
        "JOINT_NULL_EXCEED":int(ns.iloc[1]["exceed"]),
        "JOINT_EMPIRICAL_P":float(ns.iloc[1]["empirical_p"]),
        "SELECTION_AWARE_PHASE_SUPPORT_P_LT_0P05":pass05,
        "SELECTION_AWARE_PHASE_SUPPORT_P_LT_0P01":pass01,
        "SCIENTIFIC_VERDICT":(
            "DIRECT_COMPLEX_PHASE_SUPPORT_SURVIVES_EXACT_SELECTOR_AWARE_NULL"
            if pass01 else
            "DIRECT_COMPLEX_PHASE_SUPPORT_NOT_SIGNIFICANT_UNDER_EXACT_SELECTOR_AWARE_NULL"
        ),
        "CLAIM_BOUNDARY":"Selector-aware conditional phase-randomization result; offsource controls contain real H1/L1 selection arrays but no empirical complex phases, so this is not an empirical offsource detector-phase null.",
        "NEXT":(
            "FREEZE_SELECTOR_AWARE_COMPLEX_PHASE_RESULT_AND_INTEGRATE_PAPER_II"
            if pass01 else
            "CLOSE_COMPLEX_PHASE_AS_SELECTION_COMPATIBLE_AND_RETAIN_AMPLITUDE_RESULT"
        ),
        "PROCESS_EXIT":0,
    }

    pd.DataFrame([out]).to_csv(OUT/"FINAL_SUMMARY.csv",index=False)
    text="\n".join(f"{k}={v}" for k,v in out.items())+"\n"
    (OUT/"RUN_SUMMARY.txt").write_text(text,encoding="utf-8")
    print(text,end="")

if __name__=="__main__":
    try:
        main()
    except Exception:
        tb=traceback.format_exc()
        (OUT/"FATAL_TRACEBACK.txt").write_text(tb,encoding="utf-8")
        print(tb,file=sys.stderr)
        d={
            "R_STATUS":"FAIL",
            "STAGE":STAGE,
            "SCIENTIFIC_VERDICT":"TECHNICAL_FAILURE_NO_NEW_SCIENTIFIC_RESULT",
            "NEXT":"SEND_EVENT_ERRORS_AND_FATAL_TRACEBACK",
            "PROCESS_EXIT":2,
        }
        text="\n".join(f"{k}={v}" for k,v in d.items())+"\n"
        (OUT/"RUN_SUMMARY.txt").write_text(text,encoding="utf-8")
        print(text,end="")
        raise SystemExit(2)
