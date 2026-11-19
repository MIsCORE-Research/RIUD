#!/usr/bin/env python3
import pandas as pd, numpy as np, json, hashlib
from scipy.stats import spearmanr
from pathlib import Path
OUT=Path(__file__).resolve().parent
r=pd.read_csv(OUT/'GAP_ALIGNED_R40_MEMORY_ROWS.csv').dropna(subset=['RELATIVE_TO_GAP_LATENT','MEMORY_MAGNITUDE'])
obs=float(spearmanr(r.RELATIVE_TO_GAP_LATENT,r.MEMORY_MAGNITUDE).statistic)
rng=np.random.default_rng(20260829); gaps=r[['EVENT','GAP_CENTER_LATENT']].drop_duplicates(); by=dict(zip(gaps.EVENT,gaps.GAP_CENTER_LATENT)); ev=r.EVENT.unique(); null=[]
for _ in range(999):
 perm=rng.permutation(ev); mp=dict(zip(ev,perm)); gp={e:by[mp[e]] for e in ev}; rr=r.copy(); rr['x']=rr['U_SOURCE']-rr['EVENT'].map(gp); null.append(float(spearmanr(rr.x,rr.MEMORY_MAGNITUDE).statistic))
null=np.array(null); p=float((1+np.sum(null>=obs))/(len(null)+1))
pd.DataFrame({'METRIC':['ROW_SPEARMAN_RELATIVE_GAP_VS_MEMORY','NULL_999'],'VALUE':[obs,float(null.mean())]}).to_csv(OUT/'GAP_MEMORY_DIRECTIONAL_TEST.csv',index=False)
s={'OBSERVED_SPEARMAN':obs,'NULL_MEAN':float(null.mean()),'NULL_95':float(np.quantile(null,.95)),'PERMUTATION_P_GREATER_EQUAL':p,'N_ROWS':len(r),'SEED':20260829,'STATUS':'DIRECTIONAL_DESCRIPTIVE_TEST','NO_REFIT':True,'HOLDOUT30_ACCESSED':False}
(OUT/'GAP_MEMORY_DIRECTIONAL_TEST.json').write_text(json.dumps(s,indent=2),encoding='utf-8')
with (OUT/'SHA256_MANIFEST.txt').open('w',encoding='utf-8') as f:
 for q in sorted(OUT.iterdir()):
  if q.name!='SHA256_MANIFEST.txt':f.write(f'{hashlib.sha256(q.read_bytes()).hexdigest()}  {q.name}\n')
print(json.dumps(s,indent=2))
