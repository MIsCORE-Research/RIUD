import csv, hashlib
from pathlib import Path
import numpy as np

BASE=Path(r'E:/RIUD_ACTIVE_20260808/MIsCORE_RIUD_AUXILIARY_HORIZONDUMP_MECHANISM_TEST_R0_20260827')
OUT=Path(__file__).resolve().parent

def main():
    rows=[]
    with open(BASE/'AUXILIARY_SURFACE_TIMESERIES.csv',newline='',encoding='utf-8') as f:
        src=csv.DictReader(f)
        for r in src:
            tau=float(r['TAU_FROM_AHC']); mean=float(r['ANGULAR_MEAN']); rms=float(r['ANGULAR_RMS'])
            if 0<=tau<5 or 25<=tau<50:
                rows.append({'EVENT':r['EVENT'],'VARIABLE':r['VARIABLE'],'WINDOW':'EARLY_0_5M' if tau<5 else 'LATE_25_50M','MEAN':mean,'RMS':rms,'VARIANCE':max(0.0,rms*rms-mean*mean),'MAXABS':float(r['ANGULAR_MAXABS'])})
    # time-sample averages, same two fixed windows and no event-dependent selection
    out=[]
    for ev in ['0319','0323']:
        for v in sorted(set(r['VARIABLE'] for r in rows)):
            rr=[r for r in rows if r['EVENT']==ev and r['VARIABLE']==v]
            for w in ['EARLY_0_5M','LATE_25_50M']:
                q=[r for r in rr if r['WINDOW']==w]
                out.append({'EVENT':ev,'VARIABLE':v,'WINDOW':w,'N':len(q),'MEAN_OF_ANGULAR_MEAN':float(np.mean([r['MEAN'] for r in q])),'MEAN_OF_RMS':float(np.mean([r['RMS'] for r in q])),'MEAN_OF_ANGULAR_VARIANCE':float(np.mean([r['VARIANCE'] for r in q])),'MEAN_OF_MAXABS':float(np.mean([r['MAXABS'] for r in q]))})
    with open(OUT/'SURFACE_MEAN_VARIANCE_DECOMPOSITION.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
    comp=[]
    for ev in ['0319','0323']:
        for v in sorted(set(r['VARIABLE'] for r in rows)):
            e=next(x for x in out if x['EVENT']==ev and x['VARIABLE']==v and x['WINDOW']=='EARLY_0_5M'); l=next(x for x in out if x['EVENT']==ev and x['VARIABLE']==v and x['WINDOW']=='LATE_25_50M')
            comp.append({'EVENT':ev,'VARIABLE':v,'RMS_EARLY_MINUS_LATE':e['MEAN_OF_RMS']-l['MEAN_OF_RMS'],'VARIANCE_EARLY_MINUS_LATE':e['MEAN_OF_ANGULAR_VARIANCE']-l['MEAN_OF_ANGULAR_VARIANCE'],'MEAN_ABS_EARLY_MINUS_LATE':abs(e['MEAN_OF_ANGULAR_MEAN'])-abs(l['MEAN_OF_ANGULAR_MEAN']),'MAXABS_EARLY_MINUS_LATE':e['MEAN_OF_MAXABS']-l['MEAN_OF_MAXABS']})
    with open(OUT/'SURFACE_TRANSIENT_COMPONENT_COMPARISON.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(comp[0]));w.writeheader();w.writerows(comp)
    report=['# Surface transient mean/variance decomposition','', 'Fixed windows: AhC 0–5M (early) versus 25–50M (late). Variance is RMS² minus angular-mean², clipped only at numerical zero.']
    for x in comp: report.append(f"- {x['EVENT']} {x['VARIABLE']}: ΔRMS={x['RMS_EARLY_MINUS_LATE']:.9g}; Δvariance={x['VARIANCE_EARLY_MINUS_LATE']:.9g}; Δ|mean|={x['MEAN_ABS_EARLY_MINUS_LATE']:.9g}; Δmaxabs={x['MAXABS_EARLY_MINUS_LATE']:.9g}")
    report += ['', 'Interpretation:', 'Positive Δvariance indicates an early excess in angular nonuniformity; positive Δ|mean| indicates a mean-field contribution. This is component attribution, not a derived GR law.']
    (OUT/'SURFACE_TRANSIENT_DECOMPOSITION.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
if __name__=='__main__':main()
