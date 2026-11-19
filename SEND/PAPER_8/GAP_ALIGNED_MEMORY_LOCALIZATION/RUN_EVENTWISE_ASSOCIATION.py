#!/usr/bin/env python3
import pandas as pd, numpy as np, json, hashlib
from scipy.stats import spearmanr, kendalltau
from pathlib import Path
OUT=Path(__file__).resolve().parent
r=pd.read_csv(OUT/'GAP_ALIGNED_R40_MEMORY_ROWS.csv')
g=pd.read_csv(r'E:\RIUD_ACTIVE_20260808\MIsCORE_RAW_GAP_WINDOW_PROJECTION_CORRECTED_R1_20260829\EVENT_GAP_SUMMARIES_CORRECTED.csv')
r['w']=r['MEMORY_MAGNITUDE'].clip(lower=0)
def agg(x):
 w=x.w.to_numpy(); rel=x.RELATIVE_TO_GAP_LATENT.to_numpy()
 return pd.Series({'MEMORY_TOTAL':x.MEMORY_MAGNITUDE.sum(),'MEMORY_MAX':x.MEMORY_MAGNITUDE.max(),'MEMORY_CENTROID_REL_GAP':float(np.sum(w*rel)/(np.sum(w)+1e-15)),'MEMORY_ONSET_REL_GAP':float(x.loc[x.MEMORY_MAGNITUDE>0,'RELATIVE_TO_GAP_LATENT'].min()) if (x.MEMORY_MAGNITUDE>0).any() else np.nan})
a=r.groupby('EVENT').apply(agg,include_groups=False).reset_index()
a=a.merge(g,left_on='EVENT',right_on='EVENT_ID',how='left')
out=[]
for v in ['MEMORY_TOTAL','MEMORY_MAX','MEMORY_CENTROID_REL_GAP','MEMORY_ONSET_REL_GAP']:
 z=a[[v,'MEAN_PRE_MINUS_POST']].dropna()
 sr=spearmanr(z[v],z.MEAN_PRE_MINUS_POST); kt=kendalltau(z[v],z.MEAN_PRE_MINUS_POST)
 out.append({'X':v,'N':len(z),'SPEARMAN_RHO':sr.statistic,'SPEARMAN_P':sr.pvalue,'KENDALL_TAU':kt.statistic,'KENDALL_P':kt.pvalue})
pd.DataFrame(out).to_csv(OUT/'EVENTWISE_GAP_MEMORY_ASSOCIATION.csv',index=False)
a.to_csv(OUT/'EVENTWISE_GAP_MEMORY_SUMMARY.csv',index=False)
s={'EVENTS':len(a),'ASSOCIATION_ROWS':len(out),'STATUS':'DESCRIPTIVE_ASSOCIATION_ONLY','NO_REFIT':True,'HOLDOUT30_ACCESSED':False}
(OUT/'EVENTWISE_ASSOCIATION_SUMMARY.json').write_text(json.dumps(s,indent=2),encoding='utf-8')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
with (OUT/'SHA256_MANIFEST.txt').open('w',encoding='utf-8') as f:
 for p in sorted(OUT.iterdir()):
  if p.name!='SHA256_MANIFEST.txt':f.write(f'{h(p)}  {p.name}\n')
print(pd.DataFrame(out).to_string(index=False)); print(json.dumps(s,indent=2))
