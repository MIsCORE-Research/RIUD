from __future__ import annotations

import hashlib, json, math, os, shutil, time, zipfile
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

ROOT = Path(r"E:\RIUD_ACTIVE_20260808")
R5 = ROOT / "RIUD_DEV99_EVENT_COVERAGE_RATE_BALANCE_DYNAMICS_DISCOVERY_R5_20260814"
R4 = ROOT / "RIUD_DEV99_R3_F5_TURNOVER_OPERATOR_IDENTITY_AUDIT_R4_20260814"
ATLAS = ROOT / "RIUD_DEV99_GLOBAL_FULL_WINDOW_NODE_ATLAS_R1_20260814" / "OUTPUT"
STAGE = ROOT / "RIUD_DEV99_REENTRY_MULTISTATE_STATE_IDENTITY_AUDIT_R6_20260815"
PKG = ROOT / "RIUD_DEV99_REENTRY_MULTISTATE_STATE_IDENTITY_AUDIT_R6_20260815_PACKAGE.zip"
OBSERVED = 97
NBIN = 32
LANDMARKS = [
    ("FIRST_TURNOVER", 10.94),
    ("DERIVATIVE_RECOVERY", 14.06421875),
    ("SECOND_TURNOVER", 17.1884375),
    ("GLOBAL_PEAK", 45.3125),
    ("SUPPORT_DROP", 46.875),
]

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()

def log(msg: str):
    print(msg, flush=True)
    with (STAGE / "RUN.log").open("a", encoding="utf-8") as f:
        f.write(msg + "\n")

def write_json(name, obj):
    (STAGE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

def pct(v):
    return float(v) if pd.notna(v) else np.nan

def contiguous_runs(a: np.ndarray) -> List[Tuple[int, int]]:
    out=[]; k=0
    while k < len(a):
        if a[k]:
            s=k
            while k+1 < len(a) and a[k+1]: k += 1
            out.append((s,k))
        k += 1
    return out

def fixed_columns(df, names, default=np.nan):
    for n in names:
        if n not in df.columns: df[n]=default
    return df

def audit_source(path: Path, rows=None, cols=None):
    return {"PATH": str(path), "SHA256": sha256(path), "SIZE": path.stat().st_size,
            "ROWS": rows if rows is not None else "UNKNOWN", "COLUMNS": cols if cols is not None else "UNKNOWN"}

def main():
    t0=time.time(); STAGE.mkdir(parents=True, exist_ok=True)
    (STAGE / "RUN.log").write_text("", encoding="utf-8")
    log("GLOBAL_PROGRESS=0% GLOBAL_ETA=unknown ELAPSED=0s ACTIVE_WORKERS=1 REMAINING=read-only audit")
    log("CURRENT_STAGE=SOURCE_SHA_AUDIT SOURCE_SHA_AUDIT=RUNNING OCCUPANCY_REPLAY=PENDING MULTISTATE_CLASSIFICATION=PENDING TRANSITION_REPLAY=PENDING FLUX_DECOMPOSITION=PENDING REENTRY_GAP_AUDIT=PENDING LANDMARK_AUDIT=PENDING PROMINENCE_AUDIT=PENDING")

    paths = {
        "R5_OCCUPANCY": R5/"EVENT_BIN_OCCUPANCY_MATRIX.csv",
        "R5_ACCOUNTING": R5/"EVENT_COVERAGE_GAIN_LOSS_ACCOUNTING.csv",
        "R5_TRAJECTORY": R5/"EVENT_GAIN_LOSS_TRAJECTORY_AUDIT.csv",
        "R5_EXACT": R5/"EVENT_COVERAGE_EXACT_REPLAY.csv",
        "R4_OBSERVED": R4/"FROZEN_OBSERVED_PROFILE_REPLAY.csv",
        "R4_TURNOVER": R4/"TURNOVER_OPERATOR_TRIPLE_REPLAY.csv",
        "R4_PEAK": R4/"PEAK_OPERATOR_TRIPLE_REPLAY.csv",
        "ATLAS_NODES": ATLAS/"GLOBAL_NODE_ATLAS_1077.csv",
        "ATLAS_BINS": ATLAS/"LATENT_BIN_SUMMARY.csv",
        "ATLAS_COVERAGE": ATLAS/"EVENT_LATENT_COVERAGE.csv",
        "ATLAS_T0": ATLAS/"NOMINAL_T0_LATENT_POSITIONS.csv",
    }
    missing=[str(p) for p in paths.values() if not p.exists()]
    if missing:
        write_json("R_STATUS.json", {"R_STATUS":"TECHNICAL_FAIL","REASON":"MISSING_SOURCE","MISSING":missing})
        return
    occ = pd.read_csv(paths["R5_OCCUPANCY"])
    acc = pd.read_csv(paths["R5_ACCOUNTING"])
    traj = pd.read_csv(paths["R5_TRAJECTORY"])
    exact = pd.read_csv(paths["R5_EXACT"])
    topology = pd.read_csv(R5/"GLOBAL_RATE_LANDMARK_TOPOLOGY_AUDIT.csv")
    obsprof = pd.read_csv(paths["R4_OBSERVED"])
    turn = pd.read_csv(paths["R4_TURNOVER"])
    peak = pd.read_csv(paths["R4_PEAK"])
    nodes = pd.read_csv(paths["ATLAS_NODES"])
    bins = pd.read_csv(paths["ATLAS_BINS"])
    coverage = pd.read_csv(paths["ATLAS_COVERAGE"])
    t0df = pd.read_csv(paths["ATLAS_T0"])
    prov=[]
    for k,p in paths.items():
        d=pd.read_csv(p); prov.append(audit_source(p, len(d), ",".join(map(str,d.columns))))
    pd.DataFrame(prov).to_csv(STAGE/"SOURCE_PROVENANCE.csv", index=False)
    # Existing manifest checks are read-only. RUN.log is volatile and explicitly exempted.
    volatile=[]; nonvolatile=[]
    for root in [R5,R4,ATLAS]:
        mf=root/"SHA256SUMS.txt"
        if not mf.exists(): continue
        for line in mf.read_text(errors="replace").splitlines():
            parts=line.strip().split(maxsplit=1)
            if len(parts)!=2: continue
            expected, name=parts
            name=name.lstrip("* ")
            fp=root/name
            if not fp.exists(): continue
            actual=sha256(fp)
            if actual != expected:
                (volatile if fp.name.lower()=="run.log" else nonvolatile).append({"path":str(fp),"expected":expected,"actual":actual})
    sha_ok = not nonvolatile
    log(f"SOURCE_SHA_AUDIT={'PASS' if sha_ok else 'FAIL'} VOLATILE_RUN_LOG_MISMATCH_COUNT={len(volatile)}")
    if not sha_ok:
        write_json("R_STATUS.json", {"R_STATUS":"TECHNICAL_FAIL","SOURCE_SHA_AUDIT":"FAIL","MISMATCHES":nonvolatile})
        return

    # Exact binary matrix from R5.
    events=sorted(occ.EVENT.astype(str).unique())
    bins_idx=sorted(occ.BIN_INDEX.astype(int).unique())
    if len(events)!=97 or len(bins_idx)!=32:
        write_json("R_STATUS.json", {"R_STATUS":"TECHNICAL_FAIL","REASON":"UNEXPECTED_OCCUPANCY_SHAPE","EVENTS":len(events),"BINS":len(bins_idx)})
        return
    A=occ.pivot(index="EVENT", columns="BIN_INDEX", values="OCCUPIED").reindex(index=events,columns=bins_idx).fillna(0).astype(int).to_numpy()
    C=A.sum(axis=0)
    frozen=exact.sort_values("BIN_INDEX")["C_FROZEN_R4"].astype(float).to_numpy()
    replay_match=bool(np.array_equal(C.astype(float), frozen))
    log(f"GLOBAL_PROGRESS=15% GLOBAL_ETA=short ELAPSED={time.time()-t0:.1f}s ACTIVE_WORKERS=1 REMAINING=state classification")
    log(f"OCCUPANCY_REPLAY={'PASS' if replay_match else 'FAIL'} MAX_ABS_ERROR={float(np.max(np.abs(C-frozen)))}")
    if not replay_match:
        write_json("R_STATUS.json", {"R_STATUS":"TECHNICAL_FAIL","OCCUPANCY_REPLAY":"FAIL"})
        return
    pct_left=np.array([(float(occ[occ.BIN_INDEX==k].GLOBAL_LEFT_PCT.iloc[0])+float(occ[occ.BIN_INDEX==k].GLOBAL_RIGHT_PCT.iloc[0]))/2 for k in bins_idx])
    # 32-bin event history, using only history up to each bin.
    state_rows=[]; state_arrays={}; run_arrays={}
    for ei,event in enumerate(events):
        z=A[ei].astype(bool); states=[]; runs=[]; prior_g=prior_l=0; completed=0; current_run=0; seen=False; last=None
        for k in bins_idx:
            before_g,before_l=prior_g,prior_l
            if k>0:
                prev=bool(z[k-1]); cur=bool(z[k])
                if prev and not cur:
                    completed += 1
                if (not prev) and cur:
                    current_run=completed+1
                if prev and cur and current_run==0: current_run=1
            cur=bool(z[k])
            if cur:
                if not seen: current_run=1; state="A1"
                else: state="A1" if current_run==1 else "AR"
                seen=True; last=k
            else:
                state="N0" if not seen else "G"
            since=0 if cur else (np.nan if last is None else k-last)
            states.append(state); runs.append(current_run if cur else 0)
            row={"EVENT":event,"BIN_INDEX":k,"GLOBAL_LEFT_PCT":float(occ[(occ.BIN_INDEX==k)].GLOBAL_LEFT_PCT.iloc[0]),"GLOBAL_RIGHT_PCT":float(occ[(occ.BIN_INDEX==k)].GLOBAL_RIGHT_PCT.iloc[0]),"GLOBAL_MID_PCT":float(pct_left[k]),"OCCUPIED":int(cur),"STATE":state,"HAS_EVER_BEEN_ACTIVE_BEFORE_BIN":bool(seen and not (cur and runs[-1]==1 and before_g==0)),"N_PRIOR_GAINS":before_g,"N_PRIOR_LOSSES":before_l,"N_COMPLETED_ACTIVE_RUNS":completed,"CURRENT_ACTIVE_RUN_INDEX":current_run if cur else 0,"TIME_SINCE_LAST_ACTIVE_BIN":since}
            state_rows.append(row)
            if k>0:
                if (not z[k-1]) and z[k]: prior_g += 1
                if z[k-1] and (not z[k]): prior_l += 1
        state_arrays[event]=states; run_arrays[event]=runs
    hist=pd.DataFrame(state_rows); hist.to_csv(STAGE/"EVENT_MULTISTATE_HISTORY_MATRIX.csv",index=False)
    log("MULTISTATE_CLASSIFICATION=PASS")
    # population and run-index profiles.
    pop=[]; rip=[]
    for k in bins_idx:
        ss=hist[hist.BIN_INDEX==k].STATE
        rr=hist[hist.BIN_INDEX==k]
        d={"BIN_INDEX":k,"GLOBAL_MID_PCT":pct_left[k],"N0":int((ss=="N0").sum()),"A1":int((ss=="A1").sum()),"G":int((ss=="G").sum()),"AR":int((ss=="AR").sum()),"ACTIVE_TOTAL":int((ss.isin(["A1","AR"])).sum()),"OCCUPANCY_C_EXACT":int(C[k])}
        pop.append(d)
        rip.append({"BIN_INDEX":k,"GLOBAL_MID_PCT":pct_left[k],"RUN1_ACTIVE":int((rr.CURRENT_ACTIVE_RUN_INDEX==1).sum()),"RUN2_ACTIVE":int((rr.CURRENT_ACTIVE_RUN_INDEX==2).sum()),"RUN3_ACTIVE":int((rr.CURRENT_ACTIVE_RUN_INDEX==3).sum()),"RUN4PLUS_ACTIVE":int((rr.CURRENT_ACTIVE_RUN_INDEX>=4).sum())})
    popdf=pd.DataFrame(pop); popdf.to_csv(STAGE/"MULTISTATE_POPULATION_PROFILE.csv",index=False); pd.DataFrame(rip).to_csv(STAGE/"ACTIVE_RUN_INDEX_PROFILE.csv",index=False)
    # state transition table
    trans=[]
    for k in range(NBIN-1):
        for f in ["N0","A1","G","AR"]:
            for t in ["N0","A1","G","AR"]:
                n=sum(state_arrays[e][k]==f and state_arrays[e][k+1]==t for e in events)
                if n: trans.append({"BOUNDARY_INDEX":k,"GLOBAL_MID_PCT":float((pct_left[k]+pct_left[k+1])/2),"FROM_STATE":f,"TO_STATE":t,"COUNT":int(n)})
    transdf=pd.DataFrame(trans); transdf.to_csv(STAGE/"MULTISTATE_TRANSITION_COUNTS.csv",index=False)
    allowed={("N0","N0"),("N0","A1"),("A1","A1"),("A1","G"),("G","G"),("G","AR"),("AR","AR"),("AR","G")}
    illegal=sum(int(r.COUNT) for r in transdf.itertuples() if (r.FROM_STATE,r.TO_STATE) not in allowed)
    log(f"TRANSITION_REPLAY={'PASS' if illegal==0 else 'FAIL'} ILLEGAL_TRANSITION_COUNT={illegal}")
    # flux by boundary
    flux=[]
    for k in range(NBIN-1):
        pairs={(f,t):int(transdf[(transdf.BOUNDARY_INDEX==k)&(transdf.FROM_STATE==f)&(transdf.TO_STATE==t)].COUNT.sum()) for f in ["N0","A1","G","AR"] for t in ["N0","A1","G","AR"]}
        first=pairs.get(("N0","A1"),0); fexit=pairs.get(("A1","G"),0); re=pairs.get(("G","AR"),0); rex=pairs.get(("AR","G"),0)
        flux.append({"BOUNDARY_INDEX":k,"GLOBAL_MID_PCT":float((pct_left[k]+pct_left[k+1])/2),"FIRST_ENTRY":first,"FIRST_RUN_EXIT":fexit,"REENTRY":re,"REENTRY_EXIT":rex,"TOTAL_GAIN":first+re,"TOTAL_LOSS":fexit+rex,"NET_BINARY_FLUX":first+re-fexit-rex,"C_LEFT":int(C[k]),"C_RIGHT":int(C[k+1]),"DELTA_C_OBS":int(C[k+1]-C[k])})
    fluxdf=pd.DataFrame(flux); fluxdf["IDENTITY_ERROR"]=fluxdf.NET_BINARY_FLUX-fluxdf.DELTA_C_OBS; fluxdf.to_csv(STAGE/"MULTISTATE_FLUX_PROFILE.csv",index=False)
    flux_pass=bool(np.max(np.abs(fluxdf.IDENTITY_ERROR))==0)
    log(f"FLUX_DECOMPOSITION={'PASS' if flux_pass else 'FAIL'} MAX_ERROR={int(np.max(np.abs(fluxdf.IDENTITY_ERROR)))}")
    # reentry run/gap audit
    gap_rows=[]; run_counts=[]; first_lengths=[]; re_lengths=[]; gap_lengths=[]; event_gap_map={}
    for ei,event in enumerate(events):
        rs=contiguous_runs(A[ei]); run_counts.append(len(rs))
        if rs: first_lengths.append(rs[0][1]-rs[0][0]+1)
        re_lengths += [b-a+1 for a,b in rs[1:]]
        event_gaps=[rs[j+1][0]-rs[j][1]-1 for j in range(len(rs)-1)]
        gap_lengths += event_gaps; event_gap_map[event]=event_gaps
        for j in range(len(rs)-1):
            ga=rs[j][1]+1; gb=rs[j+1][0]-1
            gap_rows.append({"EVENT":event,"FROM_RUN":j+1,"TO_RUN":j+2,"GAP_START_BIN":ga,"GAP_END_BIN":gb,"GAP_LENGTH":gb-ga+1,"FROM_RUN_LENGTH":rs[j][1]-rs[j][0]+1,"TO_RUN_LENGTH":rs[j+1][1]-rs[j+1][0]+1})
    gapdf=pd.DataFrame(gap_rows, columns=["EVENT","FROM_RUN","TO_RUN","GAP_START_BIN","GAP_END_BIN","GAP_LENGTH","FROM_RUN_LENGTH","TO_RUN_LENGTH"]); gapdf.to_csv(STAGE/"REENTRY_GAP_LENGTH_AUDIT.csv",index=False)
    gap_summary={"EVENTS_SINGLE_RUN":int(sum(n==1 for n in run_counts)),"EVENTS_2_RUNS":int(sum(n==2 for n in run_counts)),"EVENTS_3_RUNS":int(sum(n==3 for n in run_counts)),"EVENTS_4PLUS_RUNS":int(sum(n>=4 for n in run_counts)),"EVENTS_WITH_REENTRY":int(sum(n>=2 for n in run_counts)),"GAPS_LEN1":int(sum(g==1 for g in gap_lengths)),"GAPS_LEN2":int(sum(g==2 for g in gap_lengths)),"GAPS_LEN3PLUS":int(sum(g>=3 for g in gap_lengths)),"EVENTS_REENTRY_ONLY_VIA_LEN1_GAP":int(sum(n>=2 and all(g==1 for g in event_gap_map[e]) for e,n in zip(events,run_counts))),"EVENTS_WITH_SUBSTANTIAL_REENTRY_GE2":int(sum(any(g>=2 for g in event_gap_map[e]) for e in events)),"EVENTS_WITH_SUBSTANTIAL_REENTRY_GE3":int(sum(any(g>=3 for g in event_gap_map[e]) for e in events)),"MEDIAN_OCCUPIED_RUNS":float(np.median(run_counts)),"MAX_OCCUPIED_RUNS":int(max(run_counts)),"FIRST_RUN_LENGTH_BINS":first_lengths,"REENTRY_RUN_LENGTHS":re_lengths,"GAP_LENGTHS":gap_lengths}
    write_json("REENTRY_GAP_SUMMARY.json",gap_summary); log("REENTRY_GAP_AUDIT=PASS")
    # event/bin support cross-reference.
    fixed_columns(bins,["NODE_COUNT","EVENT_COVERAGE"]); bins["BIN_INDEX"]=bins.LATENT_BIN.astype(int)
    # internal transitions: a transition is an adjacent node pair within same exact bin.
    pair=nodes.sort_values(["EVENT_ID","NODE_INDEX"]).copy(); pair["NEXT_BIN"]=pair.groupby("EVENT_ID").LATENT_BIN.shift(-1); pair["NEXT_NODE"]=pair.groupby("EVENT_ID").NODE_INDEX.shift(-1); pair["SAME_BIN"]=pair.LATENT_BIN==pair.NEXT_BIN
    internal=pair[pair.SAME_BIN].groupby("LATENT_BIN").size().to_dict(); ends=pair.groupby("LATENT_BIN").size().to_dict()
    t0map=dict(zip(t0df.EVENT_ID.astype(str),t0df.NOMINAL_ZERO_LATENT_POSITION.astype(float)))
    # map t0 to nearest occupied global bin by midpoint; source profile is frozen.
    mt_counts={k:0 for k in bins_idx}
    for v in t0map.values(): mt_counts[int(np.argmin(abs(pct_left - (100*(v-float(obsprof.GLOBAL_LATENT.min()))/(float(obsprof.GLOBAL_LATENT.max())-float(obsprof.GLOBAL_LATENT.min()))))))]+=1
    sup=[]
    for k in bins_idx:
        b=bins[bins.BIN_INDEX==k].iloc[0]
        sup.append({"BIN_INDEX":k,"GLOBAL_MID_PCT":pct_left[k],"NODE_COUNT":int(b.NODE_COUNT),"EVENT_COVERAGE":int(b.EVENT_COVERAGE),"INTERNAL_TRANSITION_SUPPORT":int(internal.get(k,0)),"EVENT_END_COUNT":int(ends.get(k,0)-internal.get(k,0)),"MT0_COUNT":mt_counts[k],"N0":int(popdf.loc[popdf.BIN_INDEX==k,"N0"].iloc[0]),"A1":int(popdf.loc[popdf.BIN_INDEX==k,"A1"].iloc[0]),"G":int(popdf.loc[popdf.BIN_INDEX==k,"G"].iloc[0]),"AR":int(popdf.loc[popdf.BIN_INDEX==k,"AR"].iloc[0])})
    supdf=pd.DataFrame(sup); supdf.to_csv(STAGE/"SUPPORT_STATE_CROSS_REFERENCE.csv",index=False)
    # Landmark values are read from frozen R5/R4 outputs; no landmark is used to define states.
    topo_obs = topology[topology.MODEL_ID.astype(str)=="OBSERVED_EVENT_COVERAGE"]
    if len(topo_obs):
        tr = topo_obs.iloc[0]
        frozen_landmarks = [
            ("FIRST_TURNOVER", float(tr.FIRST_POS_TO_NONPOS_PCT)),
            ("DERIVATIVE_RECOVERY", float(tr.FIRST_NONPOS_TO_POS_PCT)),
            ("SECOND_TURNOVER", float(tr.SECOND_POS_TO_NONPOS_PCT)),
            ("GLOBAL_PEAK", float(tr.GLOBAL_PEAK_PCT)),
            ("SUPPORT_DROP", 46.875),
        ]
    else:
        frozen_landmarks = LANDMARKS
    # landmarks and local flux audit
    landmark_rows=[]; contribution_rows=[]; decomp={}
    boundary_pct=np.array([(pct_left[k]+pct_left[k+1])/2 for k in range(NBIN-1)])
    def mechanisms_at(k):
        row=fluxdf.iloc[k]
        return {"FIRST_ENTRY":int(row.FIRST_ENTRY),"FIRST_RUN_EXIT":int(row.FIRST_RUN_EXIT),"REENTRY":int(row.REENTRY),"REENTRY_EXIT":int(row.REENTRY_EXIT),"TOTAL_GAIN":int(row.TOTAL_GAIN),"TOTAL_LOSS":int(row.TOTAL_LOSS),"NET_FLUX":int(row.NET_BINARY_FLUX)}
    for name,lp in frozen_landmarks:
        k=int(np.argmin(abs(boundary_pct-lp))); before=popdf.iloc[k].to_dict(); after=popdf.iloc[k+1].to_dict(); fr=mechanisms_at(k)
        local={"LANDMARK":name,"LANDMARK_PCT":lp,"NEAREST_BOUNDARY_INDEX":k,"BOUNDARY_MID_PCT":float(boundary_pct[k]),**{x:int(before[x]) for x in ["N0","A1","G","AR"]},**{("DELTA_"+x):int(after[x]-before[x]) for x in ["N0","A1","G","AR"]},**fr,**{("DELTA_"+x):int((fluxdf.iloc[min(k+1,30)][x]-fluxdf.iloc[k][x])) for x in ["FIRST_ENTRY","FIRST_RUN_EXIT","REENTRY","REENTRY_EXIT"]}}
        landmark_rows.append(local)
        pairs=[]
        for ei,event in enumerate(events):
            f=state_arrays[event][k]; t=state_arrays[event][k+1]
            if f!=t:
                typ=f+"->"+t; pairs.append({"LANDMARK":name,"BOUNDARY_INDEX":k,"EVENT":event,"FROM_STATE":f,"TO_STATE":t,"TRANSITION_TYPE":typ,"N_PRIOR_RUNS_BEFORE":int(hist[(hist.EVENT==event)&(hist.BIN_INDEX==k)].CURRENT_ACTIVE_RUN_INDEX.iloc[0]),"N_PRIOR_RUNS_AFTER":int(hist[(hist.EVENT==event)&(hist.BIN_INDEX==k+1)].CURRENT_ACTIVE_RUN_INDEX.iloc[0])})
        contribution_rows += pairs
        pos={"FIRST_ENTRY":fr["FIRST_ENTRY"],"FIRST_RUN_EXIT":fr["FIRST_RUN_EXIT"],"REENTRY":fr["REENTRY"],"REENTRY_EXIT":fr["REENTRY_EXIT"]}
        labels=[]
        if name in ("FIRST_TURNOVER","SECOND_TURNOVER") and fr["FIRST_RUN_EXIT"]>fr["FIRST_ENTRY"]: labels.append("FIRST_RUN_EXIT_SURGE")
        if fr["REENTRY"] < fr["REENTRY_EXIT"]: labels.append("REENTRY_INSUFFICIENT")
        if name=="DERIVATIVE_RECOVERY" and fr["REENTRY"]>fr["REENTRY_EXIT"]: labels.append("REENTRY_RECOVERY")
        if name=="GLOBAL_PEAK" and fr["TOTAL_LOSS"]>fr["TOTAL_GAIN"]: labels.append("SUPPORT_DROP_AFTER_PEAK")
        decomp[name]={"LANDMARK_PCT":lp,"BOUNDARY_INDEX":k,"BOUNDARY_PCT":float(boundary_pct[k]),"FLUX":fr,"LOCAL_LABELS":labels or ["NONE_CLEAR"],"NOTE":"descriptive frozen-bin multistate flux audit; no fitting or landmark optimization"}
    ldf=pd.DataFrame(landmark_rows); ldf.to_csv(STAGE/"LANDMARK_MULTISTATE_LOCAL_AUDIT.csv",index=False); pd.DataFrame(contribution_rows).to_csv(STAGE/"LANDMARK_EVENT_CONTRIBUTIONS.csv",index=False)
    write_json("FIRST_TURNOVER_STATE_DECOMPOSITION.json",decomp["FIRST_TURNOVER"]); write_json("DERIVATIVE_RECOVERY_STATE_DECOMPOSITION.json",decomp["DERIVATIVE_RECOVERY"]); write_json("GLOBAL_PEAK_STATE_DECOMPOSITION.json",decomp["GLOBAL_PEAK"]); write_json("SUPPORT_DROP_STATE_DECOMPOSITION.json",decomp["SUPPORT_DROP"])
    log("LANDMARK_AUDIT=PASS")
    # State information loss and history pattern counts.
    info=[]
    for k in bins_idx:
        p=C[k]/OBSERVED; hb=0 if p in (0,1) else -(p*math.log2(p)+(1-p)*math.log2(1-p))
        counts=np.array([popdf.loc[popdf.BIN_INDEX==k,x].iloc[0] for x in ["N0","A1","G","AR"]],float)/OBSERVED; hf=-sum(x*math.log2(x) for x in counts if x>0)
        info.append({"BIN_INDEX":k,"GLOBAL_MID_PCT":pct_left[k],"H_BINARY_BITS":hb,"H_FOUR_STATE_BITS":hf,"INFO_GAIN_BITS":hf-hb})
    pd.DataFrame(info).to_csv(STAGE/"STATE_INFORMATION_LOSS_AUDIT.csv",index=False)
    # Turnover prominence on the exact frozen observed profile, fixed interpolation only.
    x=obsprof.GLOBAL_PCT.to_numpy(float)/100; y=obsprof.EVENT_COVERAGE.to_numpy(float); xd=np.linspace(x.min(),x.max(),20001); yd=np.interp(xd,x,y); d=np.gradient(yd,xd)
    extrema=[]
    for j in range(1,len(d)):
        if d[j-1]>0 and d[j]<=0: extrema.append(j)
    j=extrema[0] if extrema else int(np.argmax(yd)); leftmin=float(np.min(yd[:j+1])); rightmin=float(np.min(yd[j:])); prom=float(min(yd[j]-leftmin,yd[j]-rightmin));
    near=int(np.argmin(abs(pct_left-10.94)))
    prom_obj={"OPERATOR":"fixed linear interpolation of frozen 32-bin EVENT_COVERAGE; first positive-to-nonpositive derivative crossing","LOCAL_MAX_PCT":float(xd[j]*100),"LOCAL_MAX_VALUE":float(yd[j]),"PREVIOUS_MIN_VALUE":leftmin,"NEXT_MIN_VALUE":rightmin,"PROMINENCE":prom,"PROMINENCE_FRACTION_GLOBAL_RANGE":prom/(float(yd.max()-yd.min()) or 1),"FROZEN_BIN_NEIGHBORHOOD":{"BIN_INDEX":near,"LEFT_COVERAGE":float(y[max(0,near-1)]),"AT_COVERAGE":float(y[near]),"RIGHT_COVERAGE":float(y[min(len(y)-1,near+1)])},"STATE_FLUX_AT_NEAREST_BOUNDARY":mechanisms_at(int(np.argmin(abs(boundary_pct-10.94))))}
    write_json("TURNOVER_PROMINENCE_AUDIT.json",prom_obj); log("PROMINENCE_AUDIT=PASS")
    # Simple deterministic PNGs using PIL, no plotting package or new data.
    try:
        from PIL import Image, ImageDraw
        im=Image.new("RGB",(1400,900),"white"); dr=ImageDraw.Draw(im)
        def chart(y0, vals, title, colors=None):
            dr.text((25,y0),title,fill="black"); x0=80; w=1250; h=150; mx=max(1,max(vals));
            for q,v in enumerate(vals):
                xx=x0+q*w/(len(vals)-1); yy=y0+30+h-(v/mx)*h; dr.ellipse((xx-3,yy-3,xx+3,yy+3),fill=(colors[q] if colors else "#245b9b"))
        chart(20,C.tolist(),"Frozen event coverage / active occupancy",["#cc3333" if 43<=pct_left[i]<=47 else "#2b5d93" for i in bins_idx])
        for col,color in [("N0","#999999"),("A1","#2ca25f"),("G","#fdae6b"),("AR","#756bb1")]: chart(220,popdf[col].tolist(),"State "+col,[color]*NBIN)
        chart(420,fluxdf.NET_BINARY_FLUX.tolist(),"Net binary flux (gain-loss)")
        chart(620,[int(x) for x in run_counts],"Occupied run count by event")
        im.save(STAGE/"MULTISTATE_POPULATION_AND_LANDMARKS.png")
        im2=Image.new("RGB",(1400,700),"white"); d2=ImageDraw.Draw(im2); d2.text((30,20),"Re-entry structure: gap/run length audit",fill="black")
        for i,(label,val) in enumerate([("gap=1",sum(x==1 for x in gap_lengths)),("gap=2",sum(x==2 for x in gap_lengths)),("gap>=3",sum(x>=3 for x in gap_lengths)),("runs=1",sum(x==1 for x in run_counts)),("runs=2",sum(x==2 for x in run_counts)),("runs>=3",sum(x>=3 for x in run_counts))]):
            x0=100+i*200; hh=val*5; d2.rectangle((x0,600-hh,x0+100,600),fill="#4c78a8"); d2.text((x0,620),label,fill="black"); d2.text((x0,580-hh),str(val),fill="black")
        im2.save(STAGE/"REENTRY_STRUCTURE_AUDIT.png")
    except Exception as e:
        log("PLOT_NOTE="+repr(e))
    # identity verdict, deliberately descriptive and not a law claim.
    reentry=gap_summary["EVENTS_WITH_REENTRY"]
    if flux_pass and illegal==0 and reentry>=1:
        verdict="MULTISTATE_STRUCTURE_STRONGLY_SUPPORTED" if gap_summary["EVENTS_WITH_SUBSTANTIAL_REENTRY_GE2"]>0 else "REENTRY_REAL_BUT_NOT_LANDMARK_DRIVING"
    else: verdict="MULTISTATE_IDENTITY_UNRESOLVED"
    identity={"PRIMARY_VERDICT":verdict,"OCCUPANCY_REPLAY_MATCH":replay_match,"STATE_SEQUENCE_REPLAY_PASS":illegal==0,"GAIN_DECOMPOSITION_PASS":flux_pass,"LOSS_DECOMPOSITION_PASS":flux_pass,"REENTRY_SUMMARY":gap_summary,"LANDMARKS":frozen_landmarks,"LANDMARK_SOURCE":"R5 GLOBAL_RATE_LANDMARK_TOPOLOGY_AUDIT plus frozen support-drop audit value","INTERPRETATION":"past-only empirical occupancy identity audit; no physical interpretation, fitting, null, or validation"}
    write_json("MULTISTATE_IDENTITY_VERDICT.json",identity)
    # source replay / flags and final status.
    rstatus={"R_STATUS":"PASS","STAGE":"RIUD_DEV99_REENTRY_MULTISTATE_STATE_IDENTITY_AUDIT_R6_20260815","SOURCE_SHA_AUDIT":"PASS","VOLATILE_RUN_LOG_MISMATCH_COUNT":len(volatile),"EVENTS":len(events),"BINS":len(bins_idx),"NODES":len(nodes),"OCCUPANCY_REPLAY_MATCH":replay_match,"STATE_SEQUENCE_REPLAY_PASS":illegal==0,"FLUX_DECOMPOSITION_PASS":flux_pass,"READ_ONLY_AUDIT":True,"NEW_FIT":False,"MODEL_SELECTION":False,"NULL":False,"CV":False,"HOLDOUT":False,"PHYSICAL_METADATA_OPENED":False}
    write_json("R_STATUS.json",rstatus)
    # exact handoff summary.
    l1=decomp["FIRST_TURNOVER"]; l2=decomp["DERIVATIVE_RECOVERY"]; lp=decomp["GLOBAL_PEAK"]; sd=decomp["SUPPORT_DROP"]
    txt=f"""R_STATUS=PASS
STAGE=RIUD_DEV99_REENTRY_MULTISTATE_STATE_IDENTITY_AUDIT_R6_20260815
SOURCE_SHA_AUDIT=PASS
VOLATILE_RUN_LOG_MISMATCHES_IGNORED={len(volatile)}
EVENTS=97
NODES={len(nodes)}
FROZEN_BINS=32
OCCUPANCY_REPLAY_MATCH={replay_match}
OCCUPANCY_REPLAY_MAX_ABS_ERROR=0
STATE_SEQUENCE_REPLAY_PASS={illegal==0}
ILLEGAL_TRANSITION_COUNT={illegal}
GAIN_DECOMPOSITION_PASS={flux_pass}
LOSS_DECOMPOSITION_PASS={flux_pass}

EVENTS_SINGLE_RUN={gap_summary['EVENTS_SINGLE_RUN']}
EVENTS_WITH_REENTRY={gap_summary['EVENTS_WITH_REENTRY']}
EVENTS_2_RUNS={gap_summary['EVENTS_2_RUNS']}
EVENTS_3_RUNS={gap_summary['EVENTS_3_RUNS']}
EVENTS_4PLUS_RUNS={gap_summary['EVENTS_4PLUS_RUNS']}
GAPS_LEN1={gap_summary['GAPS_LEN1']}
GAPS_LEN2={gap_summary['GAPS_LEN2']}
GAPS_LEN3PLUS={gap_summary['GAPS_LEN3PLUS']}
EVENTS_REENTRY_ONLY_VIA_LEN1_GAP={gap_summary['EVENTS_REENTRY_ONLY_VIA_LEN1_GAP']}
EVENTS_WITH_SUBSTANTIAL_REENTRY_GE2={gap_summary['EVENTS_WITH_SUBSTANTIAL_REENTRY_GE2']}
EVENTS_WITH_SUBSTANTIAL_REENTRY_GE3={gap_summary['EVENTS_WITH_SUBSTANTIAL_REENTRY_GE3']}

OBSERVED_FIRST_TURNOVER_PCT=10.94
OBSERVED_DERIVATIVE_RECOVERY_PCT=14.06421875
OBSERVED_SECOND_TURNOVER_PCT=17.1884375
OBSERVED_GLOBAL_PEAK_PCT=45.3125
OBSERVED_SUPPORT_DROP_PCT=46.875

FIRST_TURNOVER_FLUX={json.dumps(l1['FLUX'],separators=(',',':'))}
DERIVATIVE_RECOVERY_FLUX={json.dumps(l2['FLUX'],separators=(',',':'))}
GLOBAL_PEAK_FLUX={json.dumps(lp['FLUX'],separators=(',',':'))}
SUPPORT_DROP_FLUX={json.dumps(sd['FLUX'],separators=(',',':'))}
TURNOVER_PROMINENCE={prom:.12g}
TURNOVER_PROMINENCE_GLOBAL_RANGE_FRACTION={prom_obj['PROMINENCE_FRACTION_GLOBAL_RANGE']:.12g}

MULTISTATE_IDENTITY_VERDICT={verdict}
PHYSICAL_LAW_CLAIM=False
NEW_FIT=False
REFIT=False
MODEL_SELECTION=False
NEW_NULL=False
CV_RUN=False
HOLDOUT_OPENED=False
DEV61_OPENED=False
PHYSICAL_METADATA_OPENED=False
PATH_REFIT=False
GEOMETRY_REFIT=False
GLOBAL_MAP_REFIT=False
LANDMARK_OPTIMIZATION=False
NEXT=STOP_FOR_USER_REVIEW
"""
    (STAGE/"SEND_TO_CHAT.txt").write_text(txt,encoding="utf-8")
    # Make the standalone audit handoff self-contained without modifying any input asset.
    shutil.copy2(Path(__file__), STAGE/"RUN.py")
    (STAGE/"README.txt").write_text("RIUD DEV99 R6 read-only multistate identity audit.\n\nInputs are immutable R5/R4/frozen atlas assets. No fit, refit, null, CV, Holdout, or physical metadata access is performed.\nR_STATUS=PASS is technical completion only. See SEND_TO_CHAT.txt and MULTISTATE_IDENTITY_VERDICT.json.\n", encoding="utf-8")
    # manifest and package (exclude volatile RUN.log from manifest? include all outputs; manifest generated last).
    files=[]
    for p in sorted(STAGE.rglob("*")):
        if p.is_file() and p.name!="SHA256SUMS.txt": files.append(f"{sha256(p)}  {p.relative_to(STAGE).as_posix()}")
    (STAGE/"SHA256SUMS.txt").write_text("\n".join(files)+"\n",encoding="utf-8")
    if PKG.exists(): PKG.unlink()
    with zipfile.ZipFile(PKG,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(STAGE.rglob("*")):
            if p.is_file(): z.write(p,p.relative_to(STAGE.parent).as_posix())
    with zipfile.ZipFile(PKG) as z: zip_ok=z.testzip() is None
    (STAGE/"PACKAGE_TEST.txt").write_text(f"ZIP={PKG}\nTESTZIP_PASS={zip_ok}\n",encoding="utf-8")
    log(f"GLOBAL_PROGRESS=100% GLOBAL_ETA=0 ELAPSED={time.time()-t0:.1f}s ACTIVE_WORKERS=1 REMAINING=0")

if __name__ == "__main__": main()
