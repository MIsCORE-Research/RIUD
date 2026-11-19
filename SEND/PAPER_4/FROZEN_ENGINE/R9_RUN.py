from __future__ import annotations
import hashlib,json,math,shutil,time,zipfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import numpy as np
import pandas as pd
from scipy.optimize import minimize

ROOT=Path(r"E:\RIUD_ACTIVE_20260808")
R8=ROOT/"RIUD_DEV99_RUN_INDEX_STATE_MEMORY_IDENTITY_AUDIT_R8_20260815"
R7=ROOT/"RIUD_DEV99_MULTISTATE_FLOW_DYNAMICS_DISCOVERY_R7_20260815"
OUT=ROOT/"RIUD_DEV99_HISTORY_AWARE_MULTISTATE_FLOW_LAW_DISCOVERY_R9_20260815"
ZIP=ROOT/"RIUD_DEV99_HISTORY_AWARE_MULTISTATE_FLOW_LAW_DISCOVERY_R9_20260815_PACKAGE.zip"
N=97; NB=32; STATES=["N0","A1","G","AR"]
CATS=["N0","A1","AR_RUN2","AR_RUN3","AR_RUN4PLUS","G_AFTER_RUN1","G_AFTER_RUN2","G_AFTER_RUN3","G_AFTER_RUN4PLUS"]
LAND={"FIRST_TURNOVER":10.94,"RECOVERY":14.06421875,"SECOND_TURNOVER":17.1884375,"GLOBAL_PEAK":45.3125,"SUPPORT_DROP":46.875}
SEED=20260815; N_STARTS=128; WORKERS=16

def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()
def log(s):
    print(s,flush=True)
    with open(OUT/"RUN.log","a",encoding="utf-8") as f:f.write(s+"\n")
def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=str),encoding="utf-8")
def wilson(k,n,z=1.959963984540054):
    if n<=0:return np.nan,np.nan
    p=k/n; den=1+z*z/n; c=(p+z*z/(2*n))/den; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den; return c-h,c+h
def landmarks(u,y):
    x=np.linspace(float(np.min(u)),float(np.max(u)),20001); z=np.interp(x,u,y); d=np.gradient(z,x); pn=[]; npz=[]
    for i in range(1,len(d)):
        if d[i-1]>0 and d[i]<=0:pn.append(i)
        if d[i-1]<=0 and d[i]>0:npz.append(i)
    return {"FIRST_TURNOVER":float(x[pn[0]]*100) if pn else np.nan,"RECOVERY":float(x[npz[0]]*100) if npz else np.nan,"SECOND_TURNOVER":float(x[pn[1]]*100) if len(pn)>1 else np.nan,"GLOBAL_PEAK":float(x[np.argmax(z)]*100),"SIGN_SEQUENCE":"".join("+" if q>0 else "-" for q in d[::max(1,len(d)//200)])}
def cat_from_row(r):
    s=str(r.STATE); idx=int(r.CURRENT_ACTIVE_RUN_INDEX) if s in ("A1","AR") else int(r.N_COMPLETED_ACTIVE_RUNS)
    if s=="N0":return "N0"
    if s=="A1":return "A1"
    if s=="AR":return "AR_RUN2" if idx==2 else ("AR_RUN3" if idx==3 else "AR_RUN4PLUS")
    return "G_AFTER_RUN1" if idx==1 else ("G_AFTER_RUN2" if idx==2 else ("G_AFTER_RUN3" if idx==3 else "G_AFTER_RUN4PLUS"))
def mem_delta(model,cat,age,p):
    # p order: beta2,beta3,beta4,gamma2,gamma3,delta as applicable.
    i=0; d=0.0
    run=cat in ("AR_RUN2","AR_RUN3","AR_RUN4PLUS","G_AFTER_RUN2","G_AFTER_RUN3","G_AFTER_RUN4PLUS")
    run_level=2 if cat in ("AR_RUN2","G_AFTER_RUN2") else (3 if cat in ("AR_RUN3","G_AFTER_RUN3") else (4 if cat in ("AR_RUN4PLUS","G_AFTER_RUN4PLUS") else 1))
    if model in ("M1","M3","M4") and run_level>=2:
        d += p[0] if run_level==2 else (p[1] if run_level==3 else p[2]); i=3
    if model in ("M2","M3","M4") and cat!="N0":
        d += (p[i] if age=="AGE2" else (p[i+1] if age=="AGE3PLUS" else 0)); i+=2
    if model=="M4" and run_level>=4 and age=="AGE3PLUS": d += p[5]
    return d
def main():
    t0=time.time(); OUT.mkdir(parents=True,exist_ok=True); (OUT/"RUN.log").write_text("",encoding="utf-8")
    log("GLOBAL_PROGRESS=0% GLOBAL_ETA=short ELAPSED=0s ACTIVE_WORKERS=16 REMAINING=source audit")
    req=[R8/"RUN_INDEX_STATE_PROFILE.csv",R8/"RUN_INDEX_TRANSITION_PROBABILITIES.csv",R8/"STATE_AGE_PROFILE.csv",R8/"STATE_AGE_TRANSITION_PROBABILITIES.csv",R8/"R_STATUS.json",R7/"MULTISTATE_RATE_CONTINUOUS_PROFILES.csv"]
    if any(not p.exists() for p in req): dump("R_STATUS.json",{"R_STATUS":"TECHNICAL_FAIL","REASON":"missing R8/R7 source"}); return
    mism=[]; vol=[]
    for root in [R8,R7]:
        mf=root/"SHA256SUMS.txt"
        if not mf.exists():continue
        for line in mf.read_text(errors="replace").splitlines():
            q=line.strip().split(maxsplit=1)
            if len(q)!=2:continue
            ex,name=q; p=root/name.lstrip("* ")
            if p.exists() and sha(p)!=ex:(vol if p.name.lower()=="run.log" else mism).append(str(p))
    if mism:dump("R_STATUS.json",{"R_STATUS":"TECHNICAL_FAIL","REASON":"nonvolatile SHA mismatch","MISMATCHES":mism});return
    hist=pd.read_csv(R8.parent/"RIUD_DEV99_REENTRY_MULTISTATE_STATE_IDENTITY_AUDIT_R6_20260815"/"EVENT_MULTISTATE_HISTORY_MATRIX.csv").sort_values(["EVENT","BIN_INDEX"]).reset_index(drop=True)
    runprof=pd.read_csv(R8/"RUN_INDEX_STATE_PROFILE.csv").sort_values("BIN_INDEX").reset_index(drop=True)
    r7=pd.read_csv(R7/"MULTISTATE_RATE_CONTINUOUS_PROFILES.csv"); f7=r7[r7.MODEL_ID.astype(str)=="F7"].sort_values("GLOBAL_PCT")
    u=runprof.GLOBAL_MID_PCT.to_numpy(float)/100; du=float(np.median(np.diff(u))); events=sorted(hist.EVENT.astype(str).unique())
    source=[]
    for p in req:
        d=pd.read_csv(p) if p.suffix.lower()==".csv" else None; source.append({"PATH":str(p),"SHA256":sha(p),"SIZE":p.stat().st_size,"ROWS":len(d) if d is not None else "JSON","COLUMNS":",".join(d.columns) if d is not None else "JSON"})
    pd.DataFrame(source).to_csv(OUT/"SOURCE_PROVENANCE.csv",index=False);log("SOURCE_SHA_AUDIT=PASS VOLATILE_RUN_LOG_MISMATCHES_IGNORED="+str(len(vol)))
    # R8 past-only memory rows are the fixed memory covariates for each event/bin.
    drows=[]
    for e,g in hist.groupby("EVENT",sort=True):
        g=g.sort_values("BIN_INDEX").reset_index(drop=True); active_age=0; gap_age=0
        for _,r in g.iterrows():
            cat=cat_from_row(r); s=str(r.STATE)
            if s in ("A1","AR"):active_age+=1;gap_age=0;age=active_age
            elif s=="G":gap_age+=1;active_age=0;age=gap_age
            else:active_age=0;gap_age=0;age=0
            drows.append({"EVENT":e,"BIN_INDEX":int(r.BIN_INDEX),"STATE":s,"CATEGORY":cat,"AGE_CLASS":"AGE1" if age==1 else ("AGE2" if age==2 else ("AGE3PLUS" if age>=3 else "NONE"))})
    mem=pd.DataFrame(drows); mem["U"]=mem.BIN_INDEX.map(dict(enumerate(u)))
    # Boundary/event observations: one source-state trial per event/boundary.
    obs=[]
    for e,g in mem.groupby("EVENT",sort=True):
        g=g.sort_values("BIN_INDEX").reset_index(drop=True)
        for k in range(NB-1):
            a=g.iloc[k]; b=g.iloc[k+1]; cat=a.CATEGORY
            typ="01" if cat=="N0" else ("1G" if cat=="A1" else ("GR" if cat.startswith("G_") else "RG"))
            success=int((typ=="01" and b.CATEGORY=="A1") or (typ=="1G" and b.CATEGORY.startswith("G_")) or (typ=="GR" and b.CATEGORY.startswith("AR_")) or (typ=="RG" and b.CATEGORY.startswith("G_")))
            # R7 F7 evaluates its frozen base at the right-bin coordinate u[k+1].
            obs.append({"EVENT":e,"BOUNDARY_INDEX":k,"U":float(u[k+1]),"CATEGORY":cat,"AGE_CLASS":a.AGE_CLASS,"TYPE":typ,"SUCCESS":success})
    obs=pd.DataFrame(obs); nobs=len(obs)
    # Stored R7 columns are rates k, not log-rates. Convert once and keep
    # boundary indexing separate from event-row indexing.
    base_boundary={key:np.log(np.clip(np.interp(u[1:],f7.GLOBAL_PCT.to_numpy(float)/100,f7[key].to_numpy(float)),1e-12,None)) for key in ["K01","K1G","KGR","KRG"]}
    base_rates={key:base_boundary[key][obs.BOUNDARY_INDEX.to_numpy(int)] for key in base_boundary}
    keymap={"01":"K01","1G":"K1G","GR":"KGR","RG":"KRG"}
    def objective(p,model):
        dl=np.zeros(nobs)
        for typ in ["01","1G","GR","RG"]:
            m=obs.TYPE.to_numpy()==typ; idx=np.where(m)[0]
            if typ=="01": dl[idx]=0
            else: dl[idx]=[mem_delta(model,c,a,p) for c,a in zip(obs.CATEGORY.iloc[idx],obs.AGE_CLASS.iloc[idx])]
        lam=np.exp(np.clip(np.array([base_rates[keymap[t]][i] for i,t in enumerate(obs.TYPE)],float)+dl,-20,20)); pr=1-np.exp(-lam*du); pr=np.clip(pr,1e-12,1-1e-12); y=obs.SUCCESS.to_numpy(int)
        return -float(np.sum(y*np.log(pr)+(1-y)*np.log1p(-pr)))
    models={"M0":0,"M1":3,"M2":2,"M3":5,"M4":6}; bounds={m:[(-8,8)]*n for m,n in models.items()}
    def fit(m):
        if m=="M0":return {"MODEL_ID":"M0","PARAMS":np.zeros(0),"NLL":objective(np.zeros(0),m),"CONVERGED":1,"STARTS":1,"STATUS":True,"SECOND":np.nan}
        rng=np.random.default_rng(SEED+sum(map(ord,m))); best=None; vals=[]; conv=0
        for _ in range(N_STARTS):
            x=rng.normal(0,.35,models[m]); res=minimize(objective,x,args=(m,),method="L-BFGS-B",bounds=bounds[m],options={"maxiter":100,"ftol":1e-8,"gtol":1e-5,"maxls":15});vals.append(float(res.fun));conv+=int(bool(res.success));
            if best is None or res.fun<best.fun:best=res
        return {"MODEL_ID":m,"PARAMS":best.x,"NLL":float(best.fun),"CONVERGED":conv,"STARTS":N_STARTS,"STATUS":bool(best.success),"SECOND":sorted(vals)[1]}
    checkpoint=OUT/"R9_FIT_CHECKPOINT_V2.json"
    log("GLOBAL_PROGRESS=15%% GLOBAL_ETA=short ELAPSED=%.1fs ACTIVE_WORKERS=16 REMAINING=fit M0-M4"%(time.time()-t0))
    if checkpoint.exists():
        raw=json.loads(checkpoint.read_text(encoding="utf-8")); outs=[]
        for x in raw:
            x["PARAMS"]=np.asarray(x["PARAMS"],float); outs.append(x)
        log("FIT_CHECKPOINT=REUSED")
    else:
        outs=[]
        with ThreadPoolExecutor(max_workers=5) as ex:
            fs={ex.submit(fit,m):m for m in models}
            for f in as_completed(fs):
                x=f.result(); outs.append(x); log("MODEL_FIT=%s NLL=%.6f CONVERGED=%d/%d"%(fs[f],x["NLL"],x["CONVERGED"],x["STARTS"]))
        checkpoint.write_text(json.dumps([{**x,"PARAMS":x["PARAMS"].tolist()} for x in outs],indent=2),encoding="utf-8")
        log("FIT_CHECKPOINT=SAVED")
    outmap={x["MODEL_ID"]:x for x in outs}; total_params={m:16+models[m] for m in models}; ntrial=nobs; rows=[]
    # M0-M4 likelihood candidates; downstream reconstruction below.
    for m in models:
        x=outmap[m]; L=-x["NLL"]; k=total_params[m];rows.append({"MODEL_ID":m,"PARAMETER_COUNT":k,"JOINT_LOG_LIK":L,"AIC":2*k-2*L,"BIC":k*math.log(ntrial)-2*L,"FIT_STATUS":x["STATUS"],"CONVERGED_STARTS":x["CONVERGED"],"TOTAL_STARTS":x["STARTS"],"CONVERGENCE_RATE":x["CONVERGED"]/x["STARTS"],"SECOND_BEST_OBJECTIVE":x["SECOND"]})
    cand=pd.DataFrame(rows); basebic=float(cand[cand.MODEL_ID=="M0"].BIC.iloc[0]);cand["DELTA_BIC_VS_M0"]=cand.BIC-basebic
    bestbic=cand.sort_values(["BIC","PARAMETER_COUNT"]).iloc[0];bestll=cand.sort_values(["JOINT_LOG_LIK","PARAMETER_COUNT"],ascending=[False,True]).iloc[0];bestcompact=cand[cand.BIC<=bestbic.BIC+6].sort_values(["PARAMETER_COUNT","BIC"]).iloc[0];best=str(bestcompact.MODEL_ID)
    log("MODEL_RANKING_DONE BEST_BIC=%s BEST_LIKELIHOOD=%s BEST_COMPACT=%s"%(bestbic.MODEL_ID,bestll.MODEL_ID,bestcompact.MODEL_ID))
    # Fixed memory-conditioned downstream expectation at every frozen bin.
    def p_for(model,param,k,cat,age):
        typ="01" if cat=="N0" else ("1G" if cat=="A1" else ("GR" if cat.startswith("G_") else "RG")); lb=base_boundary[keymap[typ]][k]
        return 1-math.exp(-math.exp(np.clip(lb+mem_delta(model,cat,age,param),-20,20))*du)
    def reconstruct(model,param):
        pred=[]; comp=[]
        for k in range(NB):
            if k==0:
                q=mem[mem.BIN_INDEX==0]; d={c:float((q.CATEGORY==c).sum()) for c in CATS}
            else:
                d={c:0.0 for c in CATS}; q=mem[mem.BIN_INDEX==k-1]
                for r in q.itertuples():
                    p=p_for(model,param,k-1,r.CATEGORY,r.AGE_CLASS); c=r.CATEGORY
                    if c=="N0":d["A1"]+=p;d["N0"]+=1-p
                    elif c=="A1":d["G_AFTER_RUN1"]+=p;d["A1"]+=1-p
                    elif c=="AR_RUN2":d["G_AFTER_RUN2"]+=p;d["AR_RUN2"]+=1-p
                    elif c=="AR_RUN3":d["G_AFTER_RUN3"]+=p;d["AR_RUN3"]+=1-p
                    elif c=="AR_RUN4PLUS":d["G_AFTER_RUN4PLUS"]+=p;d["AR_RUN4PLUS"]+=1-p
                    elif c=="G_AFTER_RUN1":d["AR_RUN2"]+=p;d["G_AFTER_RUN1"]+=1-p
                    elif c=="G_AFTER_RUN2":d["AR_RUN3"]+=p;d["G_AFTER_RUN2"]+=1-p
                    elif c in ("G_AFTER_RUN3","G_AFTER_RUN4PLUS"):d["AR_RUN4PLUS"]+=p;d[c]+=1-p
                
            d.update({"MODEL_ID":model,"BIN_INDEX":k,"GLOBAL_PCT":float(runprof.loc[k,"GLOBAL_MID_PCT"]),"C_PRED":d["A1"]+d["AR_RUN2"]+d["AR_RUN3"]+d["AR_RUN4PLUS"],"TOTAL_PRED":sum(d[c] for c in CATS)})
            comp.append(d)
        return pd.DataFrame(comp)
    recon={m:reconstruct(m,outmap[m]["PARAMS"]) for m in models}; profrows=[]
    for m,df in recon.items():
        for k,r in df.iterrows():
            uval=float(r.GLOBAL_PCT)/100; typ_rates={}
            for typ,key in keymap.items():typ_rates["K_"+typ]=math.exp(np.clip(base_boundary[key][min(k,NB-2)]+mem_delta(m,"A1" if typ=="1G" else ("G_AFTER_RUN1" if typ=="GR" else ("AR_RUN2" if typ=="RG" else "N0")),"AGE1",outmap[m]["PARAMS"]),-20,20))
            profrows.append({"MODEL_ID":m,"BIN_INDEX":k,"GLOBAL_PCT":r.GLOBAL_PCT,**{c:r[c] for c in CATS},**typ_rates})
    profout=pd.DataFrame(profrows)
    profout["PROFILE_KIND"]="FROZEN_BIN"
    # Add a dense, read-only interpolation of the already reconstructed frozen-bin
    # profile for downstream plotting/audit. This does not refit or create new data.
    bdf=recon[best]
    dense=np.linspace(float(u[0]),float(u[-1]),20001)
    dense_arr={"U":dense,"GLOBAL_PCT":dense*100,"MODEL_ID":np.full(len(dense),best),"BIN_INDEX":np.full(len(dense),np.nan)}
    for c in CATS:
        dense_arr[c]=np.interp(dense,u,bdf[c].to_numpy(float))
    dense_arr["C_PRED"]=dense_arr["A1"]+dense_arr["AR_RUN2"]+dense_arr["AR_RUN3"]+dense_arr["AR_RUN4PLUS"]
    dense_arr["TOTAL_PRED"]=sum(dense_arr[c] for c in CATS)
    dense_arr["PROFILE_KIND"]=np.full(len(dense),"DENSE_INTERPOLATED")
    profout=pd.concat([profout,pd.DataFrame(dense_arr)],ignore_index=True,sort=False)
    profout.to_csv(OUT/"MEMORY_FLOW_CONTINUOUS_PROFILE.csv",index=False)
    pd.DataFrame([dict(row) for m,df in recon.items() for _,row in df.iterrows()]).to_csv(OUT/"MEMORY_COMPOSITION_RECONSTRUCTION.csv",index=False)
    obsC=runprof.A1.to_numpy(float)+runprof.AR_RUN2.to_numpy(float)+runprof.AR_RUN3.to_numpy(float)+runprof.AR_RUN4PLUS.to_numpy(float); lmobs=landmarks(u,obsC); aud=[]
    for m,df in recon.items():
        c=df.C_PRED.to_numpy(float); lm=landmarks(u,c); row=cand[cand.MODEL_ID==m].iloc[0].to_dict();row.update({"MODEL_ID":m,"PRED_FIRST_TURNOVER":lm["FIRST_TURNOVER"],"PRED_RECOVERY":lm["RECOVERY"],"PRED_SECOND_TURNOVER":lm["SECOND_TURNOVER"],"PRED_GLOBAL_PEAK":lm["GLOBAL_PEAK"],"PRED_SIGN_SEQUENCE":lm["SIGN_SEQUENCE"],"OBS_FIRST_TURNOVER":LAND["FIRST_TURNOVER"],"OBS_RECOVERY":LAND["RECOVERY"],"OBS_SECOND_TURNOVER":LAND["SECOND_TURNOVER"],"OBS_GLOBAL_PEAK":LAND["GLOBAL_PEAK"],"COVERAGE_FULL_R2":1-np.sum((obsC-c)**2)/np.sum((obsC-obsC.mean())**2),"COVERAGE_RISE_R2":1-np.sum((obsC[u<=.453125]-c[u<=.453125])**2)/np.sum((obsC[u<=.453125]-obsC[u<=.453125].mean())**2),"COVERAGE_FALL_R2":1-np.sum((obsC[u>=.453125]-c[u>=.453125])**2)/np.sum((obsC[u>=.453125]-obsC[u>=.453125].mean())**2)})
        for x,o in [("FIRST_TURNOVER","FIRST_TURNOVER"),("RECOVERY","RECOVERY"),("SECOND_TURNOVER","SECOND_TURNOVER"),("GLOBAL_PEAK","GLOBAL_PEAK")]:row[x+"_ERROR"]=abs(row["PRED_"+x]-LAND[o]) if not np.isnan(row["PRED_"+x]) else np.nan
        row["TOPOLOGY_SIGN_SEQUENCE_MATCH"]=False; aud.append(row)
    audit=pd.DataFrame(aud);audit.to_csv(OUT/"MEMORY_FLOW_LANDMARK_AUDIT.csv",index=False);cand.to_csv(OUT/"MEMORY_FLOW_MODEL_CANDIDATES.csv",index=False)
    # Memory-conditioned rates and equation coefficients.
    par=outmap[best]["PARAMS"]; rate_rows=[]
    for k in range(NB-1):
        for cat in CATS:
            for age in ["AGE1","AGE2","AGE3PLUS"]:
                if cat=="N0" and age!="AGE1":continue
                typ="01" if cat=="N0" else ("1G" if cat=="A1" else ("GR" if cat.startswith("G_") else "RG")); key=keymap[typ]; rate_rows.append({"MODEL_ID":best,"BOUNDARY_INDEX":k,"GLOBAL_PCT":float((u[k]+u[k+1])*50),"TRANSITION_TYPE":typ,"CATEGORY":cat,"AGE_CLASS":age,"BASE_RATE":base_rates[key][k],"MEMORY_DELTA":mem_delta(best,cat,age,par),"RATE":math.exp(np.clip(base_rates[key][k]+mem_delta(best,cat,age,par),-20,20))})
    pd.DataFrame(rate_rows).to_csv(OUT/"MEMORY_CONDITIONED_RATES.csv",index=False)
    # Equation text/json with explicit numeric memory coefficients.
    names=["beta2","beta3","beta4","gamma2","gamma3","delta"]
    coeff={n:float(par[i]) for i,n in enumerate(names[:len(par)])}
    if best=="M3":
        rate_rules={"lambda_01":"lambda_01_R7F7(u)","lambda_1G":"lambda_1G_R7F7(u)*exp(gamma_age)","lambda_GR":"lambda_GR_R7F7(u)*exp(beta_run+gamma_gap_age)","lambda_RG":"lambda_RG_R7F7(u)*exp(beta_run+gamma_active_age)"}
        gr_txt="lambda_GR(u,run_index,gap_age)=lambda_GR_R7F7(u)*exp(beta_run+gamma_gap_age)"
        rg_txt="lambda_RG(u,run_index,active_age)=lambda_RG_R7F7(u)*exp(beta_run+gamma_active_age)"
    elif best=="M4":
        rate_rules={"lambda_01":"lambda_01_R7F7(u)","lambda_1G":"lambda_1G_R7F7(u)*exp(gamma_age)","lambda_GR":"lambda_GR_R7F7(u)*exp(beta_run+gamma_gap_age+delta*I(run>=4,age>=3))","lambda_RG":"lambda_RG_R7F7(u)*exp(beta_run+gamma_active_age+delta*I(run>=4,age>=3))"}
        gr_txt="lambda_GR(u,run_index,gap_age)=lambda_GR_R7F7(u)*exp(beta_run+gamma_gap_age+delta*I(run>=4,age>=3))"
        rg_txt="lambda_RG(u,run_index,active_age)=lambda_RG_R7F7(u)*exp(beta_run+gamma_active_age+delta*I(run>=4,age>=3))"
    else:
        rate_rules={"lambda_01":"lambda_01_R7F7(u)","lambda_1G":"lambda_1G_R7F7(u)*exp(gamma_age)","lambda_GR":"lambda_GR_R7F7(u)*memory_factor","lambda_RG":"lambda_RG_R7F7(u)*memory_factor"}
        gr_txt="lambda_GR/RG=R7F7 baseline with model-specific memory terms"
        rg_txt="lambda_RG/RG=R7F7 baseline with model-specific memory terms"
    eq={"MODEL_ID":best,"BASE":"R7 F7 two-Gaussian shared progression rates loaded read-only","MEMORY_COEFFICIENTS":coeff,"RATE_RULES":rate_rules,"ODE":"dN0/du=-lambda01*N0; dA1/du=lambda01*N0-lambda1G*A1; dG/du=lambda1G*A1+lambdaRG*AR-lambdaGR*G; dAR/du=lambdaGR*G-lambdaRG*AR","C":"A1+AR","PARAMETER_COUNT":int(bestcompact.PARAMETER_COUNT),"JOINT_LOG_LIK":float(bestcompact.JOINT_LOG_LIK),"AIC":float(bestcompact.AIC),"BIC":float(bestcompact.BIC),"DELTA_BIC_VS_M0":float(bestcompact.DELTA_BIC_VS_M0)};dump("BEST_HISTORY_AWARE_FLOW_EQUATION.json",eq)
    txt=[f"BEST_COMPACT_MODEL={best}","BASE_PROGRESSION=R7_F7_TWO_GAUSSIAN_SHARED_READ_ONLY",f"PARAMETER_COUNT={bestcompact.PARAMETER_COUNT}","lambda_01(u)=lambda_01_R7F7(u)","lambda_1G(u,active_age)=lambda_1G_R7F7(u)*exp(gamma_age)",gr_txt,rg_txt,"dN0/du=-lambda01*N0","dA1/du=lambda01*N0-lambda1G*A1","dG/du=lambda1G*A1+lambdaRG*AR-lambdaGR*G","dAR/du=lambdaGR*G-lambdaRG*AR","C=A1+AR"]+[f"{k}={v:.12g}" for k,v in coeff.items()]+[f"JOINT_LOG_LIK={bestcompact.JOINT_LOG_LIK}",f"AIC={bestcompact.AIC}",f"BIC={bestcompact.BIC}",f"DELTA_BIC_VS_M0={bestcompact.DELTA_BIC_VS_M0}",f"COVERAGE_FULL_R2={audit[audit.MODEL_ID==best].COVERAGE_FULL_R2.iloc[0]}",f"PRED_GLOBAL_PEAK={audit[audit.MODEL_ID==best].PRED_GLOBAL_PEAK.iloc[0]}","OBS_GLOBAL_PEAK=45.3125"]
    (OUT/"BEST_HISTORY_AWARE_FLOW_EQUATION.txt").write_text("\n".join(txt)+"\n",encoding="utf-8")
    # Stability ledger and verdict.
    pd.DataFrame([{"MODEL_ID":m,"CONVERGED_STARTS":outmap[m]["CONVERGED"],"TOTAL_STARTS":outmap[m]["STARTS"],"CONVERGENCE_RATE":outmap[m]["CONVERGED"]/outmap[m]["STARTS"],"BEST_OBJECTIVE":outmap[m]["NLL"],"SECOND_BEST_OBJECTIVE":outmap[m]["SECOND"],"STATUS":outmap[m]["STATUS"]} for m in models]).to_csv(OUT/"OPTIMIZER_STABILITY_AUDIT.csv",index=False)
    ledger=[]
    descriptions={"M0":"R7 F7 frozen baseline; no memory conditioning","M1":"run-index conditioned flow","M2":"past-state age conditioned flow","M3":"run-index plus past-state age conditioned flow","M4":"run-index plus age plus run>=4 and age>=3 interaction"}
    for m in models:
        ledger.append({"MODEL_ID":m,"DESCRIPTION":descriptions[m],"BASE_RATE_SOURCE":"R7 F7 frozen read-only","PARAMETER_COUNT":int(total_params[m]),"MEMORY_PARAMETER_COUNT":int(models[m]),"N_STARTS":int(outmap[m]["STARTS"]),"CONVERGED_STARTS":int(outmap[m]["CONVERGED"]),"SEED":int(SEED+sum(map(ord,m))),"PRIMARY_TARGET":"transition likelihood","SELECTION_ROLE":"BIC/likelihood/compact ranking"})
    pd.DataFrame(ledger).to_csv(OUT/"MEMORY_FLOW_MODEL_LEDGER.csv",index=False)
    b=audit[audit.MODEL_ID==best].iloc[0]; peakidx=int(np.argmax(recon[best].C_PRED)); arpred=float(recon[best].iloc[peakidx]["AR_RUN4PLUS"]/(recon[best].iloc[peakidx]["AR_RUN2"]+recon[best].iloc[peakidx]["AR_RUN3"]+recon[best].iloc[peakidx]["AR_RUN4PLUS"]))
    topo=bool(max(b.FIRST_TURNOVER_ERROR,b.RECOVERY_ERROR,b.SECOND_TURNOVER_ERROR,b.GLOBAL_PEAK_ERROR)<=3.125)
    memory_improved=float(bestcompact.BIC)<float(cand[cand.MODEL_ID=="M0"].BIC.iloc[0]); adequate=outmap[best]["CONVERGED"]/max(1,outmap[best]["STARTS"])>=.5
    verdict="HISTORY_AWARE_MULTISTATE_FLOW_CANDIDATE" if memory_improved and topo and adequate else ("MEMORY_IMPROVES_GLOBAL_PEAK_BUT_PARTIAL" if memory_improved else "MEMORY_STRUCTURE_REAL_BUT_RATE_LAW_INSUFFICIENT")
    dump("SCIENTIFIC_VERDICT.json",{"VERDICT":verdict,"BEST_BIC_MODEL":best,"BEST_LIKELIHOOD_MODEL":str(bestll.MODEL_ID),"BEST_COMPACT_MODEL":best,"MEMORY_IMPROVES_BIC":memory_improved,"TOPOLOGY_RECOVERY":topo,"OPTIMIZER_ADEQUATE":adequate,"FINAL_LAW_FROZEN":False,"NO_NULL":True})
    status={"R_STATUS":"PASS","SOURCE_SHA_AUDIT":"PASS","EVENTS":N,"FROZEN_BINS":NB,"MODELS_TESTED":list(models),"BEST_BIC_MODEL":str(bestbic.MODEL_ID),"BEST_LIKELIHOOD_MODEL":str(bestll.MODEL_ID),"BEST_COMPACT_MODEL":best,"FINAL_LAW_FROZEN":False,"NULL_RUN":False,"CV_RUN":False,"HOLDOUT_OPENED":False,"PHYSICAL_METADATA_OPENED":False}
    dump("R_STATUS.json",status)
    send=f"""R_STATUS=PASS
SOURCE_SHA_AUDIT=PASS
EVENTS=97
FROZEN_BINS=32
MODELS_TESTED=M0,M1,M2,M3,M4
BEST_BIC_MODEL={bestbic.MODEL_ID}
BEST_LIKELIHOOD_MODEL={bestll.MODEL_ID}
BEST_COMPACT_MODEL={best}
PARAMETER_COUNT={bestcompact.PARAMETER_COUNT}
JOINT_LOG_LIK={bestcompact.JOINT_LOG_LIK}
AIC={bestcompact.AIC}
BIC={bestcompact.BIC}
DELTA_BIC_VS_M0={bestcompact.DELTA_BIC_VS_M0}
CONVERGED_STARTS={outmap[best]['CONVERGED']}
TOTAL_STARTS={outmap[best]['STARTS']}
CONVERGENCE_RATE={outmap[best]['CONVERGED']/outmap[best]['STARTS']}
COVERAGE_FULL_R2={b.COVERAGE_FULL_R2}
COVERAGE_RISE_R2={b.COVERAGE_RISE_R2}
COVERAGE_FALL_R2={b.COVERAGE_FALL_R2}
OBS_FIRST_TURNOVER=10.94
PRED_FIRST_TURNOVER={b.PRED_FIRST_TURNOVER}
OBS_RECOVERY=14.06421875
PRED_RECOVERY={b.PRED_RECOVERY}
OBS_SECOND_TURNOVER=17.1884375
PRED_SECOND_TURNOVER={b.PRED_SECOND_TURNOVER}
OBS_GLOBAL_PEAK=45.3125
PRED_GLOBAL_PEAK={b.PRED_GLOBAL_PEAK}
AR4PLUS_FRACTION_OBS_PEAK={float(runprof.loc[int(np.argmin(abs(runprof.GLOBAL_MID_PCT-45.3125))),"AR_RUN4PLUS"]/(runprof.loc[int(np.argmin(abs(runprof.GLOBAL_MID_PCT-45.3125))),["AR_RUN2","AR_RUN3","AR_RUN4PLUS"]].sum()))}
AR4PLUS_FRACTION_PRED_PEAK={arpred}
HIGH_RUN_INDEX_PEAK_RECOVERED={arpred>.5}
TOPOLOGY_SIGN_SEQUENCE_MATCH=False
MEMORY_FLOW_VERDICT={verdict}
FINAL_LAW_FROZEN=False
NULL_RUN=False
CV_RUN=False
5FOLD_RUN=False
HOLDOUT_OPENED=False
DEV61_OPENED=False
PHYSICAL_METADATA_OPENED=False
NEXT=STOP_FOR_USER_REVIEW
"""
    (OUT/"SEND_TO_CHAT.txt").write_text(send,encoding="utf-8")
    try:
        from PIL import Image,ImageDraw
        im=Image.new("RGB",(1500,850),"white");d=ImageDraw.Draw(im);d.text((20,20),"R9 history-aware multistate flow",fill="black")
        for col,color,y in [("AR_RUN2","#2ca25f",60),("AR_RUN3","#1f77b4",230),("AR_RUN4PLUS","#d62728",400),("G_AFTER_RUN4PLUS","#9467bd",570)]:
            vals=recon[best][col].to_numpy(float); d.text((20,y),col,fill="black"); pts=[];lo=0;hi=max(1,vals.max())
            for i,v in enumerate(vals):pts.append((100+i*1300/(len(vals)-1),y+25+120-(v/hi)*120))
            d.line(pts,fill=color,width=2)
        im.save(OUT/"MEMORY_FLOW_DYNAMICS.png")
    except Exception as e:log("PLOT_NOTE="+repr(e))
    shutil.copy2(Path(__file__),OUT/"RUN.py");(OUT/"README.txt").write_text("R9 DEV99 history-aware multistate flow discovery. R7 F7 base progression is read-only; M0-M4 add only predeclared run-index/state-age terms. No physical metadata/null/CV/Holdout/law freeze.\n",encoding="utf-8")
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
    log("GLOBAL_PROGRESS=100%% GLOBAL_ETA=0 ELAPSED=%.1fs ACTIVE_WORKERS=16 REMAINING=0"%(time.time()-t0))
if __name__=="__main__":main()
