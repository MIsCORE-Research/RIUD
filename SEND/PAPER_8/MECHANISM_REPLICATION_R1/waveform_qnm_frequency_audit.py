import csv, json, numpy as np, qnm
from pathlib import Path
P=Path(r'E:/RIUD_ACTIVE_20260808/MIsCORE_RIUD_AUXILIARY_HORIZONDUMP_MECHANISM_TEST_R0_20260827')
OUT=Path(__file__).resolve().parent
def main():
    rows=[]
    for ev in ['0319','0323','0320']:
        import h5py
        with h5py.File(P/ev/'HorizonsDump.h5','r') as f:
            idx=np.asarray(f['AhC.dir/SpinFunction.tdm/index.dat'][:],float); t0=float(idx[0,0])
        meta=json.loads((P/ev/'metadata.json').read_text()); af=float(meta['remnant_dimensionless_spin'][2]); mf=float(meta['remnant_mass'])
        for l,m,key in [(2,2,'Extrapolated_N2.dir/Y_l2_m2.dat'),(4,4,'Extrapolated_N2.dir/Y_l4_m4.dat')]:
            import h5py
            with h5py.File(P/ev/'rMPsi4_Asymptotic_GeometricUnits.h5','r') as f: x=np.asarray(f[key][:],float)
            phase=np.unwrap(np.arctan2(x[:,2],x[:,1])); freq=np.abs(np.gradient(phase,x[:,0])); amp=np.hypot(x[:,1],x[:,2]); qw=qnm.modes_cache(s=-2,l=l,m=m,n=0)(af)[0]; qfreq=abs(float(qw.real))/mf
            for name,lo,hi in [('AHC_10_20M',10,20),('AHC_20_40M',20,40),('AHC_40_80M',40,80)]:
                ok=(x[:,0]-t0>=lo)&(x[:,0]-t0<hi)&np.isfinite(freq)
                if ok.any(): rows.append({'EVENT':ev,'MODE':f'({l},{m},0)','WINDOW':name,'N':int(ok.sum()),'MEDIAN_ABS_ANGULAR_FREQ_INITIAL_M':float(np.median(freq[ok])),'QNM_REAL_FREQ_INITIAL_M':qfreq,'MEDIAN_MINUS_QNM':float(np.median(freq[ok])-qfreq),'MEDIAN_AMPLITUDE':float(np.median(amp[ok]))})
    with open(OUT/'WAVEFORM_QNM_FREQUENCY_AUDIT.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (OUT/'WAVEFORM_QNM_FREQUENCY_AUDIT.md').write_text('# Source-native waveform frequency versus Kerr QNM\n\nInstantaneous absolute angular frequency was calculated from the unwrapped phase in fixed AhC-relative windows. The Kerr QNM real frequency uses source-native final spin and remnant mass; no fit or offset was introduced.\n\nThe comparison is a ringdown consistency check only. It does not identify the earlier surface transient as QNM excitation or establish the RIUD memory mechanism.\n',encoding='utf-8')
if __name__=='__main__':main()
