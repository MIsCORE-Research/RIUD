import csv
from pathlib import Path
import numpy as np, h5py

ROOT=Path(r'E:/RIUD_ACTIVE_20260808/MIsCORE_RIUD_AUXILIARY_HORIZONDUMP_MECHANISM_TEST_R0_20260827/0320')
OUT=Path(__file__).resolve().parent
VARS=['SpinFunction','WeylE_NN','WeylB_NN','DimlessRicciScalar']
def td(f,base):
    idx=np.asarray(f[base+'/index.dat'][:],float); dat=np.asarray(f[base+'/data.dat'][:],float).ravel(); out=[]
    for q in idx:
        end=int(q[1]); n=int(q[2]*q[3]); x=dat[end-n:end]; out.append((q[0],float(np.mean(x)),float(np.sqrt(np.mean(x*x)))))
    return np.asarray(out)
def main():
    with h5py.File(ROOT/'HorizonsDump.h5','r') as f:
        d={(ah,v):td(f,f'{ah}.dir/{v}.tdm') for ah in ['AhA','AhB','AhC'] for v in VARS}
    t0=d[('AhC','SpinFunction')][0,0]; rows=[]
    for (ah,v),x in d.items():
        for i,q in enumerate(x): rows.append({'EVENT':'0320','AH':ah,'VARIABLE':v,'INDEX':i,'T_NATIVE':q[0],'TAU_FROM_AHC':q[0]-t0,'ANGULAR_MEAN':q[1],'ANGULAR_RMS':q[2]})
    with open(OUT/'AUX0320_SURFACE_TIMESERIES.csv','w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    sm=[]
    for v in VARS:
        x=d[('AhC',v)];
        for name,lo,hi in [('EARLY_0_5M',0,5),('LATE_25_50M',25,50)]:
            ok=(x[:,0]-t0>=lo)&(x[:,0]-t0<hi); sm.append({'EVENT':'0320','VARIABLE':v,'WINDOW':name,'N':int(ok.sum()),'MEAN_RMS':float(x[ok,2].mean()) if ok.any() else '','MEAN_VARIANCE_NOT_AVAILABLE':'RMS-only extractor'})
    with open(OUT/'AUX0320_SURFACE_WINDOW_SUMMARY.csv','w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=list(sm[0]));w.writeheader();w.writerows(sm)
    (OUT/'AUX0320_SOURCE_NOTE.md').write_text('# SXS:BBH:0320 auxiliary surface audit\n\nSame source-native fields and fixed AhC-relative windows as the 0319/0323 audit. Waveform and observational labels are not used.\n',encoding='utf-8')
if __name__=='__main__':main()
