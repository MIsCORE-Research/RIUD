import csv, numpy as np
from pathlib import Path
import h5py
BASE=Path(r'E:/RIUD_ACTIVE_20260808/MIsCORE_RIUD_AUXILIARY_HORIZONDUMP_MECHANISM_TEST_R0_20260827')
OUT=Path(__file__).resolve().parent
V=['SpinFunction','WeylE_NN','WeylB_NN','DimlessRicciScalar']
def td(f,b):
 idx=np.asarray(f[b+'/index.dat'][:],float); dat=np.asarray(f[b+'/data.dat'][:],float).ravel(); a=[]
 for q in idx:
  en=int(q[1]); n=int(q[2]*q[3]); x=dat[en-n:en]; a.append((q[0],np.sqrt(np.mean(x*x))))
 return np.asarray(a)
def cc(a,b):
 a=a-a.mean(); b=b-b.mean(); return float(np.dot(a,b)/np.sqrt(np.dot(a,a)*np.dot(b,b)))
def main():
 out=[]; lagrows=[]
 for ev in ['0319','0323','0320']:
  with h5py.File(BASE/ev/'HorizonsDump.h5','r') as f: d={v:td(f,'AhC.dir/'+v+'.tdm') for v in V}; t0=d['SpinFunction'][0,0]
  lo=max(x[:,0].min() for x in d.values()); hi=min(x[:,0].max() for x in d.values()); grid=np.arange(max(t0,lo),min(t0+80,hi),0.5)
  y={v:np.interp(grid,d[v][:,0],d[v][:,1]) for v in V}
  for i,a in enumerate(V):
   for b in V[i+1:]:
    out.append({'EVENT':ev,'WINDOW':'0_80M','VAR_A':a,'VAR_B':b,'ZERO_LAG_CORR':cc(y[a],y[b]),'N':len(grid)})
    for lag in range(-20,21):
     # positive lag: A(t) against B(t+lag)
     if lag>=0: x=y[a][:-lag or None]; z=y[b][lag:]
     else: x=y[a][-lag:]; z=y[b][:lag or None]
     lagrows.append({'EVENT':ev,'VAR_A':a,'VAR_B':b,'LAG_M':lag,'CORR':cc(x,z),'WINDOW':'0_80M'})
 with open(OUT/'SURFACE_ZERO_LAG_CORRELATIONS.csv','w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
 with open(OUT/'SURFACE_LAG_CORRELATIONS.csv','w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(lagrows[0]));w.writeheader();w.writerows(lagrows)
 summ=[]
 for ev in ['0319','0323','0320']:
  for a in V:
   for b in V:
    if V.index(a)>=V.index(b): continue
    q=[x for x in lagrows if x['EVENT']==ev and x['VAR_A']==a and x['VAR_B']==b]; m=max(q,key=lambda x:abs(float(x['CORR'])))
    summ.append({'EVENT':ev,'VAR_A':a,'VAR_B':b,'ZERO_LAG_CORR':next(x['ZERO_LAG_CORR'] for x in out if x['EVENT']==ev and x['VAR_A']==a and x['VAR_B']==b),'MAX_ABS_CORR_FIXED_LAG':m['CORR'],'LAG_AT_MAX_ABS_CORR_M':m['LAG_M']})
 with open(OUT/'SURFACE_LAG_SUMMARY.csv','w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(summ[0]));w.writeheader();w.writerows(summ)
 (OUT/'SURFACE_CROSS_CORRELATION_AUDIT.md').write_text('# Surface-field cross-correlation audit\n\nAhC angular RMS series were interpolated onto a fixed 0.5M grid from AhC to 80M. Zero-lag correlations and a predeclared lag scan from −20M to +20M are reported. The lag scan is descriptive; no maximum-lag law is fitted.\n\n'+ '\n'.join(f"- {x['EVENT']} {x['VAR_A']} vs {x['VAR_B']}: zero-lag={float(x['ZERO_LAG_CORR']):.6g}; max-|r|={float(x['MAX_ABS_CORR_FIXED_LAG']):.6g} at lag={x['LAG_AT_MAX_ABS_CORR_M']}M" for x in summ)+'\n',encoding='utf-8')
if __name__=='__main__':main()
