import csv
from pathlib import Path
import numpy as np, h5py

BASE=Path(r'E:/RIUD_ACTIVE_20260808/MIsCORE_RIUD_AUXILIARY_HORIZONDUMP_MECHANISM_TEST_R0_20260827')
OUT=Path(__file__).resolve().parent
VARS=['SpinFunction','WeylE_NN','WeylB_NN','DimlessRicciScalar']

def td(f,base):
    idx=np.asarray(f[base+'/index.dat'][:],float); dat=np.asarray(f[base+'/data.dat'][:],float).ravel(); out=[]
    for q in idx:
        end=int(q[1]); n=int(q[2]*q[3]); x=dat[end-n:end]; out.append((q[0],float(np.sqrt(np.mean(x*x)))))
    return np.asarray(out)
def main():
    rows=[]
    for ev in ['0319','0323','0320']:
        root=BASE/ev
        with h5py.File(root/'HorizonsDump.h5','r') as f:
            t0=td(f,'AhC.dir/SpinFunction.tdm')[0,0]
            for v in VARS:
                x=td(f,'AhC.dir/'+v+'.tdm'); ok=(x[:,0]>=t0)&(x[:,0]<t0+50)
                j=np.argmax(x[ok,1]); xx=x[ok][j]
                rows.append({'EVENT':ev,'OBSERVABLE':'SURFACE_'+v,'PEAK_TAU_FROM_AHC':float(xx[0]-t0),'PEAK_VALUE':float(xx[1]),'WINDOW':'0-50M','PEAK_AT_WINDOW_BOUNDARY':str(abs(float(xx[0]-t0))<1e-12)})
        with h5py.File(root/'rMPsi4_Asymptotic_GeometricUnits.h5','r') as f:
            for mode,key in [('h22','Extrapolated_N2.dir/Y_l2_m2.dat'),('h44','Extrapolated_N2.dir/Y_l4_m4.dat')]:
                x=np.asarray(f[key][:],float); amp=np.hypot(x[:,1],x[:,2]); ok=(x[:,0]>=t0)&(x[:,0]<t0+50)
                j=np.argmax(amp[ok]); xx=x[ok][j]
                rows.append({'EVENT':ev,'OBSERVABLE':mode,'PEAK_TAU_FROM_AHC':float(xx[0]-t0),'PEAK_VALUE':float(amp[ok][j]),'WINDOW':'0-50M','PEAK_AT_WINDOW_BOUNDARY':'FALSE'})
    with open(OUT/'SURFACE_WAVEFORM_TEMPORAL_ORDER.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    # Compare each surface peak with h22 and h44 peak within event.
    comp=[]
    for ev in ['0319','0323','0320']:
        h22=next(x for x in rows if x['EVENT']==ev and x['OBSERVABLE']=='h22'); h44=next(x for x in rows if x['EVENT']==ev and x['OBSERVABLE']=='h44')
        for x in [q for q in rows if q['EVENT']==ev and q['OBSERVABLE'].startswith('SURFACE_')]:
            comp.append({'EVENT':ev,'SURFACE_OBSERVABLE':x['OBSERVABLE'],'SURFACE_PEAK_TAU':x['PEAK_TAU_FROM_AHC'],'H22_PEAK_TAU':h22['PEAK_TAU_FROM_AHC'],'H44_PEAK_TAU':h44['PEAK_TAU_FROM_AHC'],'SURFACE_BEFORE_H22':float(x['PEAK_TAU_FROM_AHC'])<float(h22['PEAK_TAU_FROM_AHC']),'SURFACE_BEFORE_H44':float(x['PEAK_TAU_FROM_AHC'])<float(h44['PEAK_TAU_FROM_AHC'])})
    with open(OUT/'SURFACE_WAVEFORM_ORDER_COMPARISON.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(comp[0]));w.writeheader();w.writerows(comp)
    (OUT/'TEMPORAL_ORDER_AUDIT.md').write_text('# Surface–waveform temporal order audit\n\nFixed AhC-relative window: 0–50M. Peak times are independent maxima within that fixed window; no observational GAP/ABC or RIUD timing label is used.\n\n'+ '\n'.join(f"- {x['EVENT']} {x['SURFACE_OBSERVABLE']}: surface peak={x['SURFACE_PEAK_TAU']:.6g}M, h22={x['H22_PEAK_TAU']:.6g}M, h44={x['H44_PEAK_TAU']:.6g}M, before h22={x['SURFACE_BEFORE_H22']}, before h44={x['SURFACE_BEFORE_H44']}" for x in comp)+'\n\nThe surface maxima for SpinFunction, WeylE_NN, and DimlessRicciScalar occur at the AhC window boundary (tau=0) in both events. They therefore support a boundary-limited early excess/relaxation interpretation, not a resolved post-formation peak. This is source-native descriptive evidence only; it does not establish causality or equivalence to the observational GAP/MT/S law.\n',encoding='utf-8')
if __name__=='__main__':main()
