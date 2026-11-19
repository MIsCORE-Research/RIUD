import csv
from pathlib import Path
import numpy as np, sxs
from sxs.waveforms import energy_flux, angular_momentum_flux

ARCH=Path(__file__).resolve().parent.parent / "R8_PHYSICAL_MECHANISM_CLOSURE" / "R8_EXTERNAL_NR_SOURCE_ARCHIVE"
R8=Path(__file__).resolve().parent.parent / "R8_PHYSICAL_MECHANISM_CLOSURE" / "R8_DERIVED_SOURCE_NATIVE"
OUT=Path(__file__).resolve().parent
EVENTS=['0180','0513','0526','1144','1765','2092','2497','2499','2505','2506']

def integ(t,y,lo,hi):
    ok=(t>=lo)&(t<hi)&np.isfinite(y)
    return float(np.trapezoid(y[ok],t[ok])) if ok.sum()>1 else float('nan')
def peak(t,y,lo=0,hi=50):
    ok=(t>=lo)&(t<hi)&np.isfinite(y)
    if not ok.any(): return float('nan')
    return float(t[np.where(ok)[0][np.argmax(y[ok])]])

def main():
    with open(R8/'R8_NR_SOURCE_NATIVE_SUMMARY.csv',encoding='utf-8-sig',newline='') as f: meta={r['EVENT'].split(':')[-1]:r for r in csv.DictReader(f)}
    rows=[]
    for ev in EVENTS:
        ch=float(meta[ev]['COMMON_HORIZON_TIME']); x=sxs.load(str(ARCH/ev/'Strain_N2.h5')); t=np.asarray(x.t,float); tau=t-ch
        ef=np.asarray(energy_flux(x),float); jf=np.asarray(angular_momentum_flux(x),float); jn=np.linalg.norm(jf,axis=1)
        h22=abs(np.asarray(x[:,x.index(2,2)],complex)); h44=abs(np.asarray(x[:,x.index(4,4)],complex)); h22p=peak(tau,h22); h44p=peak(tau,h44); efp=peak(tau,ef); jfp=peak(tau,jn)
        total_e=integ(tau,ef,0,50); total_j=integ(tau,jn,0,50)
        landmarks={'H22_PEAK':h22p,'H44_PEAK':h44p,'J_FLUX_PEAK':jfp,'E_FLUX_PEAK':efp,'QNM_220_APPROX':11.7}
        for name,lt in landmarks.items():
            rows.append({'EVENT':ev,'LANDMARK':name,'TAU_LANDMARK':lt,'E_CUMULATIVE_0_TO_LANDMARK':integ(tau,ef,0,lt),'E_TOTAL_0_TO_50':total_e,'E_FRACTION':integ(tau,ef,0,lt)/total_e if total_e else '','J_NORM_CUMULATIVE_0_TO_LANDMARK':integ(tau,jn,0,lt),'J_NORM_TOTAL_0_TO_50':total_j,'J_NORM_FRACTION':integ(tau,jn,0,lt)/total_j if total_j else ''})
        for lo,hi in [(0,5),(5,10),(10,20),(20,40),(40,50)]:
            rows.append({'EVENT':ev,'LANDMARK':f'WINDOW_{lo}_{hi}M','TAU_LANDMARK':hi,'E_CUMULATIVE_0_TO_LANDMARK':integ(tau,ef,lo,hi),'E_TOTAL_0_TO_50':total_e,'E_FRACTION':integ(tau,ef,lo,hi)/total_e if total_e else '','J_NORM_CUMULATIVE_0_TO_LANDMARK':integ(tau,jn,lo,hi),'J_NORM_TOTAL_0_TO_50':total_j,'J_NORM_FRACTION':integ(tau,jn,lo,hi)/total_j if total_j else ''})
    with (OUT/'SXS10_RADIATIVE_HISTORY_AUDIT.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    lines=['# SXS10 source-native radiative-history audit','','Energy flux and angular-momentum-flux norm were integrated directly from original Strain_N2.h5 on a fixed AhC-relative 0–50M support. Landmark rows use h22/h44 peak, flux peaks, and a fixed 11.7M QNM reference marker; window rows are fixed intervals. This is descriptive history accounting only, with no fit or R40 likelihood modification.']
    for lm in ['H22_PEAK','H44_PEAK','J_FLUX_PEAK','E_FLUX_PEAK','QNM_220_APPROX']:
        q=[r for r in rows if r['LANDMARK']==lm]; lines.append(f"- {lm}: median E cumulative fraction={np.median([float(r['E_FRACTION']) for r in q]):.6g}; median J-norm cumulative fraction={np.median([float(r['J_NORM_FRACTION']) for r in q]):.6g}; N={len(q)}")
    for wname in ['WINDOW_0_5M','WINDOW_5_10M','WINDOW_10_20M','WINDOW_20_40M','WINDOW_40_50M']:
        q=[r for r in rows if r['LANDMARK']==wname]; lines.append(f"- {wname}: median E share={np.median([float(r['E_FRACTION']) for r in q]):.6g}; median J-norm share={np.median([float(r['J_NORM_FRACTION']) for r in q]):.6g}")
    lines += ['', 'These fractions describe where radiation is distributed in the source-native interval; they do not establish that cumulative radiation is the microscopic origin of RIUD memory or S.']
    (OUT/'SXS10_RADIATIVE_HISTORY_AUDIT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__':main()
