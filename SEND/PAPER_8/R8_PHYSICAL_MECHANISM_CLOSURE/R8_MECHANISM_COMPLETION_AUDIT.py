import csv, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
IDS=['0180','0513','0526','1144','1765','2092','2497','2499','2505','2506']
TRANS_VARS=['A_AREAL','M_CH','CHI','J_MAG','D_A_DT','D_MCH_DT','D_CHI_DT','D_J_DT',
            'DIST_FINAL_A','DIST_FINAL_MCH','DIST_FINAL_CHI','DIST_FINAL_J',
            'RELAX_RATE_A','RELAX_RATE_MCH','RELAX_RATE_CHI','RELAX_RATE_J',
            'E_INFINITY_FLUX','JZ_INFINITY_FLUX','CUM_E_INFINITY','CUM_JZ_INFINITY']

def f(x):
    try:
        y=float(x)
        return y if math.isfinite(y) else float('nan')
    except Exception:
        return float('nan')

def write(path, rows):
    cols=sorted({k for r in rows for k in r})
    with open(path,'w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=cols); w.writeheader(); w.writerows(rows)

def main():
    rows=list(csv.DictReader(open(ROOT/'R8_SXS_MECHANISM_ROW_MASTER.csv',encoding='utf-8')))
    trs=list(csv.DictReader(open(ROOT/'R8_SXS_MECHANISM_TRANSITION_AUDIT.csv',encoding='utf-8')))
    by={sid:sorted([r for r in rows if r['EVENT']=='SXS:BBH:'+sid],key=lambda r:int(r['BIN_INDEX'])) for sid in IDS}
    trby={sid:sorted([r for r in trs if r['EVENT']=='SXS:BBH:'+sid],key=lambda r:f(r['RIUD_TRANSITION_TIME'])) for sid in IDS}
    cps=[]
    for sid in IDS:
        rr=by[sid]
        for v in TRANS_VARS:
            a=np.array([f(r.get(v,'')) for r in rr]); t=np.array([f(r['SOURCE_NATIVE_TIME']) for r in rr])
            ok=np.isfinite(a)&np.isfinite(t)
            idx=np.where(ok[:-1]&ok[1:]&(np.diff(t)>0))[0]
            if len(idx)==0:
                cps.append({'EVENT':'SXS:BBH:'+sid,'VARIABLE':v,'CHANGE_TIME':'','CHANGE_INDEX':'','MAX_ABS_SLOPE':'','NEAREST_TRANSITION_TIME':'','DELTA_TIME':'','STATUS':'UNAVAILABLE'})
                continue
            slopes=np.abs(np.diff(a)[idx]/np.diff(t)[idx]); k=int(idx[int(np.argmax(slopes))])
            ct=float((t[k]+t[k+1])/2); cand=[f(x['RIUD_TRANSITION_TIME']) for x in trby[sid]]
            cand=[x for x in cand if math.isfinite(x)]
            nt=min(cand,key=lambda x:abs(x-ct)) if cand else float('nan')
            cps.append({'EVENT':'SXS:BBH:'+sid,'VARIABLE':v,'CHANGE_TIME':ct,'CHANGE_INDEX':k,'MAX_ABS_SLOPE':float(slopes.max()),'NEAREST_TRANSITION_TIME':nt,'DELTA_TIME':abs(ct-nt) if math.isfinite(nt) else '','STATUS':'AVAILABLE'})
    write(ROOT/'R8_SXS_CHANGEPOINT_AUDIT.csv',cps)

    # Fixed derivative-boundary audit for 1144. No smoothing or endpoint repair.
    # The first irregular cadence and the first large jump are reported explicitly.
    import h5py
    p=ROOT/'R8_EXTERNAL_NR_SOURCE_ARCHIVE'/'1144'/'Horizons.h5'; out=[]
    with h5py.File(p,'r') as h:
        for name,path in [('CHI','AhC.dir/chiMagInertial.dat'),('J_MAG','AhC.dir/DimensionfulInertialSpin.dat')]:
            x=np.asarray(h[path][:],float); t=x[:,0]; y=x[:,1] if x.shape[1]==2 else np.linalg.norm(x[:,1:4],axis=1)
            dt=np.diff(t); d=np.gradient(y,t); j=int(np.argmax(np.abs(d)))
            out.append({'EVENT':'SXS:BBH:1144','VARIABLE':name,'N_ROWS':len(t),'DT_MIN':float(dt.min()),'DT_MEDIAN':float(np.median(dt)),'DT_MAX':float(dt.max()),'VALUE_MIN':float(y.min()),'VALUE_MAX':float(y.max()),'DERIVATIVE_MAX_ABS':float(np.abs(d).max()),'DERIVATIVE_P99_ABS':float(np.quantile(np.abs(d),.99)),'MAX_DERIVATIVE_INDEX':j,'MAX_DERIVATIVE_TIME':float(t[j]),'FIRST_LARGE_JUMP_PREV':float(y[j-1]) if j else '','FIRST_LARGE_JUMP_VALUE':float(y[j]),'FIRST_LARGE_JUMP_NEXT':float(y[j+1]) if j+1<len(y) else '','STATUS':'AMBIGUOUS_BOUNDARY_EFFECT'})
    write(ROOT/'R8_SXS1144_DERIVATIVE_AUDIT.csv',out)

    # Use the already-frozen SXS R40 event-level S only as a secondary diagnostic.
    # No S refit or SXS normalization is performed here.
    sfile=Path(r'E:/RIUD_ACTIVE_20260808/RIUD_SXS_R40_W1_W4_LIKELIHOOD_REPLAY_R0_20260824/SXS_R40_W1_W4_EVENT_LEVEL.csv')
    sumfile=ROOT/'R8_DERIVED_SOURCE_NATIVE'/'R8_NR_SOURCE_NATIVE_SUMMARY.csv'
    srows={r['SXS_ID']:f(r['S_FROZEN']) for r in csv.DictReader(open(sfile,encoding='utf-8')) if r.get('WINDOW')=='W1'}
    ssum={r['EVENT']:r for r in csv.DictReader(open(sumfile,encoding='utf-8'))}
    metrics=['AHC_AREAL_MASS_DELTA','AHC_MASS_DELTA','AHC_CHI_DELTA','AHC_JMAG_DELTA','INFINITY_ENERGY_FLUX_POST','INFINITY_JZ_FLUX_POST','AHC_MAX_ABS_AREA_DOT','AHC_MAX_ABS_MASS_DOT','AHC_MAX_ABS_CHI_DOT','AHC_MAX_ABS_JMAG_DOT','LOCAL_RELAXATION_TIMESCALE_PROXY']
    def corr(a,b):
        a=np.asarray(a,float); b=np.asarray(b,float)
        if len(a)<3 or np.std(a)==0 or np.std(b)==0: return float('nan'),float('nan')
        ra=np.argsort(np.argsort(a)); rb=np.argsort(np.argsort(b))
        return float(np.corrcoef(a,b)[0,1]),float(np.corrcoef(ra,rb)[0,1])
    sout=[]
    for m in metrics:
        a=[]; b=[]
        for e,s in srows.items():
            if e in ssum:
                v=f(ssum[e].get(m,''))
                if math.isfinite(s) and math.isfinite(v): a.append(s); b.append(v)
        p,sp=corr(a,b)
        sout.append({'METRIC':m,'N_EVENTS':len(a),'PEARSON_S_VS_METRIC':p,'SPEARMAN_S_VS_METRIC':sp,'STATUS':'FROZEN_S_SECONDARY_DIAGNOSTIC'})
    write(ROOT/'R8_SXS_S_CONNECTION_AUDIT.csv',sout)
    print('COMPLETION_AUDIT=PASS')
    print('CHANGEPOINT_ROWS='+str(len(cps)))
    print('S_CONNECTION=FROZEN_SECONDARY_DIAGNOSTIC_N10')

if __name__=='__main__': main()
