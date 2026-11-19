import csv, numpy as np, h5py
from pathlib import Path
BASE=Path(r'E:/RIUD_ACTIVE_20260808/MIsCORE_RIUD_AUXILIARY_HORIZONDUMP_MECHANISM_TEST_R0_20260827')
OUT=Path(__file__).resolve().parent
def td(f,base):
    idx=np.asarray(f[base+'/index.dat'][:],float); dat=np.asarray(f[base+'/data.dat'][:],float).ravel(); out=[]
    for q in idx:
        end=int(q[1]); n=int(q[2]*q[3]); out.append((q[0],dat[end-n:end]))
    return out
def main():
    rows=[]
    for ev in ['0319','0323','0320']:
        with h5py.File(BASE/ev/'HorizonsDump.h5','r') as f:
            e=dict(td(f,'AhC.dir/WeylE_NN.tdm')); b=dict(td(f,'AhC.dir/WeylB_NN.tdm')); t0=float(td(f,'AhC.dir/SpinFunction.tdm')[0][0])
        for t in sorted(set(e)&set(b)):
            x=e[t]; y=b[t]
            if x.size!=y.size: continue
            rows.append({'EVENT':ev,'TAU_FROM_AHC':t-t0,'E_RMS':float(np.sqrt(np.mean(x*x))),'B_RMS':float(np.sqrt(np.mean(y*y))),'EB_ENERGY_PROXY':float(np.mean(x*x+y*y)),'E2_MINUS_B2_PROXY':float(np.mean(x*x-y*y)),'EB_CROSS_PROXY':float(np.mean(x*y)),'E_ABS_MEAN':float(abs(np.mean(x))),'B_ABS_MEAN':float(abs(np.mean(y)))})
    with open(OUT/'WEYL_E_B_COUPLING_TIMESERIES.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    sm=[]
    for ev in ['0319','0323','0320']:
        for win,lo,hi in [('EARLY_0_5M',0,5),('LATE_25_50M',25,50)]:
            q=[r for r in rows if r['EVENT']==ev and lo<=r['TAU_FROM_AHC']<hi]
            sm.append({'EVENT':ev,'WINDOW':win,'N':len(q),'MEAN_EB_ENERGY_PROXY':float(np.mean([r['EB_ENERGY_PROXY'] for r in q])),'MEAN_E2_MINUS_B2_PROXY':float(np.mean([r['E2_MINUS_B2_PROXY'] for r in q])),'MEAN_EB_CROSS_PROXY':float(np.mean([r['EB_CROSS_PROXY'] for r in q])),'MEAN_E_RMS':float(np.mean([r['E_RMS'] for r in q])),'MEAN_B_RMS':float(np.mean([r['B_RMS'] for r in q]))})
    with open(OUT/'WEYL_E_B_COUPLING_WINDOW_SUMMARY.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(sm[0]));w.writeheader();w.writerows(sm)
    comp=[]
    for ev in ['0319','0323','0320']:
        e=next(x for x in sm if x['EVENT']==ev and x['WINDOW']=='EARLY_0_5M'); l=next(x for x in sm if x['EVENT']==ev and x['WINDOW']=='LATE_25_50M')
        comp.append({'EVENT':ev,'DELTA_EB_ENERGY_PROXY':e['MEAN_EB_ENERGY_PROXY']-l['MEAN_EB_ENERGY_PROXY'],'DELTA_E2_MINUS_B2_PROXY':e['MEAN_E2_MINUS_B2_PROXY']-l['MEAN_E2_MINUS_B2_PROXY'],'DELTA_EB_CROSS_PROXY':e['MEAN_EB_CROSS_PROXY']-l['MEAN_EB_CROSS_PROXY'],'DELTA_E_RMS':e['MEAN_E_RMS']-l['MEAN_E_RMS'],'DELTA_B_RMS':e['MEAN_B_RMS']-l['MEAN_B_RMS']})
    with open(OUT/'WEYL_E_B_COUPLING_COMPONENT_COMPARISON.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(comp[0]));w.writeheader();w.writerows(comp)
    (OUT/'WEYL_E_B_COUPLING_AUDIT.md').write_text('# Weyl E/B coupling proxy audit\n\nFor AhC, the raw angular `WeylE_NN` and `WeylB_NN` arrays were paired at identical native times. Fixed early (0–5M) and late (25–50M) windows were compared. The combinations are diagnostic proxies, not curvature invariants or fitted laws.\n\n'+ '\n'.join(f"- {x['EVENT']}: Δ(E²+B²)={x['DELTA_EB_ENERGY_PROXY']:.9g}; Δ(E²−B²)={x['DELTA_E2_MINUS_B2_PROXY']:.9g}; Δ(E·B)={x['DELTA_EB_CROSS_PROXY']:.9g}; ΔE_RMS={x['DELTA_E_RMS']:.9g}; ΔB_RMS={x['DELTA_B_RMS']:.9g}" for x in comp)+'\n\nA consistent positive Δ(E²+B²) and Δ(E²−B²) indicates an early electric-dominated curvature transient in this NN projection. It does not establish a microscopic mechanism or causal relation to the RIUD S law.\n',encoding='utf-8')
if __name__=='__main__':main()
