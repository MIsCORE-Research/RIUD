#!/usr/bin/env python3
import pandas as pd, json, hashlib
from pathlib import Path
OUT=Path(__file__).resolve().parent; OUT.mkdir(parents=True,exist_ok=True)
gap=pd.read_csv(r'E:\RIUD_ACTIVE_20260808\RIUD_GAP_T0_PROVENANCE_AND_MERGER_REFERENCE_AUDIT_R1_20260821\FROZEN_GAP_NATIVE_TIME_TABLE.csv')
r40=pd.read_csv(r'E:\RIUD_ACTIVE_20260808\MIsCORE_R40_BLIND_ROW_IDENTITY_R2_20260827\CANONICAL_R40_EVENT_LEVEL_HAZARD.csv')
join=r40.merge(gap[['EVENT_ID','GAP_CENTER_LATENT','GAP_CENTER_NATIVE_TAU','GLOBAL_SCALE','MAPPING_STATUS']],left_on='EVENT',right_on='EVENT_ID',how='left')
join['RELATIVE_TO_GAP_LATENT']=join['U_SOURCE']-join['GAP_CENTER_LATENT']
join['MEMORY_MAGNITUDE']=join['MEMORY_DELTA_R40_P1'].abs()+join['MEMORY_DELTA_R39_P0'].abs()
join.to_csv(OUT/'GAP_ALIGNED_R40_MEMORY_ROWS.csv',index=False)
valid=join.dropna(subset=['GAP_CENTER_LATENT'])
q=valid.groupby('BIN_INDEX').agg(N=('EVENT','size'),MEDIAN_REL_GAP=('RELATIVE_TO_GAP_LATENT','median'),MEDIAN_MEMORY=('MEMORY_MAGNITUDE','median'),MEAN_MEMORY=('MEMORY_MAGNITUDE','mean')).reset_index()
q.to_csv(OUT/'GAP_ALIGNED_MEMORY_BY_BIN.csv',index=False)
top=valid.nlargest(100,'MEMORY_MAGNITUDE')[['EVENT','BIN_INDEX','U_SOURCE','GAP_CENTER_LATENT','RELATIVE_TO_GAP_LATENT','RUN_BUCKET','AGE_CLASS','MEMORY_MAGNITUDE']]
top.to_csv(OUT/'TOP_GAP_ALIGNED_MEMORY_ROWS.csv',index=False)
s={'R40_ROWS':len(r40),'GAP_ROWS':len(gap),'COMMON_EVENTS':int(valid['EVENT'].nunique()),'UNBOUND_EVENTS':sorted(set(r40.EVENT)-set(gap.EVENT_ID)),'MAPPING_STATUS_COUNTS':gap.MAPPING_STATUS.value_counts().to_dict(),'GAP_ALIGNED_COORDINATE':'U_SOURCE - GAP_CENTER_LATENT','STATUS':'DESCRIPTIVE_GAP_MEMORY_LOCALIZATION','HOLDOUT30_ACCESSED':False,'REFIT':False}
(OUT/'SUMMARY.json').write_text(json.dumps(s,indent=2),encoding='utf-8')
(OUT/'REPORT.md').write_text('# GAP-aligned memory localization\n\nDescriptive join of frozen R40 rows to frozen GAP table; no refit or redefinition.\n\n'+json.dumps(s,indent=2),encoding='utf-8')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
with (OUT/'SHA256_MANIFEST.txt').open('w',encoding='utf-8') as f:
 for p in sorted(OUT.iterdir()):
  if p.name!='SHA256_MANIFEST.txt':f.write(f'{h(p)}  {p.name}\n')
print(json.dumps(s,indent=2))
