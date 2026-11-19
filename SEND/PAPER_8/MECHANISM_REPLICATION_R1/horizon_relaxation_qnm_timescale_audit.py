import csv, importlib.metadata
from pathlib import Path
import h5py, numpy as np, qnm

BASE=Path(__file__).resolve().parent.parent / "R8_PHYSICAL_MECHANISM_CLOSURE" / "R8_EXTERNAL_NR_SOURCE_ARCHIVE"
R8=Path(__file__).resolve().parent.parent / "R8_PHYSICAL_MECHANISM_CLOSURE" / "R8_DERIVED_SOURCE_NATIVE"
OUT=Path(__file__).resolve().parent
EVENTS=['0180','0513','0526','1144','1765','2092','2497','2499','2505','2506']
VAR_KEYS={'ArealMass':'ArealMass.dat','DimensionfulInertialSpinMag':'DimensionfulInertialSpinMag.dat','chiMagInertial':'chiMagInertial.dat'}

def cross_time(t,y,target):
    for i in range(1,len(t)):
        if (y[i-1]-target)*(y[i]-target)<=0 and y[i]!=y[i-1]:
            return float(t[i-1]+(target-y[i-1])*(t[i]-t[i-1])/(y[i]-y[i-1]))
    return float('nan')

def main():
    with open(R8/'R8_NR_SOURCE_NATIVE_SUMMARY.csv',encoding='utf-8-sig',newline='') as f: meta={r['EVENT'].split(':')[-1]:r for r in csv.DictReader(f)}
    rows=[]
    for ev in EVENTS:
        with h5py.File(BASE/ev/'Horizons.h5','r') as f:
            for v,key in VAR_KEYS.items():
                a=np.asarray(f['AhC.dir/'+key][:],float); t=a[:,0]-a[0,0]; y=a[:,1]
                ini=float(y[0]); fin=float(y[-1]); d=fin-ini
                q={f'TAU_TO_{p}P':cross_time(t,y,ini+(p/100.0)*d) for p in [50,90]}
                row={'EVENT':ev,'VARIABLE':v,'INITIAL_VALUE':ini,'FINAL_VALUE':fin,'DELTA':d,'TAU_TO_50P':q['TAU_TO_50P'],'TAU_TO_90P':q['TAU_TO_90P']}
                rows.append(row)
        a=meta[ev]; chi=float(a['AHC_CHI_FINAL']); mf=float(a['AHC_CHRISTODOULOU_MASS_FINAL'])
        w,_,_=qnm.modes_cache(s=-2,l=2,m=2,n=0)(chi)
        for r in [x for x in rows if x['EVENT']==ev]:
            r.update({'CHI_F_USED':chi,'FINAL_M_OVER_INITIAL_USED':mf,'QNM_220_DAMPING_MF':float(-1/w.imag),'QNM_220_DAMPING_INITIAL_M':float(-1/w.imag*mf),'QNM_LIBRARY':'qnm','QNM_VERSION':importlib.metadata.version('qnm')})
    with (OUT/'SXS10_HORIZON_RELAXATION_QNM_TIMESCALE.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    lines=['# Horizon relaxation versus Kerr QNM timescale audit','','For each SXS10 event, the first crossing of 50% and 90% of the AhC-to-final scalar change was read from the native `Horizons.h5` series. The comparison QNM scale is the source-native final-spin `(2,2,0)` damping time from qnm 0.4.4, converted to initial-M units with the preserved final-mass ratio. No relaxation fit or parameter tuning was performed.']
    for v in VAR_KEYS:
        q=[r for r in rows if r['VARIABLE']==v]
        vals50=np.array([float(r['TAU_TO_50P']) for r in q]); vals90=np.array([float(r['TAU_TO_90P']) for r in q]); tau=np.array([float(r['QNM_220_DAMPING_INITIAL_M']) for r in q])
        lines.append(f"- {v}: median tau50={np.nanmedian(vals50):.6g}M, median tau90={np.nanmedian(vals90):.6g}M; median QNM tau={np.nanmedian(tau):.6g}M")
    lines += ['', 'The crossing times are descriptive relaxation times, not a proof that the scalar horizon evolution is a QNM ringdown.']
    (OUT/'SXS10_HORIZON_RELAXATION_QNM_TIMESCALE_AUDIT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__': main()
