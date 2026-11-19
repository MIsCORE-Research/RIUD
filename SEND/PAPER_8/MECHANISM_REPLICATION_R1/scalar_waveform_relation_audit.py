import csv
from pathlib import Path
import numpy as np

OUT=Path(__file__).resolve().parent
R8=Path(__file__).resolve().parent.parent / "R8_PHYSICAL_MECHANISM_CLOSURE" / "R8_DERIVED_SOURCE_NATIVE"
EVENTS=['0180','0513','0526','1144','1765','2092','2497','2499','2505','2506']
VARS=['ArealMass','DimensionfulInertialSpinMag','chiMagInertial']

def rank(x):
    o=np.argsort(x,kind='mergesort'); r=np.empty(len(x),float); r[o]=np.arange(len(x),dtype=float); return r
def corr(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    if len(a)<3 or np.std(a)==0 or np.std(b)==0:return float('nan')
    return float(np.corrcoef(a,b)[0,1])

def main():
    with open(OUT/'SXS10_HORIZON_SCALAR_TRANSIENT.csv',encoding='utf-8-sig',newline='') as f: scalar=list(csv.DictReader(f))
    with open(R8/'R8_MODE_TIME_SERIES.csv',encoding='utf-8-sig',newline='') as f: modes=list(csv.DictReader(f))
    rows=[]
    for ev in EVENTS:
        peak={}
        for mode in ['h22','h44']:
            q=[r for r in modes if r['EVENT']==('SXS:BBH:'+ev) and r['MODE']==mode]
            q=[r for r in q if 0<=float(r['TAU_FROM_COMMON_HORIZON'])<50]
            peak[mode]=max(q,key=lambda r:float(r['AMP'])) if q else None
        for v in VARS:
            s=next(r for r in scalar if r['EVENT']==ev and r['VARIABLE']==v)
            rows.append({'EVENT':ev,'VARIABLE':v,'EARLY_MINUS_LATE':s['EARLY_MINUS_LATE'],'H22_PEAK_TAU_0_50M':peak['h22']['TAU_FROM_COMMON_HORIZON'] if peak['h22'] else '','H44_PEAK_TAU_0_50M':peak['h44']['TAU_FROM_COMMON_HORIZON'] if peak['h44'] else ''})
    with (OUT/'SXS10_SCALAR_WAVEFORM_RELATION.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    summary=[]
    for v in VARS:
        q=[r for r in rows if r['VARIABLE']==v]
        x=np.array([float(r['EARLY_MINUS_LATE']) for r in q])
        for mode in ['H22','H44']:
            y=np.array([float(r[f'{mode}_PEAK_TAU_0_50M']) for r in q])
            summary.append({'VARIABLE':v,'WAVEFORM':mode.lower(),'N':len(q),'PEARSON':corr(x,y),'SPEARMAN':corr(rank(x),rank(y)),'MEDIAN_PEAK_TAU':float(np.median(y))})
    with (OUT/'SXS10_SCALAR_WAVEFORM_RELATION_SUMMARY.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
    lines=['# SXS10 scalar horizon change versus waveform peak audit','','Scalar predictor: fixed AhC-relative early-minus-late mean in 0–5M versus 25–50M. Waveform response: independently read h22/h44 amplitude peak in fixed 0–50M. No regression, coefficient fit, event removal, or timing adjustment was performed.']
    for r in summary: lines.append(f"- {r['VARIABLE']} vs {r['WAVEFORM']}: Pearson={r['PEARSON']:.6g}, Spearman={r['SPEARMAN']:.6g}, N={r['N']}")
    lines += ['', 'These are descriptive event-level associations, not evidence of causation or a replacement for the frozen RIUD S law.']
    (OUT/'SXS10_SCALAR_WAVEFORM_RELATION_AUDIT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__':main()
