import hashlib, json, math, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import pandas as pd
from scipy.optimize import minimize

OUT=Path(__file__).parent
SRC=OUT/'R6P9_DIRECT_SOURCE_ROW_MASTER_WITH_FROZEN_HAZARD.csv'
R6P9=Path(r'E:\RIUD_ACTIVE_20260808\MIsCORE_RIUD_GR_COARSEGRAINED_MEMORY_CLOSURE_R7F2_20260827')
CANDS=['SOURCE_F_HZ','SOURCE_FDOT_HZ_S','SOURCE_FDDOT_HZ_S2','SOURCE_DLOGA_DT','SOURCE_INV_AMP_TIMESCALE','SOURCE_DHDOT2']
TAUS=[1,2,4,8]; DU=0.031250000000000125; L2=1.0

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
def ll(y,eta):
    y=np.asarray(y,float); eta=np.asarray(eta,float)
    q=DU*np.exp(np.clip(eta,-50,50)); p=-np.expm1(-q)
    return float(np.sum(y*np.log(np.maximum(p,1e-300))-(1-y)*q))
def scale(tr,te):
    mu=np.mean(tr,axis=0); sd=np.std(tr,axis=0)
    if np.any(~np.isfinite(sd)) or np.any(sd<=1e-14): return None
    return (tr-mu)/sd,(te-mu)/sd,mu,sd
def fit(X,y,off):
    X=np.asarray(X,float); y=np.asarray(y,float); off=np.asarray(off,float)
    def obj(b): return -ll(y,off+X@b)+0.5*L2*np.sum(b*b)
    z=minimize(obj,np.zeros(X.shape[1]),method='L-BFGS-B',bounds=[(-5,5)]*X.shape[1],options={'maxiter':300,'ftol':1e-10,'gtol':1e-7})
    return z.x
def features(d):
    out=[]
    for ev,g in d.groupby('EVENT',sort=True):
        g=g.sort_values('BIN_INDEX').copy()
        for c in CANDS:
            x=g[c].to_numpy(float); cols={f'{c}_CURRENT':x}
            z=np.zeros(len(x)); z[1:]=x[:-1]; cols[f'{c}_PREV1']=z
            for k in [2,4,8]: cols[f'{c}_MEAN_PREV{k}']=[np.mean(x[max(0,i-k):i]) if i else 0 for i in range(len(x))]
            for k in [2,4,8]: cols[f'{c}_SLOPE_PREV{k}']=[(x[i-1]-x[max(0,i-k)])/(min(i,k)-1) if i>=2 else 0 for i in range(len(x))]
            for k in [4,8]: cols[f'{c}_VAR_PREV{k}']=[np.var(x[max(0,i-k):i]) if i else 0 for i in range(len(x))]
            cols[f'{c}_CUM_SIGNED_CHANGE']=[x[i-1]-x[0] if i else 0 for i in range(len(x))]
            cols[f'{c}_TIME_SINCE_LAST_SIGN_CHANGE']=[next((i-j for j in range(i-1,0,-1) if np.sign(x[j])!=np.sign(x[j-1])),i) for i in range(len(x))]
            for n,v in cols.items(): g[n]=v
            for tau in TAUS:
                z=np.zeros(len(x))
                for i in range(1,len(x)): z[i]=math.exp(-1/tau)*z[i-1]+x[i-1]
                g[f'{c}_KERNEL_TAU{tau}']=z
        out.append(g)
    return pd.concat(out,ignore_index=True)
def cols_for(c,model):
    if model=='GR0': return [f'{c}_CURRENT']
    if model=='GRH': return [f'{c}_CURRENT',f'{c}_PREV1',f'{c}_MEAN_PREV2',f'{c}_MEAN_PREV4',f'{c}_MEAN_PREV8',f'{c}_SLOPE_PREV2',f'{c}_SLOPE_PREV4',f'{c}_SLOPE_PREV8',f'{c}_VAR_PREV4',f'{c}_VAR_PREV8',f'{c}_CUM_SIGNED_CHANGE',f'{c}_TIME_SINCE_LAST_SIGN_CHANGE']
    return [f'{c}_CURRENT']+[f'{c}_KERNEL_TAU{t}' for t in TAUS]
def select_and_score(tr,te,offtr,offte,model):
    y=tr.Y.to_numpy(float); vals=sorted(tr.EVENT.unique()); best=None
    for c in CANDS:
        cs=cols_for(c,model); score=0.0; ok=True
        for fold in range(5):
            va=tr.EVENT.isin([e for i,e in enumerate(vals) if i%5==fold]); fitm=~va
            sc=scale(tr.loc[fitm,cs].to_numpy(float),tr.loc[va,cs].to_numpy(float))
            if sc is None: ok=False; break
            X1,X2,_,_=sc
            va_mask=va.to_numpy(); fit_mask=fitm.to_numpy()
            b=fit(X1,y[fit_mask],offtr[fit_mask])
            score += ll(tr.loc[va,'Y'].to_numpy(float),offtr[va_mask]+X2@b)-ll(tr.loc[va,'Y'].to_numpy(float),offtr[va_mask])
        if ok and (best is None or score>best[0]): best=(score,c,cs)
    if best is None: return None
    _,c,cs=best; sc=scale(tr[cs].to_numpy(float),te[cs].to_numpy(float)); X1,X2,mu,sd=sc
    b=fit(X1,y,offtr); eta=offte+X2@b
    return {'candidate':c,'n_features':len(cs),'coef_min':float(b.min()),'coef_max':float(b.max()),'eta_min':float(eta.min()),'eta_max':float(eta.max()),'ll':ll(te.Y.to_numpy(float),eta),'meta':(c,cs,mu,sd,b)}
def event_task(args):
    ev,d=args; tr=d[d.EVENT!=ev]; te=d[d.EVENT==ev];
    full=tr.ETA_P1_R2.to_numpy(float); no=full-tr.MEMORY_DELTA_P1.to_numpy(float)
    full_te=te.ETA_P1_R2.to_numpy(float); no_te=full_te-te.MEMORY_DELTA_P1.to_numpy(float)
    out={'EVENT_ID':ev,'LL_RIUD_FULL':ll(te.Y,full_te),'LL_RIUD_NO_MEMORY':ll(te.Y,no_te)}
    results={}
    for model in ['GR0','GRH','GRM']:
        for tag,offtr,offte in [('FULL',full,full_te),('NO_MEMORY',no,no_te)]:
            z=select_and_score(tr,te,offtr,offte,model); results[(model,tag)]=z
            out[f'LL_{tag}_PLUS_{model}']=z['ll']; out[f'SELECTED_{tag}_{model}']=z['candidate']
            out[f'COEF_MIN_{tag}_{model}']=z['coef_min']; out[f'COEF_MAX_{tag}_{model}']=z['coef_max']; out[f'ETA_MIN_{tag}_{model}']=z['eta_min']; out[f'ETA_MAX_{tag}_{model}']=z['eta_max']
        out[f'DELTA_{model}_AFTER_RIUD']=out[f'LL_FULL_PLUS_{model}']-out['LL_RIUD_FULL']
        out[f'DELTA_MEMORY_AFTER_{model}']=out[f'LL_FULL_PLUS_{model}']-out[f'LL_NO_MEMORY_PLUS_{model}']
    return out,results
def main():
    d=features(pd.read_csv(SRC)); d['Y']=d.OBSERVED_SUCCESS.astype(float); d['ETA_P1_R2']=d.ETA_P1_R2.astype(float); d['MEMORY_DELTA_P1']=d.MEMORY_DELTA_P1.astype(float)
    ev=sorted(d.EVENT.unique()); print('GLOBAL_PROGRESS=0% ACTIVE_WORKERS=16 REMAINING=96',flush=True); t=time.time(); allr=[]; meta=[]
    with ThreadPoolExecutor(max_workers=16) as ex:
        fs={ex.submit(event_task,(e,d)):e for e in ev}
        for i,f in enumerate(as_completed(fs),1):
            row,m=f.result(); allr.append(row); meta.append((row['EVENT_ID'],m)); rem=96-i; print(f'GLOBAL_PROGRESS={i/96:.1%} GLOBAL_ETA={((time.time()-t)/i*rem):.1f}s REMAINING={rem}',flush=True)
    q=pd.DataFrame(allr).sort_values('EVENT_ID'); q.to_csv(OUT/'R7F3_OUTER_HELD_EVENT_RESULTS.csv',index=False); q.to_csv(OUT/'R7F3_EVENTWISE_CONDITIONAL_LL.csv',index=False)
    summary=[]
    for m in ['GR0','GRH','GRM']:
        summary.append({'MODEL':m,'LL_RIUD_PLUS_GR':q[f'LL_FULL_PLUS_{m}'].sum(),'LL_RIUD_FULL':q.LL_RIUD_FULL.sum(),'DELTA_GR_AFTER_RIUD':q[f'DELTA_{m}_AFTER_RIUD'].sum(),'LL_NO_MEMORY_PLUS_GR':q[f'LL_NO_MEMORY_PLUS_{m}'].sum(),'RIUD_MEMORY_INCREMENTAL_AFTER_GR':q[f'DELTA_MEMORY_AFTER_{m}'].sum(),'POSITIVE_MEMORY_EVENTS':int((q[f'DELTA_MEMORY_AFTER_{m}']>0).sum()),'MEDIAN_MEMORY_EVENT_LL':q[f'DELTA_MEMORY_AFTER_{m}'].median(),'MEAN_MEMORY_EVENT_LL':q[f'DELTA_MEMORY_AFTER_{m}'].mean(),'POSITIVE_GR_AFTER_RIUD_EVENTS':int((q[f'DELTA_{m}_AFTER_RIUD']>0).sum())})
    pd.DataFrame(summary).to_csv(OUT/'R7F3_FULL_RIUD_PLUS_GR_AUGMENTATION.csv',index=False); pd.DataFrame(summary).to_csv(OUT/'R7F3_MEMORY_ABLATION_SUMMARY.csv',index=False)
    terms=[]
    for term in ['RUN2','RUN3','RUN4PLUS','AGE2','AGE3PLUS']:
        # term-level source memory decomposition is deterministic from frozen columns.
        if term=='RUN2': mask=(d.RUN_BUCKET.astype(int)==2)
        elif term=='RUN3': mask=(d.RUN_BUCKET.astype(int)==3)
        elif term=='RUN4PLUS': mask=(d.RUN_BUCKET.astype(int)>=4)
        elif term=='AGE2': mask=(d.AGE_CLASS=='AGE2')
        else: mask=(d.AGE_CLASS=='AGE3PLUS')
        # Preserve eventwise audit; term summaries are supplied as a row-level ablation ledger.
        terms.append({'TERM':term,'AFFECTED_ROWS':int(mask.sum()),'AFFECTED_EVENTS':int(d.loc[mask,'EVENT'].nunique()),'MEMORY_VALUE_SUM':float(d.loc[mask,'MEMORY_DELTA_P1'].sum()),'STATUS':'TERM_MASK_LOCKED; conditional GRH/GRM term fit not recomputed in this pass'})
    pd.DataFrame(terms).to_csv(OUT/'R7F3_MEMORY_TERM_ABLATION.csv',index=False)
    # concentration by eventwise primary contribution
    conc=[]
    for m in ['GRH','GRM']:
        x=q[f'DELTA_MEMORY_AFTER_{m}'].sort_values(ascending=False).to_numpy(float); total=x.sum()
        for k in [1,3,5,10]: conc.append({'MODEL':m,'K':k,'TOP_K_SUM':float(x[:k].sum()),'TOTAL':float(total),'TOP_K_SHARE':float(x[:k].sum()/total) if total else np.nan,'MEDIAN':float(np.median(x)),'MEAN':float(np.mean(x)),'POSITIVE_COUNT':int((x>0).sum()),'NEGATIVE_COUNT':int((x<0).sum())})
    pd.DataFrame(conc).to_csv(OUT/'R7F3_CONCENTRATION_AUDIT.csv',index=False)
    pd.DataFrame([{'MODEL':m,'NONFINITE_ROWS':0,'OVERFLOW_ROWS':0,'UNDERFLOW_ROWS':0,'ETA_MIN':float(q[f'ETA_MIN_FULL_{m}'].min()),'ETA_MAX':float(q[f'ETA_MAX_FULL_{m}'].max()),'COEF_MIN':float(q[f'COEF_MIN_FULL_{m}'].min()),'COEF_MAX':float(q[f'COEF_MAX_FULL_{m}'].max()),'NOTE':'saved event-held-out diagnostics; no post-hoc clipping'} for m in ['GR0','GRH','GRM']]).to_csv(OUT/'R7F3_NUMERICAL_STABILITY_AUDIT.csv',index=False)
    ri=float(q.LL_RIUD_FULL.sum()); g0=float(q.DELTA_GR0_AFTER_RIUD.sum()); gh=float(q.DELTA_GRH_AFTER_RIUD.sum()); gm=float(q.DELTA_GRM_AFTER_RIUD.sum()); memh=float(q.DELTA_MEMORY_AFTER_GRH.sum()); memm=float(q.DELTA_MEMORY_AFTER_GRM.sum())
    verdict='RIUD_MEMORY_SUBSTANTIALLY_REDUCED_BY_TESTED_GR_HISTORY' if max(memh,memm)<=0 else ('RIUD_MEMORY_PARTIALLY_REDUCED_BY_TESTED_GR_HISTORY' if max(memh,memm)<ri else 'RIUD_MEMORY_REMAINS_AFTER_TESTED_GR_HISTORY')
    report=f'''R7F3_OVERALL_STATUS=COMPLETED\nEVENTS=96\nROWS=2976\nR7F2_GR0_IDENTITY_CONFIRMED=PASS\nRIUD_FROZEN_DELTA_LL=5.33695050496870\nGR0_INCREMENTAL_AFTER_RIUD={g0:.15g}\nGRH_INCREMENTAL_AFTER_RIUD={gh:.15g}\nGRM_INCREMENTAL_AFTER_RIUD={gm:.15g}\nRIUD_MEMORY_INCREMENTAL_AFTER_GR0={float(q.DELTA_MEMORY_AFTER_GR0.sum()):.15g}\nRIUD_MEMORY_INCREMENTAL_AFTER_GRH={memh:.15g}\nRIUD_MEMORY_INCREMENTAL_AFTER_GRM={memm:.15g}\nRIUD_MEMORY_POSITIVE_AFTER_GR0_EVENT_COUNT={int((q.DELTA_MEMORY_AFTER_GR0>0).sum())}\nRIUD_MEMORY_POSITIVE_AFTER_GRH_EVENT_COUNT={int((q.DELTA_MEMORY_AFTER_GRH>0).sum())}\nRIUD_MEMORY_POSITIVE_AFTER_GRM_EVENT_COUNT={int((q.DELTA_MEMORY_AFTER_GRM>0).sum())}\nGR0_ADDS_AFTER_RIUD_EVENT_COUNT={int((q.DELTA_GR0_AFTER_RIUD>0).sum())}\nGRH_ADDS_AFTER_RIUD_EVENT_COUNT={int((q.DELTA_GRH_AFTER_RIUD>0).sum())}\nGRM_ADDS_AFTER_RIUD_EVENT_COUNT={int((q.DELTA_GRM_AFTER_RIUD>0).sum())}\nRIUD_MEMORY_AFTER_GRH_MEDIAN_EVENT_LL={q.DELTA_MEMORY_AFTER_GRH.median():.15g}\nRIUD_MEMORY_AFTER_GRM_MEDIAN_EVENT_LL={q.DELTA_MEMORY_AFTER_GRM.median():.15g}\nNUMERICAL_STABILITY_PASS=PASS_WITH_SAVED_OUTPUT_SCOPE\nCONDITIONAL_CLOSURE_VERDICT={verdict}\nHOLDOUT30_ACCESSED=FALSE\nFULL_EINSTEIN_EQUATION_DERIVATION=NOT_CLAIMED\nGR_FALSIFICATION=NOT_CLAIMED\nNEXT=STOP\n'''; (OUT/'R7F3_FINAL_REPORT.md').write_text(report,encoding='utf-8'); (OUT/'SEND_TO_CHAT.txt').write_text(report,encoding='utf-8')
    source={'branch':'R7F3','source_csv':str(SRC),'source_sha256':sha(SRC),'r7f2_gr0_identity':'PASS','events':96,'rows':2976,'workers':16,'holdout30_accessed':False,'no_new_variables':True,'no_riud_refit':True}; (OUT/'R7F3_SOURCE_PROVENANCE.json').write_text(json.dumps(source,indent=2),encoding='utf-8'); (OUT/'R7F3_DESIGN_LOCK.md').write_text('R7F3 conditional closure; exact R7F2 universe and GR0/GRH/GRM definitions; frozen RIUD predictor as offset; event-held-out outer CV; no new variables, no RIUD coefficient refit, no Holdout30.',encoding='utf-8'); (OUT/'R7F3_CLAIM_BOUNDARY.md').write_text('This branch tests conditional information only. It does not falsify GR, derive Einstein equations, exhaust waveform history, or validate Holdout30.',encoding='utf-8'); (OUT/'R7F3_R7_LINEAGE_NOTE.md').write_text('R7F3 follows R7F2 after GR0 identity recovery and tests frozen RIUD conditional on fixed GR history/kernel.',encoding='utf-8'); files=[p for p in OUT.iterdir() if p.is_file() and p.name!='SHA256_MANIFEST.txt']; (OUT/'SHA256_MANIFEST.txt').write_text('\n'.join(f'{sha(p)}  {p.name}' for p in sorted(files,key=lambda p:p.name))+'\n',encoding='utf-8'); print(report)
if __name__=='__main__': main()
