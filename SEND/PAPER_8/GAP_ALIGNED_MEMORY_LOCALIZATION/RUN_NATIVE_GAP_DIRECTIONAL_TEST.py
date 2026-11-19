#!/usr/bin/env python3
import pandas as pd,numpy as np,json,hashlib
from scipy.stats import spearmanr
from pathlib import Path
O=Path(__file__).resolve().parent
r=pd.read_csv(O/'GAP_ALIGNED_R40_MEMORY_ROWS.csv')
g0=pd.read_csv(r'E:\RIUD_ACTIVE_20260808\RIUD_GAP_T0_PROVENANCE_AND_MERGER_REFERENCE_AUDIT_R1_20260821\FROZEN_GAP_NATIVE_TIME_TABLE.csv')[['EVENT_ID','GLOBAL_SHIFT']]
r=r.merge(g0,left_on='EVENT',right_on='EVENT_ID',how='left').dropna(subset=['GAP_CENTER_NATIVE_TAU','GLOBAL_SCALE','GLOBAL_SHIFT'])
r['SOURCE_NATIVE_TAU']=r['U_SOURCE']*r['GLOBAL_SCALE']+r['GLOBAL_SHIFT']
r['RELATIVE_TO_GAP_NATIVE']=r['SOURCE_NATIVE_TAU']-r['GAP_CENTER_NATIVE_TAU']
obs=float(spearmanr(r.RELATIVE_TO_GAP_NATIVE,r.MEMORY_MAGNITUDE).statistic)
g=r[['EVENT','GAP_CENTER_NATIVE_TAU']].drop_duplicates(); by=dict(zip(g.EVENT,g.GAP_CENTER_NATIVE_TAU)); ev=r.EVENT.unique(); rng=np.random.default_rng(20260829); null=[]
for _ in range(999):
 perm=rng.permutation(ev); gp=dict(zip(ev,[by[x] for x in perm])); q=r.copy(); q['x']=q.SOURCE_NATIVE_TAU-q.EVENT.map(gp); null.append(float(spearmanr(q.x,q.MEMORY_MAGNITUDE).statistic))
null=np.asarray(null); p=float((1+(null>=obs).sum())/(len(null)+1))
r.to_csv(O/'GAP_ALIGNED_R40_MEMORY_ROWS_NATIVE.csv',index=False)
s={'N_ROWS':len(r),'OBSERVED_SPEARMAN':obs,'NULL_MEAN':float(null.mean()),'NULL_95':float(np.quantile(null,.95)),'PERMUTATION_P_GREATER_EQUAL':p,'SEED':20260829,'COORDINATE':'U_SOURCE*GLOBAL_SCALE+GLOBAL_SHIFT-GAP_CENTER_NATIVE_TAU','STATUS':'CORRECTED_NATIVE_DIRECTIONAL_TEST','NO_REFIT':True,'HOLDOUT30_ACCESSED':False}
(O/'NATIVE_GAP_MEMORY_DIRECTIONAL_TEST.json').write_text(json.dumps(s,indent=2),encoding='utf-8')
with (O/'SHA256_MANIFEST.txt').open('w',encoding='utf-8') as f:
 for x in sorted(O.iterdir()):
  if x.name!='SHA256_MANIFEST.txt':f.write(f'{hashlib.sha256(x.read_bytes()).hexdigest()}  {x.name}\n')
print(json.dumps(s,indent=2))
