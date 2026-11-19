import csv
from pathlib import Path
import h5py
import numpy as np

BASE = Path(__file__).resolve().parent.parent / "R8_PHYSICAL_MECHANISM_CLOSURE" / "R8_EXTERNAL_NR_SOURCE_ARCHIVE"
OUT = Path(__file__).resolve().parent
EVENTS = ['0180','0513','0526','1144','1765','2092','2497','2499','2505','2506']
VARS = {
    'ArealMass': 'ArealMass.dat',
    'DimensionfulInertialSpinMag': 'DimensionfulInertialSpinMag.dat',
    'chiMagInertial': 'chiMagInertial.dat',
}

def main():
    rows=[]
    for ev in EVENTS:
        with h5py.File(BASE/ev/'Horizons.h5','r') as f:
            series={k:np.asarray(f['AhC.dir/'+fn][:],float) for k,fn in VARS.items()}
        t0=float(series['ArealMass'][0,0])
        for name,x in series.items():
            tau=x[:,0]-t0; y=x[:,1]
            early=y[(tau>=0)&(tau<5)]
            late=y[(tau>=25)&(tau<50)]
            rows.append({'EVENT':ev,'VARIABLE':name,'AHC_NATIVE_T0':t0,'EARLY_WINDOW':'0_5M','LATE_WINDOW':'25_50M','EARLY_N':len(early),'LATE_N':len(late),'EARLY_MEAN':float(np.mean(early)) if len(early) else '','LATE_MEAN':float(np.mean(late)) if len(late) else '','EARLY_MINUS_LATE':float(np.mean(early)-np.mean(late)) if len(early) and len(late) else '','EARLY_TO_LATE_RATIO':float(np.mean(early)/np.mean(late)) if len(early) and len(late) and np.mean(late)!=0 else '','STATUS':'PASS' if len(early) and len(late) else 'INSUFFICIENT_SUPPORT'})
    with (OUT/'SXS10_HORIZON_SCALAR_TRANSIENT.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    summaries=[]
    for v in VARS:
        q=[r for r in rows if r['VARIABLE']==v and r['STATUS']=='PASS']
        dif=np.array([float(r['EARLY_MINUS_LATE']) for r in q])
        summaries.append({'VARIABLE':v,'EVENTS_PASS':len(q),'EVENTS_TOTAL':len(EVENTS),'SAME_DIRECTION_COUNT':int(np.sum(dif>0)),'OPPOSITE_DIRECTION_COUNT':int(np.sum(dif<0)),'ZERO_COUNT':int(np.sum(dif==0)),'MEDIAN_EARLY_MINUS_LATE':float(np.median(dif)),'MIN_EARLY_MINUS_LATE':float(np.min(dif)),'MAX_EARLY_MINUS_LATE':float(np.max(dif))})
    with (OUT/'SXS10_HORIZON_SCALAR_TRANSIENT_SUMMARY.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(summaries[0]));w.writeheader();w.writerows(summaries)
    lines=['# SXS10 source-native AhC scalar transient audit','','Fixed, prespecified comparison: AhC-relative 0–5M versus 25–50M. No observational GAP/MT/ABC label, SXS fitting, threshold tuning, or event-specific adjustment was used. The audited quantities are AhC ArealMass, DimensionfulInertialSpinMag, and chiMagInertial from the preserved Horizons.h5 files.']
    for r in summaries:
        lines.append(f"- {r['VARIABLE']}: {r['SAME_DIRECTION_COUNT']}/{r['EVENTS_PASS']} early-minus-late positive; median difference={r['MEDIAN_EARLY_MINUS_LATE']:.8g}; range=[{r['MIN_EARLY_MINUS_LATE']:.8g},{r['MAX_EARLY_MINUS_LATE']:.8g}]")
    lines += ['', 'This is a scalar horizon-geometry relaxation audit, not an angular surface-field replication and not a microscopic derivation of the RIUD S law.']
    (OUT/'SXS10_HORIZON_SCALAR_TRANSIENT_AUDIT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

if __name__=='__main__': main()
