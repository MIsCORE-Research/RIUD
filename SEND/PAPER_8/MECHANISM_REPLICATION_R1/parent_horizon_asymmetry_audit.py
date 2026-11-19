import csv
from pathlib import Path
import numpy as np, h5py

BASE=Path(r'E:/RIUD_ACTIVE_20260808/MIsCORE_RIUD_AUXILIARY_HORIZONDUMP_MECHANISM_TEST_R0_20260827')
OUT=Path(__file__).resolve().parent
VARS=['SpinFunction','WeylE_NN','WeylB_NN','DimlessRicciScalar']
def td(f,base):
    idx=np.asarray(f[base+'/index.dat'][:],float); dat=np.asarray(f[base+'/data.dat'][:],float).ravel(); out=[]
    for q in idx:
        end=int(q[1]); n=int(q[2]*q[3]); x=dat[end-n:end]; out.append((q[0],np.mean(x),np.sqrt(np.mean(x*x))))
    return np.asarray(out,float)
def main():
    rows=[]
    for ev in ['0319','0323']:
        with h5py.File(BASE/ev/'HorizonsDump.h5','r') as f:
            d={(ah,v):td(f,f'{ah}.dir/{v}.tdm') for ah in ['AhA','AhB','AhC'] for v in VARS}
        t0=d[('AhC','SpinFunction')][0,0]
        for v in VARS:
            a,b,c=d[('AhA',v)],d[('AhB',v)],d[('AhC',v)]
            lo=max(a[:,0].min(),b[:,0].min(),c[:,0].min(),t0); hi=min(a[:,0].max(),b[:,0].max(),c[:,0].max(),t0+50)
            grid=np.unique(np.concatenate([a[:,0],b[:,0],c[:,0]])); grid=grid[(grid>=lo)&(grid<hi)]
            ai=np.interp(grid,a[:,0],a[:,1]); bi=np.interp(grid,b[:,0],b[:,1]); ci=np.interp(grid,c[:,0],c[:,1]); cr=np.interp(grid,c[:,0],c[:,2])
            for w,wl,wh in [('PRE_50_25M',-50,-25),('PRE_25_0M',-25,0),('POST_0_5M',0,5)]:
                ok=(grid-t0>=wl)&(grid-t0<wh)
                rows.append({'EVENT':ev,'VARIABLE':v,'WINDOW':w,'N':int(ok.sum()),'MEAN_ABS_PARENT_MEAN_DIFF':float(np.mean(np.abs(ai[ok]-bi[ok]))) if ok.any() else '','RMS_PARENT_MEAN_DIFF':float(np.sqrt(np.mean((ai[ok]-bi[ok])**2))) if ok.any() else '','MEAN_AH_C_RMS':float(np.mean(cr[ok])) if ok.any() else ''})
    with open(OUT/'PARENT_HORIZON_ASYMMETRY.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    comp=[]
    for ev in ['0319','0323']:
        for v in VARS:
            q={x['WINDOW']:x for x in rows if x['EVENT']==ev and x['VARIABLE']==v}
            ok=all(q[w]['MEAN_ABS_PARENT_MEAN_DIFF']!='' for w in ['PRE_50_25M','PRE_25_0M'])
            comp.append({'EVENT':ev,'VARIABLE':v,'PARENT_ABS_DIFF_PRE_50_25M':q['PRE_50_25M']['MEAN_ABS_PARENT_MEAN_DIFF'],'PARENT_ABS_DIFF_PRE_25_0M':q['PRE_25_0M']['MEAN_ABS_PARENT_MEAN_DIFF'],'PARENT_ABS_DIFF_CHANGE_TOWARD_AHC':float(q['PRE_25_0M']['MEAN_ABS_PARENT_MEAN_DIFF'])-float(q['PRE_50_25M']['MEAN_ABS_PARENT_MEAN_DIFF']) if ok else '','PARENT_RMS_DIFF_CHANGE_TOWARD_AHC':float(q['PRE_25_0M']['RMS_PARENT_MEAN_DIFF'])-float(q['PRE_50_25M']['RMS_PARENT_MEAN_DIFF']) if ok else '','AHC_RMS_POST_0_5M':q['POST_0_5M']['MEAN_AH_C_RMS'],'COMPARISON_STATUS':'PASS_PRE_COMMON_SUPPORT' if ok else 'NO_COMMON_PRE_SUPPORT'})
    with open(OUT/'PARENT_ASYMMETRY_COMPONENT_COMPARISON.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(comp[0]));w.writeheader();w.writerows(comp)
    (OUT/'PARENT_HORIZON_ASYMMETRY.md').write_text('# Parent-horizon asymmetry audit\n\nAhA and AhB were interpolated on their common native-time support. Fixed pre-formation windows (−50 to −25M and −25 to 0M) were compared, plus AhC 0–5M. This is descriptive source-native evidence only.\n\n'+ '\n'.join(f"- {x['EVENT']} {x['VARIABLE']}: status={x['COMPARISON_STATUS']}; parent |mean A-B| [-50,-25]={x['PARENT_ABS_DIFF_PRE_50_25M']}; [-25,0]={x['PARENT_ABS_DIFF_PRE_25_0M']}; change toward AhC={x['PARENT_ABS_DIFF_CHANGE_TOWARD_AHC']}; AhC post RMS={x['AHC_RMS_POST_0_5M']}" for x in comp)+'\n\nA common increase in parent asymmetry toward AhC would be consistent with inherited asymmetry, but does not establish causality or explain the R40 memory law.\n',encoding='utf-8')
if __name__=='__main__':main()
