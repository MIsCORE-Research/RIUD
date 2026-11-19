import csv
from pathlib import Path
import h5py, numpy as np, sxs
from sxs.waveforms import energy_flux, angular_momentum_flux

ARCH=Path(__file__).resolve().parent.parent / "R8_PHYSICAL_MECHANISM_CLOSURE" / "R8_EXTERNAL_NR_SOURCE_ARCHIVE"
R8=Path(__file__).resolve().parent.parent / "R8_PHYSICAL_MECHANISM_CLOSURE" / "R8_DERIVED_SOURCE_NATIVE"
OUT=Path(__file__).resolve().parent
EVENTS=['0180','0513','0526','1144','1765','2092','2497','2499','2505','2506']

def peak(t,y):
    ok=(t>=0)&(t<50)&np.isfinite(y)
    if not ok.any(): return float('nan')
    return float(t[np.where(ok)[0][np.argmax(y[ok])]])

def main():
    with open(R8/'R8_NR_SOURCE_NATIVE_SUMMARY.csv',encoding='utf-8-sig',newline='') as f: meta={r['EVENT'].split(':')[-1]:r for r in csv.DictReader(f)}
    rows=[]
    for ev in EVENTS:
        ch=float(meta[ev]['COMMON_HORIZON_TIME'])
        with h5py.File(ARCH/ev/'Horizons.h5','r') as f:
            series={k:np.asarray(f['AhC.dir/'+k+'.dat'][:],float) for k in ['ArealMass','chiMagInertial','DimensionfulInertialSpinMag']}
        hp={}
        for k,a in series.items():
            t=a[:,0]-ch; y=np.gradient(a[:,1],a[:,0]); hp[k]=peak(t,np.abs(y))
        x=sxs.load(str(ARCH/ev/'Strain_N2.h5')); tau=np.asarray(x.t,float)-ch
        ef=np.asarray(energy_flux(x),float); jf=np.asarray(angular_momentum_flux(x),float)
        fp={'ENERGY_FLUX':peak(tau,ef),'J_FLUX_NORM':peak(tau,np.linalg.norm(jf,axis=1))}
        for hv,ht in hp.items():
            for fv,ft in fp.items():
                rows.append({'EVENT':ev,'HORIZON_DERIVATIVE':hv,'HORIZON_DERIVATIVE_PEAK_TAU':ht,'HORIZON_DERIVATIVE_PEAK_AT_AHC_BOUNDARY':abs(ht)<1e-6,'FLUX':fv,'FLUX_PEAK_TAU':ft,'HORIZON_DERIVATIVE_BEFORE_FLUX':ht<ft,'ABS_TIME_DIFFERENCE':abs(ht-ft)})
    with (OUT/'SXS10_HORIZON_FLUX_ORDER_AUDIT.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    lines=['# SXS10 horizon-derivative versus flux ordering audit','','Full native `Horizons.h5` scalar series and original `Strain_N2.h5` were used. Absolute first-derivative peaks and flux maxima were measured in a fixed 0–50M AhC-relative window. This is a timing-order diagnostic, not a balance-law fit.']
    for hv in ['ArealMass','chiMagInertial','DimensionfulInertialSpinMag']:
        for fv in ['ENERGY_FLUX','J_FLUX_NORM']:
            q=[r for r in rows if r['HORIZON_DERIVATIVE']==hv and r['FLUX']==fv]
            lines.append(f"- {hv} derivative before {fv}: {sum(r['HORIZON_DERIVATIVE_BEFORE_FLUX'] for r in q)}/{len(q)}; boundary-peaked={sum(r['HORIZON_DERIVATIVE_PEAK_AT_AHC_BOUNDARY'] for r in q)}/{len(q)}; median |Δtau|={np.median([float(r['ABS_TIME_DIFFERENCE']) for r in q]):.6g}M")
    lines += ['', 'The derivative peak is not interpreted as absorbed flux because the source-native files do not provide an exact horizon-to-infinity balance binding for this audit.']
    (OUT/'SXS10_HORIZON_FLUX_ORDER_AUDIT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__':main()
