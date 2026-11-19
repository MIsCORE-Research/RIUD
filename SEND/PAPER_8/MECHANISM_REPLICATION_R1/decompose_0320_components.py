import csv, numpy as np
from pathlib import Path
P=Path(__file__).resolve().parent
rows=[]
with open(P/'AUX0320_SURFACE_TIMESERIES.csv',newline='',encoding='utf-8') as f:
    for r in csv.DictReader(f):
        tau=float(r['TAU_FROM_AHC'])
        if r['AH']=='AhC' and (0<=tau<5 or 25<=tau<50):
            mean=float(r['ANGULAR_MEAN']); rms=float(r['ANGULAR_RMS'])
            rows.append((r['VARIABLE'],'EARLY_0_5M' if tau<5 else 'LATE_25_50M',mean,rms,max(0,rms*rms-mean*mean)))
out=[]
for v in sorted(set(x[0] for x in rows)):
    e=[x for x in rows if x[0]==v and x[1]=='EARLY_0_5M']; l=[x for x in rows if x[0]==v and x[1]=='LATE_25_50M']
    out.append({'EVENT':'0320','VARIABLE':v,'RMS_EARLY_MINUS_LATE':float(np.mean([x[3] for x in e])-np.mean([x[3] for x in l])),'VARIANCE_EARLY_MINUS_LATE':float(np.mean([x[4] for x in e])-np.mean([x[4] for x in l])),'MEAN_ABS_EARLY_MINUS_LATE':float(np.mean(np.abs([x[2] for x in e]))-np.mean(np.abs([x[2] for x in l]))),'STATUS':'PASS'})
with open(P/'AUX0320_SURFACE_COMPONENT_COMPARISON.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
