import csv
from pathlib import Path
import h5py, numpy as np, sxs
from sxs.waveforms import energy_flux, angular_momentum_flux

ARCH=Path(__file__).resolve().parent.parent / "R8_PHYSICAL_MECHANISM_CLOSURE" / "R8_EXTERNAL_NR_SOURCE_ARCHIVE"
R8=Path(__file__).resolve().parent.parent / "R8_PHYSICAL_MECHANISM_CLOSURE" / "R8_DERIVED_SOURCE_NATIVE"
OUT=Path(__file__).resolve().parent
EVENTS=['0180','0513','0526','1144','1765','2092','2497','2499','2505','2506']

def c(a,b):
    m=np.isfinite(a)&np.isfinite(b)
    if m.sum()<5 or np.std(a[m])==0 or np.std(b[m])==0:return float('nan')
    return float(np.corrcoef(a[m],b[m])[0,1])
def lagmax(a,b,grid,lags):
    out=[]
    for lm in lags:
        k=int(round(lm/(grid[1]-grid[0])))
        if k>=0: x,y=a[:-k or None],b[k:]
        else: x,y=a[-k:],b[:k or None]
        out.append((lm,c(x,y)))
    return max(out,key=lambda z:abs(z[1]) if np.isfinite(z[1]) else -1)

def main():
    with open(R8/'R8_NR_SOURCE_NATIVE_SUMMARY.csv',encoding='utf-8-sig',newline='') as f: meta={r['EVENT'].split(':')[-1]:r for r in csv.DictReader(f)}
    rows=[]
    for ev in EVENTS:
        ch=float(meta[ev]['COMMON_HORIZON_TIME'])
        with h5py.File(ARCH/ev/'Horizons.h5','r') as f:
            hs={v:np.asarray(f['AhC.dir/'+v+'.dat'][:],float) for v in ['ArealMass','ChristodoulouMass','chiMagInertial']}
        x=sxs.load(str(ARCH/ev/'Strain_N2.h5')); t=np.asarray(x.t,float); tau=t-ch
        ef=np.asarray(energy_flux(x),float); jf=np.asarray(angular_momentum_flux(x),float); jn=np.linalg.norm(jf,axis=1)
        lo=max(0.0,max(a[:,0].min()-ch for a in hs.values()),tau.min()); hi=min(50.0,min(a[:,0].max()-ch for a in hs.values()),tau.max())
        grid=np.arange(lo,hi,0.1); flux={'ENERGY_FLUX':np.interp(grid,tau,ef),'J_FLUX_NORM':np.interp(grid,tau,jn)}
        deriv={}
        for v,a in hs.items():
            tt=a[:,0]-ch; deriv[v]=np.interp(grid,tt,np.gradient(a[:,1],a[:,0]))
        for window,wlo in [('0_50M',0.0),('5_50M',5.0)]:
            ok=grid>=wlo; lags=np.arange(-20,20.1,1.0)
            for hv in ['ArealMass','ChristodoulouMass','chiMagInertial']:
                for fv in ['ENERGY_FLUX','J_FLUX_NORM']:
                    a=deriv[hv][ok]; b=flux[fv][ok]; g=grid[ok]; z=c(a,b); lm,mc=lagmax(a,b,g,lags)
                    rows.append({'EVENT':ev,'WINDOW':window,'HORIZON_DERIVATIVE':hv,'FLUX':fv,'N':len(a),'ZERO_LAG_CORR':z,'MAX_ABS_CORR_FIXED_LAG':mc,'LAG_AT_MAX_ABS_CORR_M':lm})
    with (OUT/'SXS10_HORIZON_FLUX_TIMESERIES_CORRELATION.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    lines=['# SXS10 horizon-derivative versus radiative-flux time-series correlation','','Full native horizon and strain files were used. Horizon derivatives and sxs-derived radiative fluxes were interpolated onto a fixed 0.1M grid. Correlations and a prespecified ±20M/1M lag scan are descriptive; no coefficient, lag, or balance law was fitted. The 5–50M window is a boundary-exclusion control.']
    for win in ['0_50M','5_50M']:
        for hv in ['ArealMass','ChristodoulouMass','chiMagInertial']:
            for fv in ['ENERGY_FLUX','J_FLUX_NORM']:
                q=[r for r in rows if r['WINDOW']==win and r['HORIZON_DERIVATIVE']==hv and r['FLUX']==fv]
                lines.append(f"- {win} {hv} derivative vs {fv}: median zero-lag r={np.median([float(r['ZERO_LAG_CORR']) for r in q]):.6g}; median max-|r|={np.median([float(r['MAX_ABS_CORR_FIXED_LAG']) for r in q]):.6g}; lag range={min(float(r['LAG_AT_MAX_ABS_CORR_M']) for r in q):.6g}..{max(float(r['LAG_AT_MAX_ABS_CORR_M']) for r in q):.6g}M")
    lines += ['', 'No exact absorbed-horizon-flux identity is claimed because the source-native inputs do not provide a common balance-law binding in this audit.']
    (OUT/'SXS10_HORIZON_FLUX_TIMESERIES_CORRELATION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__':main()
