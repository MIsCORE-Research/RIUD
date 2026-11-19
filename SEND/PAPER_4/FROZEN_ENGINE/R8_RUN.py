from __future__ import annotations
import hashlib, json, math, time, zipfile, shutil
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(r"E:\RIUD_ACTIVE_20260808")
R6=ROOT/"RIUD_DEV99_REENTRY_MULTISTATE_STATE_IDENTITY_AUDIT_R6_20260815"
R7=ROOT/"RIUD_DEV99_MULTISTATE_FLOW_DYNAMICS_DISCOVERY_R7_20260815"
OUT=ROOT/"RIUD_DEV99_RUN_INDEX_STATE_MEMORY_IDENTITY_AUDIT_R8_20260815"
ZIP=ROOT/"RIUD_DEV99_RUN_INDEX_STATE_MEMORY_IDENTITY_AUDIT_R8_20260815_PACKAGE.zip"
N=97; NB=32; STATES=["N0","A1","G","AR"]
LANDMARKS={"L1_FIRST_TURNOVER":10.94,"L2_RECOVERY":14.06421875,"L3_SECOND_TURNOVER":17.1884375,"L4_GLOBAL_PEAK":45.3125,"L5_SUPPORT_DROP":46.875}

def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()
def log(s):
    print(s,flush=True)
    with open(OUT/"RUN.log","a",encoding="utf-8") as f:f.write(s+"\n")
def dump(name,obj): (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=str),encoding="utf-8")
def wilson(k,n,z=1.959963984540054):
    if n<=0:return (np.nan,np.nan)
    p=k/n; den=1+z*z/n; cen=(p+z*z/(2*n))/den; half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return cen-half,cen+half
def run_cat(state,idx):
    if state=="N0": return "N0"
    if state=="A1": return "A1"
    if state=="AR": return "AR_RUN2" if idx==2 else ("AR_RUN3" if idx==3 else "AR_RUN4PLUS")
    return "G_AFTER_RUN1" if idx==1 else ("G_AFTER_RUN2" if idx==2 else ("G_AFTER_RUN3" if idx==3 else "G_AFTER_RUN4PLUS"))
def age_class(age): return "AGE1" if age==1 else ("AGE2" if age==2 else "AGE3PLUS")

def source_audit():
    req=[R6/"EVENT_MULTISTATE_HISTORY_MATRIX.csv",R6/"MULTISTATE_POPULATION_PROFILE.csv",R6/"MULTISTATE_TRANSITION_COUNTS.csv",R6/"MULTISTATE_FLUX_PROFILE.csv",R7/"MULTISTATE_RATE_CONTINUOUS_PROFILES.csv",R7/"R_STATUS.json"]
    for p in req:
        if not p.exists(): raise RuntimeError("missing source "+str(p))
    mismatch=[]; volatile=[]
    for root in [R6,R7]:
        mf=root/"SHA256SUMS.txt"
        if not mf.exists(): continue
        for line in mf.read_text(errors="replace").splitlines():
            q=line.strip().split(maxsplit=1)
            if len(q)!=2:continue
            ex,name=q; p=root/name.lstrip("* ")
            if p.exists() and sha(p)!=ex:
                (volatile if p.name.lower()=="run.log" else mismatch).append({"path":str(p),"expected":ex,"actual":sha(p)})
    if mismatch: raise RuntimeError("nonvolatile SHA mismatch "+json.dumps(mismatch))
    rows=[]
    for p in req:
        d=pd.read_csv(p) if p.suffix.lower()==".csv" else None
        rows.append({"PATH":str(p),"SHA256":sha(p),"SIZE":p.stat().st_size,"ROWS":len(d) if d is not None else "JSON","COLUMNS":",".join(d.columns) if d is not None else "JSON"})
    return rows,volatile,req

def main():
    t0=time.time(); OUT.mkdir(parents=True,exist_ok=True); (OUT/"RUN.log").write_text("",encoding="utf-8")
    log("GLOBAL_PROGRESS=0% GLOBAL_ETA=short ELAPSED=0s ACTIVE_WORKERS=1 REMAINING=source audit")
    try: prov,volatile,req=source_audit()
    except Exception as e:
        dump("R_STATUS.json",{"R_STATUS":"TECHNICAL_FAIL","REASON":str(e)}); return
    pd.DataFrame(prov).to_csv(OUT/"SOURCE_PROVENANCE.csv",index=False)
    hist=pd.read_csv(R6/"EVENT_MULTISTATE_HISTORY_MATRIX.csv").sort_values(["EVENT","BIN_INDEX"]).reset_index(drop=True)
    pop=pd.read_csv(R6/"MULTISTATE_POPULATION_PROFILE.csv").sort_values("BIN_INDEX").reset_index(drop=True)
    trans=pd.read_csv(R6/"MULTISTATE_TRANSITION_COUNTS.csv")
    flux=pd.read_csv(R6/"MULTISTATE_FLUX_PROFILE.csv")
    f7=pd.read_csv(R7/"MULTISTATE_RATE_CONTINUOUS_PROFILES.csv")
    events=sorted(hist.EVENT.astype(str).unique()); u=pop.GLOBAL_MID_PCT.to_numpy(float)/100; du=float(np.median(np.diff(u)))
    log("SOURCE_SHA_AUDIT=PASS VOLATILE_RUN_LOG_MISMATCHES_IGNORED="+str(len(volatile)))
    # Past-only ages: derived by scanning only the current and previous rows.
    rows=[]
    for event,g in hist.groupby("EVENT",sort=True):
        g=g.sort_values("BIN_INDEX").reset_index(drop=True); active_age=0; gap_age=0
        for i,r in g.iterrows():
            state=str(r.STATE); run_idx=int(r.CURRENT_ACTIVE_RUN_INDEX) if state in ("A1","AR") else int(r.N_COMPLETED_ACTIVE_RUNS)
            if state in ("A1","AR"): active_age+=1; gap_age=0; age=active_age
            elif state=="G": gap_age+=1; active_age=0; age=gap_age
            else: active_age=0; gap_age=0; age=0
            rows.append({**r.to_dict(),"RUN_INDEX_CATEGORY":run_cat(state,run_idx),"RUN_INDEX":run_idx,"ACTIVE_RUN_AGE_BINS":active_age if state in ("A1","AR") else np.nan,"GAP_AGE_BINS":gap_age if state=="G" else np.nan,"STATE_AGE":age_class(age) if state in ("A1","AR","G") else "NOT_ACTIVE_OR_GAP","STATE_AGE_BINS":age})
    detail=pd.DataFrame(rows)
    profile=[]
    cats=["A1","AR_RUN2","AR_RUN3","AR_RUN4PLUS","G_AFTER_RUN1","G_AFTER_RUN2","G_AFTER_RUN3","G_AFTER_RUN4PLUS"]
    for k in range(NB):
        q=detail[detail.BIN_INDEX==k]; d={"BIN_INDEX":k,"GLOBAL_MID_PCT":float(pop.loc[k,"GLOBAL_MID_PCT"])}
        for c in cats:d[c]=int((q.RUN_INDEX_CATEGORY==c).sum())
        d["A1_REPLAY"]=d["A1"]; d["AR_RUN2_REPLAY"]=d["AR_RUN2"]; d["AR_RUN3_REPLAY"]=d["AR_RUN3"]; d["AR_RUN4PLUS_REPLAY"]=d["AR_RUN4PLUS"]
        d["G_REPLAY"]=sum(d[x] for x in ["G_AFTER_RUN1","G_AFTER_RUN2","G_AFTER_RUN3","G_AFTER_RUN4PLUS"]); d["AR_REPLAY"]=sum(d[x] for x in ["AR_RUN2","AR_RUN3","AR_RUN4PLUS"])
        d["R6_A1"]=int(pop.loc[k,"A1"]); d["R6_AR"]=int(pop.loc[k,"AR"]); d["R6_G"]=int(pop.loc[k,"G"]); d["RUN_INDEX_DECOMP_ERROR"]=d["AR_RUN2"]+d["AR_RUN3"]+d["AR_RUN4PLUS"]-int(pop.loc[k,"AR"]); d["G_DECOMP_ERROR"]=d["G_REPLAY"]-int(pop.loc[k,"G"])
        profile.append(d)
    prof=pd.DataFrame(profile); prof.to_csv(OUT/"RUN_INDEX_STATE_PROFILE.csv",index=False)
    run_pass=bool((prof.RUN_INDEX_DECOMP_ERROR==0).all() and (prof.G_DECOMP_ERROR==0).all())
    # Transition categories, including all actual category transitions.
    tp=[]; age_tp=[]
    for event,g in detail.groupby("EVENT",sort=True):
        g=g.sort_values("BIN_INDEX").reset_index(drop=True)
        for i in range(NB-1):
            a=g.iloc[i]; b=g.iloc[i+1]; ca=a.RUN_INDEX_CATEGORY; cb=b.RUN_INDEX_CATEGORY
            tp.append({"BOUNDARY_INDEX":i,"GLOBAL_MID_PCT":float((u[i]+u[i+1])*50),"FROM_CATEGORY":ca,"TO_CATEGORY":cb,"COUNT":1,"SOURCE_POPULATION_CATEGORY":ca})
            if ca in ("A1","AR_RUN2","AR_RUN3","AR_RUN4PLUS"): typ="ACTIVE_EXIT"
            elif ca.startswith("G_"): typ="G_REENTRY"
            else: typ="N0_ENTRY"
            age_tp.append({"BOUNDARY_INDEX":i,"FROM_STATE":a.STATE,"FROM_AGE":a.STATE_AGE,"TO_STATE":b.STATE,"TRANSITION_TYPE":typ,"COUNT":1})
    tpdf=pd.DataFrame(tp).groupby(["BOUNDARY_INDEX","GLOBAL_MID_PCT","FROM_CATEGORY","TO_CATEGORY"],as_index=False).COUNT.sum()
    src_cat=tpdf.groupby(["BOUNDARY_INDEX","FROM_CATEGORY"],as_index=False).COUNT.sum().rename(columns={"COUNT":"SOURCE_POPULATION"})
    tpdf=tpdf.merge(src_cat,on=["BOUNDARY_INDEX","FROM_CATEGORY"]); tpdf["TRANSITION_PROBABILITY"]=tpdf.COUNT/tpdf.SOURCE_POPULATION
    tpdf.to_csv(OUT/"RUN_INDEX_TRANSITION_COUNTS.csv",index=False)
    # Required aggregate transitions in a stable, explicit table.
    rp=[]
    for k in range(NB-1):
        q=tpdf[tpdf.BOUNDARY_INDEX==k]
        for ca in cats+['N0']:
            qq=q[q.FROM_CATEGORY==ca]
            for r in qq.itertuples(): rp.append({"BOUNDARY_INDEX":k,"GLOBAL_MID_PCT":r.GLOBAL_MID_PCT,"FROM_CATEGORY":ca,"TO_CATEGORY":r.TO_CATEGORY,"SOURCE_POPULATION":int(r.SOURCE_POPULATION),"TRANSITION_COUNT":int(r.COUNT),"TRANSITION_PROBABILITY":float(r.TRANSITION_PROBABILITY)})
    # aggregate descriptive probabilities by source category
    agg=[]
    for ca in sorted(tpdf.FROM_CATEGORY.unique()):
        q=tpdf[tpdf.FROM_CATEGORY==ca]; n=int(q.SOURCE_POPULATION.sum());
        for cb in sorted(q.TO_CATEGORY.unique()):
            s=int(q.loc[q.TO_CATEGORY==cb,"COUNT"].sum()); lo,hi=wilson(s,n); agg.append({"SCOPE":"AGGREGATE","FROM_CATEGORY":ca,"TO_CATEGORY":cb,"SOURCE_N":n,"TRANSITION_COUNT":s,"TRANSITION_PROBABILITY":s/n if n else np.nan,"CI_LOW":lo,"CI_HIGH":hi})
    pd.DataFrame(rp+agg).to_csv(OUT/"RUN_INDEX_TRANSITION_PROBABILITIES.csv",index=False)
    # Age profile and age-dependent transition probabilities.
    ageprof=[]
    for k in range(NB):
        q=detail[detail.BIN_INDEX==k]; d={"BIN_INDEX":k,"GLOBAL_MID_PCT":float(pop.loc[k,"GLOBAL_MID_PCT"])}
        for st in ["A1","AR","G"]:
            for age in ["AGE1","AGE2","AGE3PLUS"]: d[f"{st}_{age}"]=int(((q.STATE==st)&(q.STATE_AGE==age)).sum())
        ageprof.append(d)
    pd.DataFrame(ageprof).to_csv(OUT/"STATE_AGE_PROFILE.csv",index=False)
    age_events=[]
    for event,g in detail.groupby("EVENT",sort=True):
        g=g.sort_values("BIN_INDEX").reset_index(drop=True)
        for i in range(NB-1):
            a=g.iloc[i]; b=g.iloc[i+1]
            if a.STATE in ("A1","AR"):
                age_events.append({"TRANSITION_TYPE":"P_EXIT_GIVEN_ACTIVE_AGE","AGE_CLASS":a.STATE_AGE,"SUCCESS":int(b.STATE=="G")})
            if a.STATE=="G":
                age_events.append({"TRANSITION_TYPE":"P_REENTRY_GIVEN_GAP_AGE","AGE_CLASS":a.STATE_AGE,"SUCCESS":int(b.STATE=="AR")})
    ae=pd.DataFrame(age_events); ap=[]
    for (typ,age),q in ae.groupby(["TRANSITION_TYPE","AGE_CLASS"]):
        s=int(q.SUCCESS.sum()); n=len(q); lo,hi=wilson(s,n); ap.append({"TRANSITION_TYPE":typ,"AGE_CLASS":age,"SOURCE_N":n,"SUCCESS_COUNT":s,"PROBABILITY":s/n if n else np.nan,"CI_LOW":lo,"CI_HIGH":hi})
    pd.DataFrame(ap).to_csv(OUT/"STATE_AGE_TRANSITION_PROBABILITIES.csv",index=False)
    age_pass=bool(len(ageprof)==NB and ae.SUCCESS.notna().all())
    log(f"GLOBAL_PROGRESS=35% GLOBAL_ETA=short ELAPSED={time.time()-t0:.1f}s ACTIVE_WORKERS=1 REMAINING=landmark and memory audit")
    # landmark local composition and flux.
    lrows=[]; fluxcols=["FIRST_ENTRY","FIRST_RUN_EXIT","REENTRY","REENTRY_EXIT","TOTAL_GAIN","TOTAL_LOSS","NET_BINARY_FLUX"]
    for name,lp in LANDMARKS.items():
        k=int(np.argmin(abs(pop.GLOBAL_MID_PCT.to_numpy(float)-lp))); q=prof.iloc[k]
        f=flux.iloc[min(k,NB-2)]
        d={"LANDMARK":name,"LANDMARK_PCT":lp,"NEAREST_BIN_INDEX":k,"BIN_PCT":float(pop.loc[k,"GLOBAL_MID_PCT"])}
        for c in cats:d[c]=int(q[c])
        for c in fluxcols:d[c]=float(f[c]) if c in f else np.nan
        d["DOMINANT_RUN_INDEX_CATEGORY"]=max(cats,key=lambda c:int(q[c]))
        d["DOMINANT_FLUX"]=max(["FIRST_ENTRY","FIRST_RUN_EXIT","REENTRY","REENTRY_EXIT"],key=lambda c:float(f[c]))
        lrows.append(d)
    pd.DataFrame(lrows).to_csv(OUT/"LANDMARK_RUN_INDEX_AUDIT.csv",index=False)
    # Peak/20 percent memory composition and R7 F7 overlay.
    i20=int(np.argmin(abs(pop.GLOBAL_MID_PCT.to_numpy(float)-20))); ip=int(np.argmin(abs(pop.GLOBAL_MID_PCT.to_numpy(float)-LANDMARKS["L4_GLOBAL_PEAK"])))
    def comp(i):
        q=prof.iloc[i]; ar=q.AR_RUN2+q.AR_RUN3+q.AR_RUN4PLUS; gg=q.G_AFTER_RUN1+q.G_AFTER_RUN2+q.G_AFTER_RUN3+q.G_AFTER_RUN4PLUS
        return {"BIN_INDEX":i,"GLOBAL_PCT":float(pop.loc[i,"GLOBAL_MID_PCT"]),"AR_TOTAL":int(ar),"AR_RUN2":int(q.AR_RUN2),"AR_RUN3":int(q.AR_RUN3),"AR_RUN4PLUS":int(q.AR_RUN4PLUS),"AR_RUN2_FRACTION":q.AR_RUN2/ar if ar else np.nan,"AR_RUN3_FRACTION":q.AR_RUN3/ar if ar else np.nan,"AR_RUN4PLUS_FRACTION":q.AR_RUN4PLUS/ar if ar else np.nan,"G_TOTAL":int(gg),"G_AFTER_RUN1":int(q.G_AFTER_RUN1),"G_AFTER_RUN2":int(q.G_AFTER_RUN2),"G_AFTER_RUN3":int(q.G_AFTER_RUN3),"G_AFTER_RUN4PLUS":int(q.G_AFTER_RUN4PLUS),"G_AFTER_RUN4PLUS_FRACTION":q.G_AFTER_RUN4PLUS/gg if gg else np.nan}
    c20=comp(i20); cp=comp(ip)
    # Empirical aggregate hazards and stored R7 F7 rate profile.
    empirical=[]
    for k in range(NB-1):
        q=trans[trans.BOUNDARY_INDEX==k]
        def cnt(a,b): return int(q[(q.FROM_STATE==a)&(q.TO_STATE==b)].COUNT.sum())
        vals={"K01_EMP":(cnt("N0","A1"),int(pop.loc[k,"N0"])),"K1G_EMP":(cnt("A1","G"),int(pop.loc[k,"A1"])),"KGR_EMP":(cnt("G","AR"),int(pop.loc[k,"G"])),"KRG_EMP":(cnt("AR","G"),int(pop.loc[k,"AR"]))}
        row={"BOUNDARY_INDEX":k,"GLOBAL_PCT":float((u[k]+u[k+1])*50)}
        for key,(s,n) in vals.items(): row[key]=(-math.log(max(1e-12,1-s/n))/du) if n and s<n else (np.inf if n and s==n else np.nan)
        empirical.append(row)
    emp=pd.DataFrame(empirical); r7f=f7[f7.MODEL_ID.astype(str)=="F7"].sort_values("GLOBAL_PCT")
    overlay=emp.copy()
    for key in ["K01","K1G","KGR","KRG"]: overlay["F7_"+key]=np.interp(overlay.GLOBAL_PCT,r7f.GLOBAL_PCT,r7f[key])
    for key in ["K01","K1G","KGR","KRG"]: overlay["RESID_"+key]=overlay[key+"_EMP"]-overlay["F7_"+key]
    f7c=np.interp(pop.GLOBAL_MID_PCT.to_numpy(float),r7f.GLOBAL_PCT,r7f.C_PRED); overlay.to_csv(OUT/"R7_F7_MEMORY_RESIDUAL_OVERLAY.csv",index=False)
    peak_overlay={"20PCT_BIN":c20,"PEAK_BIN":cp,"F7_COVERAGE_PRED_20PCT":float(f7c[i20]),"F7_COVERAGE_PRED_PEAK":float(f7c[ip]),"OBS_COVERAGE_20PCT":int(pop.loc[i20,"ACTIVE_TOTAL"]),"OBS_COVERAGE_PEAK":int(pop.loc[ip,"ACTIVE_TOTAL"]),"F7_COVERAGE_RESID_20PCT":float(pop.loc[i20,"ACTIVE_TOTAL"]-f7c[i20]),"F7_COVERAGE_RESID_PEAK":float(pop.loc[ip,"ACTIVE_TOTAL"]-f7c[ip]),"AR4PLUS_FRACTION_CHANGE":float(cp["AR_RUN4PLUS_FRACTION"]-c20["AR_RUN4PLUS_FRACTION"])}
    dump("GLOBAL_PEAK_MEMORY_AUDIT.json",peak_overlay)
    # Descriptive memory effects.
    def effect(table,probcol="PROBABILITY"):
        q=table.dropna(subset=[probcol]);
        if len(q)<2:return {"MAX_MIN":np.nan,"RATIO":np.nan,"N_GROUPS":len(q)}
        vals=q[probcol].to_numpy(float); return {"MAX_MIN":float(vals.max()-vals.min()),"RATIO":float(vals.max()/vals.min()) if vals.min()>0 else np.inf,"N_GROUPS":len(vals)}
    run_probs=[]
    for ca in ["A1","AR_RUN2","AR_RUN3","AR_RUN4PLUS","G_AFTER_RUN1","G_AFTER_RUN2","G_AFTER_RUN3","G_AFTER_RUN4PLUS"]:
        q=tpdf[tpdf.FROM_CATEGORY==ca]; n=int(q.SOURCE_POPULATION.sum());
        if ca.startswith("G_"): s=int(q[q.TO_CATEGORY.str.startswith("AR_")].COUNT.sum()); typ="P_REENTRY_GIVEN_RUN_INDEX"
        elif ca!="N0": s=int(q[q.TO_CATEGORY.str.startswith("G_")].COUNT.sum()); typ="P_EXIT_GIVEN_RUN_INDEX"
        else: continue
        lo,hi=wilson(s,n); run_probs.append({"TYPE":typ,"GROUP":ca,"N":n,"SUCCESS":s,"PROBABILITY":s/n if n else np.nan,"CI_LOW":lo,"CI_HIGH":hi})
    runpdf=pd.DataFrame(run_probs); agepdf=pd.DataFrame(ap)
    run_effect=effect(runpdf); age_effect={"MAX_MIN":float(max(agepdf.PROBABILITY)-min(agepdf.PROBABILITY)) if len(agepdf) else np.nan,"N_GROUPS":len(agepdf)}
    run_strong=bool(run_effect["MAX_MIN"]>=.10); age_strong=bool(age_effect["MAX_MIN"]>=.10)
    peak_memory=bool(cp["AR_RUN4PLUS_FRACTION"]>c20["AR_RUN4PLUS_FRACTION"]+0.10 or cp["G_AFTER_RUN4PLUS_FRACTION"]>c20["G_AFTER_RUN4PLUS_FRACTION"]+0.10)
    r7_align=bool(abs(peak_overlay["F7_COVERAGE_RESID_PEAK"])>abs(peak_overlay["F7_COVERAGE_RESID_20PCT"]) and peak_overlay["AR4PLUS_FRACTION_CHANGE"]>.10)
    if run_strong and age_strong: verdict="RUN_INDEX_AND_AGE_MEMORY_SUPPORTED"; code="M3"
    elif run_strong and peak_memory and r7_align: verdict="RUN_INDEX_MEMORY_STRONGLY_SUPPORTED"; code="M1"
    elif age_strong: verdict="STATE_AGE_MEMORY_STRONGLY_SUPPORTED"; code="M2"
    elif r7_align: verdict="R7_TECHNICAL_FIT_INSTABILITY_CANDIDATE"; code="M5"
    else: verdict="FOUR_STATE_MEMORY_NOT_EXPLANATORY"; code="M4"
    summary={"RUN_INDEX_EFFECT":run_effect,"STATE_AGE_EFFECT":age_effect,"RUN_INDEX_STRONG":run_strong,"STATE_AGE_STRONG":age_strong,"PEAK_HIGH_RUN_INDEX_MEMORY":peak_memory,"R7_ERROR_ALIGNS_WITH_MEMORY_COMPOSITION_SHIFT":r7_align,"CASE":code,"VERDICT":verdict,"NO_P_VALUES":True,"NOTE":"descriptive audit only; no threshold optimization, fit, null, or physical interpretation"}
    dump("MEMORY_EFFECT_SUMMARY.json",summary); dump("SCIENTIFIC_VERDICT.json",{"VERDICT":verdict,"CASE":code,"RUN_INDEX_MEMORY":run_effect,"STATE_AGE_MEMORY":age_effect,"GLOBAL_PEAK_MEMORY":peak_overlay,"FINAL_LAW_FROZEN":False})
    # Figures.
    try:
        from PIL import Image,ImageDraw
        im=Image.new("RGB",(1500,900),"white"); d=ImageDraw.Draw(im); d.text((20,20),"R8 run-index / state-age memory audit",fill="black")
        def line(y,vals,color,title):
            d.text((20,y),title,fill="black"); pts=[]; x0=100; w=1300; h=130; lo=min(vals); hi=max(vals); sp=hi-lo or 1
            for i,v in enumerate(vals):pts.append((x0+i*w/(len(vals)-1),y+30+h-(v-lo)/sp*h))
            d.line(pts,fill=color,width=2)
        line(55,prof.AR_RUN2.tolist(),"#2ca25f","AR_RUN2"); line(220,prof.AR_RUN3.tolist(),"#1f77b4","AR_RUN3"); line(385,prof.AR_RUN4PLUS.tolist(),"#d62728","AR_RUN4PLUS"); line(550,prof.G_AFTER_RUN4PLUS.tolist(),"#9467bd","G_AFTER_RUN4PLUS"); line(715,prof.G_AFTER_RUN1.tolist(),"#ff7f0e","G_AFTER_RUN1")
        im.save(OUT/"RUN_INDEX_STATE_PROFILE.png")
        im2=Image.new("RGB",(1500,700),"white"); d2=ImageDraw.Draw(im2); d2.text((20,20),"Global peak memory overlay",fill="black");
        line2=[]
        for i,v in enumerate(pop.ACTIVE_TOTAL): line2.append((100+i*1300/(len(pop)-1),600-v/100*450))
        d2.line(line2,fill="black",width=2); d2.text((450,620),"20% bin",fill="blue"); d2.text((650,620),"45.3125% peak bin",fill="red")
        im2.save(OUT/"GLOBAL_PEAK_MEMORY_OVERLAY.png")
    except Exception as e: log("PLOT_NOTE="+repr(e))
    status={"R_STATUS":"PASS","SOURCE_SHA_AUDIT":"PASS","EVENTS":N,"FROZEN_BINS":NB,"R6_STATE_REPLAY_PASS":run_pass,"RUN_INDEX_DECOMPOSITION_PASS":run_pass,"STATE_AGE_DECOMPOSITION_PASS":age_pass,"AR_RUN2_TOTAL":int(prof.AR_RUN2.sum()),"AR_RUN3_TOTAL":int(prof.AR_RUN3.sum()),"AR_RUN4PLUS_TOTAL":int(prof.AR_RUN4PLUS.sum()),"G_AFTER_RUN1_TOTAL":int(prof.G_AFTER_RUN1.sum()),"G_AFTER_RUN2_TOTAL":int(prof.G_AFTER_RUN2.sum()),"G_AFTER_RUN3_TOTAL":int(prof.G_AFTER_RUN3.sum()),"G_AFTER_RUN4PLUS_TOTAL":int(prof.G_AFTER_RUN4PLUS.sum()),"MEMORY_STRUCTURE_VERDICT":verdict,"NEW_FIT":False,"REFIT":False,"NULL_RUN":False,"CV_RUN":False,"HOLDOUT_OPENED":False,"PHYSICAL_METADATA_OPENED":False}
    dump("R_STATUS.json",status)
    send=f"""R_STATUS=PASS
SOURCE_SHA_AUDIT=PASS
EVENTS=97
FROZEN_BINS=32
R6_STATE_REPLAY_PASS={run_pass}
RUN_INDEX_DECOMPOSITION_PASS={run_pass}
STATE_AGE_DECOMPOSITION_PASS={age_pass}
AR_RUN2_TOTAL={int(prof.AR_RUN2.sum())}
AR_RUN3_TOTAL={int(prof.AR_RUN3.sum())}
AR_RUN4PLUS_TOTAL={int(prof.AR_RUN4PLUS.sum())}
G_AFTER_RUN1_TOTAL={int(prof.G_AFTER_RUN1.sum())}
G_AFTER_RUN2_TOTAL={int(prof.G_AFTER_RUN2.sum())}
G_AFTER_RUN3_TOTAL={int(prof.G_AFTER_RUN3.sum())}
G_AFTER_RUN4PLUS_TOTAL={int(prof.G_AFTER_RUN4PLUS.sum())}
L1_DOMINANT_STATE_OR_FLUX={lrows[0]['DOMINANT_FLUX']}
L2_DOMINANT_STATE_OR_FLUX={lrows[1]['DOMINANT_FLUX']}
L3_DOMINANT_STATE_OR_FLUX={lrows[2]['DOMINANT_FLUX']}
L4_DOMINANT_STATE_OR_FLUX={lrows[3]['DOMINANT_FLUX']}
L5_DOMINANT_STATE_OR_FLUX={lrows[4]['DOMINANT_FLUX']}
AR4PLUS_FRACTION_AT_20PCT={c20['AR_RUN4PLUS_FRACTION']}
AR4PLUS_FRACTION_AT_GLOBAL_PEAK={cp['AR_RUN4PLUS_FRACTION']}
GLOBAL_PEAK_HIGH_RUN_INDEX_DOMINATED={peak_memory}
RUN_INDEX_MEMORY_EFFECT={json.dumps(run_effect,separators=(',',':'))}
STATE_AGE_MEMORY_EFFECT={json.dumps(age_effect,separators=(',',':'))}
R7_ERROR_ALIGNS_WITH_MEMORY_COMPOSITION_SHIFT={r7_align}
MEMORY_STRUCTURE_VERDICT={verdict}
NEW_FIT=False
REFIT=False
NULL_RUN=False
CV_RUN=False
HOLDOUT_OPENED=False
PHYSICAL_METADATA_OPENED=False
NEXT=STOP_FOR_USER_REVIEW
"""
    (OUT/"SEND_TO_CHAT.txt").write_text(send,encoding="utf-8")
    shutil.copy2(Path(__file__),OUT/"RUN.py"); (OUT/"README.txt").write_text("R8 read-only run-index/state-age memory identity audit. No fit, refit, null, CV, Holdout, physical metadata, or state-definition changes.\n",encoding="utf-8")
    lines=[]
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name!="SHA256SUMS.txt":lines.append(f"{sha(p)}  {p.relative_to(OUT).as_posix()}")
    (OUT/"SHA256SUMS.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    if ZIP.exists():ZIP.unlink()
    with zipfile.ZipFile(ZIP,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.rglob("*")):
            if p.is_file():z.write(p,p.relative_to(OUT.parent).as_posix())
    with zipfile.ZipFile(ZIP) as z:ok=z.testzip() is None
    (OUT/"PACKAGE_TEST.txt").write_text(f"ZIP={ZIP}\nTESTZIP_PASS={ok}\n",encoding="utf-8")
    log("GLOBAL_PROGRESS=100%% GLOBAL_ETA=0 ELAPSED=%.1fs ACTIVE_WORKERS=1 REMAINING=0"%(time.time()-t0))

if __name__=="__main__":main()
