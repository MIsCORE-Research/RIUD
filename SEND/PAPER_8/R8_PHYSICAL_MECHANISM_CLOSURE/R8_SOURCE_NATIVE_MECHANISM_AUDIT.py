import csv, json, hashlib, math
from pathlib import Path
import numpy as np
import h5py, sxs
from sxs.waveforms import energy_flux, angular_momentum_flux

ROOT=Path(__file__).resolve().parent
ARCH=ROOT/'R8_EXTERNAL_NR_SOURCE_ARCHIVE'; OUT=ROOT/'R8_DERIVED_SOURCE_NATIVE'; OUT.mkdir(exist_ok=True)
IDS=['0180','0513','0526','1144','1765','2092','2497','2499','2505','2506']

def interp(a,t,x):
    if len(a)==0:return float('nan')
    return float(np.interp(t,a[:,0],a[:,1]))
def safe_corr(a,b):
    m=np.isfinite(a)&np.isfinite(b)
    return float(np.corrcoef(a[m],b[m])[0,1]) if m.sum()>2 and np.std(a[m])>0 and np.std(b[m])>0 else float('nan')
def q90(x):
    x=np.asarray(x); x=x[np.isfinite(x)]
    return float(np.quantile(x,.9)) if len(x) else float('nan')

def main():
    rows=[]; mode_rows=[]; horizon_rows=[]; inv=[]
    for ix,sid in enumerate(IDS,1):
        print(f'GLOBAL_PROGRESS={ix}/{len(IDS)} CURRENT_SIMULATION={sid} CURRENT_MECHANISM=SOURCE_NATIVE_EXTRACTION',flush=True)
        edir=ARCH/sid
        meta=json.load(open(edir/'metadata.json',encoding='utf-8'))
        ch=float(meta.get('common_horizon_time',float('nan')))
        lev=next(edir.glob('Strain_N2.h5'),None)
        x=sxs.load(str(lev)); t=np.asarray(x.t,float); h22=np.asarray(x[:,x.index(2,2)],complex); h44=np.asarray(x[:,x.index(4,4)],complex)
        tau=t-ch
        m=(tau>=0)&(tau<=min(250.0,float(tau.max())))
        # source-native phase/frequency, no smoothing or fit
        ph22=np.unwrap(np.angle(h22)); ph44=np.unwrap(np.angle(h44))
        f22=np.gradient(ph22,t)/(2*np.pi); f44=np.gradient(ph44,t)/(2*np.pi)
        pos=m&(f22>0)&(f44>0)&np.isfinite(f22)&np.isfinite(f44)
        ratio=f44[pos]/(2*f22[pos]) if pos.any() else np.array([])
        phase_res=np.angle(np.exp(1j*(ph44[pos]-2*ph22[pos]))) if pos.any() else np.array([])
        amp22=np.abs(h22); amp44=np.abs(h44)
        amp_m=m&(amp22>0)&(amp44>0)
        log_quad=safe_corr(np.log(amp22[amp_m]),np.log(amp44[amp_m]))
        # AhC source-native horizon data
        with h5py.File(edir/'Horizons.h5','r') as hf:
            def get(name): return np.asarray(hf['AhC.dir/'+name][:],float)
            area=get('ArealMass.dat'); mass=get('ChristodoulouMass.dat'); spin=get('chiMagInertial.dat')
            spinvec=get('DimensionfulInertialSpin.dat'); center=get('CoordCenterInertial.dat')
        hm=(area[:,0]>=ch)
        a0=interp(area,ch,area[:,1]); ae=float(area[-1,1]); m0=interp(mass,ch,mass[:,1]); me=float(mass[-1,1]); s0=interp(spin,ch,spin[:,1]); se=float(spin[-1,1])
        post_area=area[hm,1]; post_mass=mass[hm,1]; post_spin=spin[hm,1]
        area_mono=float(np.mean(np.diff(post_area)>=-1e-10)) if len(post_area)>1 else float('nan')
        # late relaxation proxy: change in final 20% relative to full post-CH change
        k=max(2,int(.8*len(post_mass))); full=abs(me-m0); late=abs(me-post_mass[k]) if len(post_mass)>k else float('nan')
        relax_frac=float(late/full) if full>0 else float('nan')
        # derivative proxies (source-native only)
        dM=np.gradient(mass[:,1],mass[:,0]); dA=np.gradient(area[:,1],area[:,0])
        Jmag=np.linalg.norm(spinvec[:,1:4],axis=1); dJ=np.gradient(Jmag,spinvec[:,0]); dchi=np.gradient(spin[:,1],spin[:,0])
        post=mass[:,0]>=ch
        ef=np.asarray(energy_flux(x),float); jf=np.asarray(angular_momentum_flux(x),float); fm=x.t>=ch
        Epost=float(np.trapezoid(ef[fm],x.t[fm])) if fm.sum()>1 else float('nan')
        Jzpost=float(np.trapezoid(jf[fm,2],x.t[fm])) if fm.sum()>1 else float('nan')
        kt=max(1,int(.8*len(post_mass))); post_t=mass[hm,0]
        local_relax=float(abs(me-post_mass[kt])/abs(post_t[-1]-post_t[kt])) if len(post_t)>kt and abs(post_t[-1]-post_t[kt])>0 else float('nan')
        row={'EVENT':'SXS:BBH:'+sid,'LEVEL':meta.get('metadata_version',''),'COMMON_HORIZON_TIME':ch,
             'STRAIN_T_MIN':float(t[0]),'STRAIN_T_MAX':float(t[-1]),'TAU_POST_CH_MAX':float(tau.max()),
             'N_STRAIN_ROWS':len(t),'N_HORIZON_ROWS':len(area),'HORIZON_POST_ROWS':int(hm.sum()),
             'AHC_AREAL_MASS_AT_CH':a0,'AHC_AREAL_MASS_FINAL':ae,'AHC_AREAL_MASS_DELTA':ae-a0,
             'AHC_CHRISTODOULOU_MASS_AT_CH':m0,'AHC_CHRISTODOULOU_MASS_FINAL':me,'AHC_MASS_DELTA':me-m0,
             'AHC_CHI_AT_CH':s0,'AHC_CHI_FINAL':se,'AHC_CHI_DELTA':se-s0,
             'AHC_AREA_MONOTONIC_FRACTION':area_mono,'AHC_LATE_MASS_RELAXATION_FRACTION':relax_frac,
             'AHC_MAX_ABS_MASS_DOT':float(np.nanmax(np.abs(dM[post]))) if post.any() else float('nan'),
             'AHC_MAX_ABS_AREA_DOT':float(np.nanmax(np.abs(dA[post]))) if post.any() else float('nan'),
             'AHC_JMAG_AT_CH':interp(spinvec,ch,Jmag),'AHC_JMAG_FINAL':float(Jmag[-1]),'AHC_JMAG_DELTA':float(Jmag[-1]-interp(spinvec,ch,Jmag)),
             'AHC_MAX_ABS_JMAG_DOT':float(np.nanmax(np.abs(dJ[spinvec[:,0]>=ch]))) if np.any(spinvec[:,0]>=ch) else float('nan'),
             'AHC_MAX_ABS_CHI_DOT':float(np.nanmax(np.abs(dchi[spin[:,0]>=ch]))) if np.any(spin[:,0]>=ch) else float('nan'),
             'AHC_CENTER_DISPLACEMENT_POST':float(np.linalg.norm(center[-1,1:4]-np.asarray([np.interp(ch,center[:,0],center[:,j]) for j in range(1,4)]))),
             'INFINITY_ENERGY_FLUX_POST':Epost,'INFINITY_JZ_FLUX_POST':Jzpost,'LOCAL_RELAXATION_TIMESCALE_PROXY':local_relax,
             'H22_H44_FREQ_RATIO_MEDIAN':float(np.median(ratio)) if len(ratio) else float('nan'),
             'H22_H44_FREQ_RATIO_ABS_DEV_MEDIAN':float(np.median(np.abs(ratio-1))) if len(ratio) else float('nan'),
             'H22_H44_PHASE_RESIDUAL_CIRCULAR_MEDIAN':float(np.median(np.abs(phase_res))) if len(phase_res) else float('nan'),
             'LOG_AMP_QUADRATIC_CORR':log_quad,'MODE_ROWS_TESTED':int(pos.sum()),
             'HORIZON_SOURCE_PRESENT':True,'FLUX_INFINITY_SOURCE_PRESENT':False,
             'DIRECT_SXS_R40_LIKELIHOOD':False}
        rows.append(row)
        for name,arr in [('h22',h22),('h44',h44)]:
            for j in np.linspace(0,len(t)-1,min(200,len(t)),dtype=int):
                mode_rows.append({'EVENT':'SXS:BBH:'+sid,'T_NATIVE':float(t[j]),'TAU_FROM_COMMON_HORIZON':float(tau[j]),'MODE':name,'AMP':float(abs(arr[j])),'PHASE_UNWRAPPED':float(np.unwrap(np.angle(arr))[j])})
        for name,arr in [('ArealMass',area),('ChristodoulouMass',mass),('chiMagInertial',spin)]:
            for j in np.linspace(0,len(arr)-1,min(200,len(arr)),dtype=int): horizon_rows.append({'EVENT':'SXS:BBH:'+sid,'VARIABLE':name,'T_NATIVE':float(arr[j,0]),'TAU_FROM_COMMON_HORIZON':float(arr[j,0]-ch),'VALUE':float(arr[j,1])})
        inv.append({'EVENT':'SXS:BBH:'+sid,'WAVEFORM_FILE':'Strain_N2.h5','HORIZON_FILE':'Horizons.h5','MODES_PRESENT':'h22,h44','HORIZON_VARIABLES_PRESENT':'AhC ArealMass,ChristodoulouMass,chiMagInertial,CoordCenterInertial','FLUX_INFINITY_PRESENT':'FALSE','SOURCE_TIME':'native dimensionless SXS time','COMMON_HORIZON_TIME_FIELD':'metadata.json:common_horizon_time'})
    def write(name,rs):
        with open(OUT/name,'w',newline='',encoding='utf-8') as f:
            cols=sorted({k for r in rs for k in r}); w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rs)
    write('R8_NR_SOURCE_NATIVE_SUMMARY.csv',rows); write('R8_MODE_TIME_SERIES.csv',mode_rows); write('R8_HORIZON_TIME_SERIES.csv',horizon_rows); write('R8_SOURCE_NATIVE_VARIABLE_INVENTORY.csv',inv)
    json.dump({'cohort':IDS,'n_events':len(rows),'source_native_only':True,'no_R40_refit':True,'no_holdout30':True},open(OUT/'R8_DERIVED_METADATA.json','w',encoding='utf-8'),indent=2)
    print('R8_SOURCE_NATIVE_EXTRACTION=PASS')
    print('EVENTS_EXTRACTED='+str(len(rows)))

if __name__=='__main__':main()
