import csv
from pathlib import Path
import numpy as np, qnm, sxs

ARCH=Path(__file__).resolve().parent.parent / "R8_PHYSICAL_MECHANISM_CLOSURE" / "R8_EXTERNAL_NR_SOURCE_ARCHIVE"
R8=Path(__file__).resolve().parent.parent / "R8_PHYSICAL_MECHANISM_CLOSURE" / "R8_DERIVED_SOURCE_NATIVE"
OUT=Path(__file__).resolve().parent
EVENTS=['0180','0513','0526','1144','1765','2092','2497','2499','2505','2506']

def main():
    with open(R8/'R8_NR_SOURCE_NATIVE_SUMMARY.csv',encoding='utf-8-sig',newline='') as f: meta={r['EVENT'].split(':')[-1]:r for r in csv.DictReader(f)}
    rows=[]
    for ev in EVENTS:
        x=sxs.load(str(ARCH/ev/'Strain_N2.h5'))
        t=np.asarray(x.t,float); ch=float(meta[ev]['COMMON_HORIZON_TIME']); tau=t-ch
        for mode,l,mm,h in [('h22',2,2,np.asarray(x[:,x.index(2,2)],complex)),('h44',4,4,np.asarray(x[:,x.index(4,4)],complex))]:
            ph=np.unwrap(np.angle(h)); freq=np.abs(np.gradient(ph,t)); chi=float(meta[ev]['AHC_CHI_FINAL']); mf=float(meta[ev]['AHC_CHRISTODOULOU_MASS_FINAL']); om=qnm.modes_cache(s=-2,l=l,m=mm,n=0)(chi)[0]; qfreq=abs(float(om.real))/mf
            for win,lo,hi in [('10_20M',10,20),('20_40M',20,40),('40_80M',40,80)]:
                ok=(tau>=lo)&(tau<hi)&np.isfinite(freq)
                rows.append({'EVENT':ev,'MODE':f'({l},{mm},0)','WINDOW':'AHC_'+win,'N':int(ok.sum()),'MEDIAN_FREQ_INITIAL_M':float(np.median(freq[ok])) if ok.any() else '','QNM_REAL_FREQ_INITIAL_M':qfreq,'MEDIAN_MINUS_QNM':float(np.median(freq[ok])-qfreq) if ok.any() else '','STATUS':'PASS' if ok.sum()>=3 else 'INSUFFICIENT_ROWS'})
    with (OUT/'SXS10_QNM_FREQUENCY_EXTENSION.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    lines=['# SXS10 source-native QNM frequency extension','','Corrected audit: reads original `Strain_N2.h5` directly, not downsampled summary history. Fixed AhC-relative windows 10–20M, 20–40M, and 40–80M. Frequency is from unwrapped native phase; QNM frequency uses qnm 0.4.4 with preserved final spin and mass ratio. No fit or timing adjustment.']
    for mode in ['(2,2,0)','(4,4,0)']:
        for win in ['AHC_10_20M','AHC_20_40M','AHC_40_80M']:
            q=[r for r in rows if r['MODE']==mode and r['WINDOW']==win and r['STATUS']=='PASS']
            lines.append(f"- {mode} {win}: {len(q)}/10 scorable; median frequency-minus-QNM={np.median([float(r['MEDIAN_MINUS_QNM']) for r in q]):.8g} M^-1" if q else f'- {mode} {win}: no window with >=3 rows')
    lines += ['', 'Ringdown consistency only; not a microscopic RIUD mechanism identification.']
    (OUT/'SXS10_QNM_FREQUENCY_EXTENSION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__': main()
