import csv
from pathlib import Path
import numpy as np, sxs
from sxs.waveforms import energy_flux, angular_momentum_flux

ARCH=Path(__file__).resolve().parent.parent / "R8_PHYSICAL_MECHANISM_CLOSURE" / "R8_EXTERNAL_NR_SOURCE_ARCHIVE"
R8=Path(__file__).resolve().parent.parent / "R8_PHYSICAL_MECHANISM_CLOSURE" / "R8_DERIVED_SOURCE_NATIVE"
OUT=Path(__file__).resolve().parent
EVENTS=['0180','0513','0526','1144','1765','2092','2497','2499','2505','2506']

def peak(t,y,lo=0,hi=50):
    ok=(t>=lo)&(t<hi)&np.isfinite(y)
    if not ok.any(): return float('nan'),float('nan'),0
    j=np.where(ok)[0][np.argmax(y[ok])]
    return float(t[j]),float(y[j]),int(ok.sum())

def main():
    with open(R8/'R8_NR_SOURCE_NATIVE_SUMMARY.csv',encoding='utf-8-sig',newline='') as f: meta={r['EVENT'].split(':')[-1]:r for r in csv.DictReader(f)}
    scalar={}
    with open(OUT/'SXS10_HORIZON_RELAXATION_QNM_TIMESCALE.csv',encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f): scalar.setdefault(r['EVENT'],{})[r['VARIABLE']]=r
    rows=[]
    for ev in EVENTS:
        x=sxs.load(str(ARCH/ev/'Strain_N2.h5')); t=np.asarray(x.t,float); ch=float(meta[ev]['COMMON_HORIZON_TIME']); tau=t-ch
        ef=np.asarray(energy_flux(x),float); jf=np.asarray(angular_momentum_flux(x),float); jmag=np.linalg.norm(jf,axis=1)
        h22=np.abs(np.asarray(x[:,x.index(2,2)],complex)); h44=np.abs(np.asarray(x[:,x.index(4,4)],complex))
        e_t,e_v,e_n=peak(tau,ef); j_t,j_v,j_n=peak(tau,jmag); h22_t,h22_v,h22_n=peak(tau,h22); h44_t,h44_v,h44_n=peak(tau,h44)
        base={'EVENT':ev,'H22_PEAK':h22_t,'H44_PEAK':h44_t}
        for v in ['ArealMass','DimensionfulInertialSpinMag','chiMagInertial']:
            s=scalar[ev][v]; tag=v.upper()
            base['TAU50_'+tag]=s['TAU_TO_50P']; base['TAU90_'+tag]=s['TAU_TO_90P']
        for obs,tv,vv,nn in [('ENERGY_FLUX_PEAK',e_t,e_v,e_n),('ANGULAR_MOMENTUM_FLUX_NORM_PEAK',j_t,j_v,j_n)]:
            row=dict(base); row.update({'OBSERVABLE':obs,'TAU_FROM_AHC':tv,'VALUE':vv,'N_WINDOW':nn})
            row['ORDER_TAU50_BEFORE_'+obs]=all(float(row['TAU50_'+v.upper()])<tv for v in ['ArealMass','DimensionfulInertialSpinMag','chiMagInertial'])
            row['ORDER_FLUX_BEFORE_H22']=tv<h22_t; row['ORDER_FLUX_BEFORE_H44']=tv<h44_t; rows.append(row)
    with (OUT/'SXS10_RADIATIVE_TIMING_AUDIT.csv').open('w',newline='',encoding='utf-8') as f:
        cols=sorted({k for r in rows for k in r}); w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)
    lines=['# SXS10 source-native radiative timing audit','','Original Strain_N2.h5 files were loaded directly. Energy flux and angular-momentum flux were calculated with the installed sxs waveform routines. Peaks are independent maxima in the fixed AhC-relative 0–50M window. Scalar tau50/tau90 values come from the fixed horizon audit; no timing fit or event-specific selection was used.']
    for obs in ['ENERGY_FLUX_PEAK','ANGULAR_MOMENTUM_FLUX_NORM_PEAK']:
        q=[r for r in rows if r['OBSERVABLE']==obs]; key='ORDER_TAU50_BEFORE_'+obs; lines.append(f"- {obs}: median peak tau={np.median([float(r['TAU_FROM_AHC']) for r in q]):.6g}M; all scalar tau50 before peak={sum(r[key] for r in q)}/{len(q)}; peak before h22={sum(r['ORDER_FLUX_BEFORE_H22'] for r in q)}/{len(q)}; peak before h44={sum(r['ORDER_FLUX_BEFORE_H44'] for r in q)}/{len(q)}")
    lines += ['', 'This establishes source-native temporal ordering only; it does not identify the flux peak with the observational GAP or the frozen RIUD transition.']
    (OUT/'SXS10_RADIATIVE_TIMING_AUDIT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__':main()
