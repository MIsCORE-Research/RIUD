import csv, json, importlib.metadata
from pathlib import Path
import qnm

BASE=Path(r'E:/RIUD_ACTIVE_20260808/MIsCORE_RIUD_AUXILIARY_HORIZONDUMP_MECHANISM_TEST_R0_20260827')
OUT=Path(__file__).resolve().parent
def main():
    rows=[]
    for ev in ['0319','0323','0320']:
        m=json.loads((BASE/ev/'metadata.json').read_text())
        af=float(m['remnant_dimensionless_spin'][2]); mf=float(m['remnant_mass'])
        for l,mm in [(2,2),(4,4)]:
            w,_,_=qnm.modes_cache(s=-2,l=l,m=mm,n=0)(af)
            rows.append({'EVENT':ev,'MODE':f'({l},{mm},0)','CHI_F_Z':af,'REMNANT_M_OVER_M_INITIAL':mf,'OMEGA_REAL_MF':float(w.real),'OMEGA_IMAG_MF':float(w.imag),'DAMPING_TIME_OVER_MF':float(-1/w.imag),'OSCILLATION_PERIOD_OVER_MF':float(2*3.141592653589793/w.real),'DAMPING_TIME_OVER_INITIAL_M':float(mf*(-1/w.imag)),'QNM_LIBRARY':'qnm','QNM_VERSION':importlib.metadata.version('qnm')})
    with open(OUT/'QNM_SOURCE_NATIVE_RESULTS.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    # peak gaps from fixed previous temporal audit
    tr=[]; peak_rows=[]
    with open(OUT/'SURFACE_WAVEFORM_TEMPORAL_ORDER.csv',newline='',encoding='utf-8') as f: src=csv.DictReader(f); tr=list(src)
    for ev in ['0319','0323','0320']:
        h22=next(x for x in tr if x['EVENT']==ev and x['OBSERVABLE']=='h22');h44=next(x for x in tr if x['EVENT']==ev and x['OBSERVABLE']=='h44')
        q22=next(x for x in rows if x['EVENT']==ev and x['MODE']=='(2,2,0)'); q44=next(x for x in rows if x['EVENT']==ev and x['MODE']=='(4,4,0)')
        peak_rows.append({'EVENT':ev,'H22_PEAK_TAU':float(h22['PEAK_TAU_FROM_AHC']),'H44_PEAK_TAU':float(h44['PEAK_TAU_FROM_AHC']),'H44_MINUS_H22_PEAK':float(h44['PEAK_TAU_FROM_AHC'])-float(h22['PEAK_TAU_FROM_AHC']),'QNM_220_DAMPING_TIME_INITIAL_M':q22['DAMPING_TIME_OVER_INITIAL_M'],'QNM_440_DAMPING_TIME_INITIAL_M':q44['DAMPING_TIME_OVER_INITIAL_M'],'PEAK_GAP_OVER_QNM220_DAMPING':(float(h44['PEAK_TAU_FROM_AHC'])-float(h22['PEAK_TAU_FROM_AHC']))/float(q22['DAMPING_TIME_OVER_INITIAL_M'])})
    with open(OUT/'QNM_PEAK_INTERVAL_COMPARISON.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(peak_rows[0]));w.writeheader();w.writerows(peak_rows)
    (OUT/'QNM_SOURCE_NATIVE_AUDIT.md').write_text('# Source-native Kerr QNM audit\n\nThe installed `qnm` library was used with source-native remnant z-spin and remnant mass from metadata for SXS:BBH:0319, 0323, and 0320. No coefficient was fitted.\n\nThe observed h44-minus-h22 peak interval is 0.50–0.70M across the three events, while the `(2,2,0)` damping scale in initial-M units is approximately 11.74M. Therefore the peak interval is not itself a damping-time measurement; it is much shorter than one QNM damping time.\n\nThis is a consistency calculation only and does not identify the surface transient with a QNM or explain the RIUD memory law.\n',encoding='utf-8')
if __name__=='__main__':main()
