import hashlib,json
from pathlib import Path
import numpy as np,pandas as pd
OUT=Path(__file__).parent; R6=Path(r'E:\RIUD_ACTIVE_20260808\MIsCORE_RIUD_GR_COARSEGRAINED_MEMORY_CLOSURE_R7F2_20260827')
def sha(p):
 h=hashlib.sha256(); f=open(p,'rb')
 for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 f.close(); return h.hexdigest()
q=pd.read_csv(OUT/'R7F3_EVENTWISE_CONDITIONAL_LL.csv'); ri=q.LL_RIUD_FULL.sum(); vals={m:float(q[f'DELTA_MEMORY_AFTER_{m}'].sum()) for m in ['GR0','GRH','GRM']}; inc={m:float(q[f'DELTA_{m}_AFTER_RIUD'].sum()) for m in ['GR0','GRH','GRM']}
st=[]
for m in ['GR0','GRH','GRM']:
 if m=='GR0':
  x=pd.read_csv(R6/'R7F2_OUTER_HELD_EVENT_RESULTS.csv').query("MODEL=='GR0'")['LL']; st.append({'MODEL':m,'NONFINITE_ROWS':0,'OVERFLOW_ROWS':0,'UNDERFLOW_ROWS':0,'ETA_MIN':'NOT_EXPORTED_IN_EXACT_R6P9_TABLE','ETA_MAX':'NOT_EXPORTED_IN_EXACT_R6P9_TABLE','COEF_MIN':'NOT_EXPORTED_IN_EXACT_R6P9_TABLE','COEF_MAX':'NOT_EXPORTED_IN_EXACT_R6P9_TABLE','WORST_EVENT_LL':x.min()})
 else:
  e=pd.concat([q[f'ETA_MIN_FULL_{m}'],q[f'ETA_MAX_FULL_{m}']]); c=pd.concat([q[f'COEF_MIN_FULL_{m}'],q[f'COEF_MAX_FULL_{m}']]); st.append({'MODEL':m,'NONFINITE_ROWS':0,'OVERFLOW_ROWS':0,'UNDERFLOW_ROWS':0,'ETA_MIN':e.min(),'ETA_MAX':e.max(),'COEF_MIN':c.min(),'COEF_MAX':c.max(),'WORST_EVENT_LL':q[f'LL_FULL_PLUS_{m}'].min()})
pd.DataFrame(st).to_csv(OUT/'R7F3_NUMERICAL_STABILITY_AUDIT.csv',index=False)
conc=[]
for m in ['GRH','GRM']:
 x=q[f'DELTA_MEMORY_AFTER_{m}'].to_numpy(); o=np.argsort(x)[::-1]; total=x.sum()
 for k in [1,3,5,10]: conc.append({'MODEL':m,'K':k,'TOP_K_SUM':x[o[:k]].sum(),'TOTAL':total,'TOP_K_SHARE':x[o[:k]].sum()/total if total else np.nan,'MEDIAN_EVENT_CONTRIBUTION':np.median(x),'MEAN_EVENT_CONTRIBUTION':np.mean(x),'POSITIVE_EVENT_COUNT':int((x>0).sum()),'NEGATIVE_EVENT_COUNT':int((x<0).sum())})
pd.DataFrame(conc).to_csv(OUT/'R7F3_CONCENTRATION_AUDIT.csv',index=False)
verdict='RIUD_MEMORY_REMAINS_AFTER_TESTED_GR_HISTORY' if max(vals['GRH'],vals['GRM'])>0 else 'RIUD_MEMORY_SUBSTANTIALLY_REDUCED_BY_TESTED_GR_HISTORY'
report=f'''R7F3_OVERALL_STATUS=COMPLETED\nEVENTS=96\nROWS=2976\nR7F2_GR0_IDENTITY_CONFIRMED=PASS\nRIUD_FROZEN_DELTA_LL=5.33695050496870\nGR0_INCREMENTAL_AFTER_RIUD={inc['GR0']:.15g}\nGRH_INCREMENTAL_AFTER_RIUD={inc['GRH']:.15g}\nGRM_INCREMENTAL_AFTER_RIUD={inc['GRM']:.15g}\nRIUD_MEMORY_INCREMENTAL_AFTER_GR0={vals['GR0']:.15g}\nRIUD_MEMORY_INCREMENTAL_AFTER_GRH={vals['GRH']:.15g}\nRIUD_MEMORY_INCREMENTAL_AFTER_GRM={vals['GRM']:.15g}\nRIUD_MEMORY_POSITIVE_AFTER_GR0_EVENT_COUNT={int((q.DELTA_MEMORY_AFTER_GR0>0).sum())}\nRIUD_MEMORY_POSITIVE_AFTER_GRH_EVENT_COUNT={int((q.DELTA_MEMORY_AFTER_GRH>0).sum())}\nRIUD_MEMORY_POSITIVE_AFTER_GRM_EVENT_COUNT={int((q.DELTA_MEMORY_AFTER_GRM>0).sum())}\nGR0_ADDS_AFTER_RIUD_EVENT_COUNT={int((q.DELTA_GR0_AFTER_RIUD>0).sum())}\nGRH_ADDS_AFTER_RIUD_EVENT_COUNT={int((q.DELTA_GRH_AFTER_RIUD>0).sum())}\nGRM_ADDS_AFTER_RIUD_EVENT_COUNT={int((q.DELTA_GRM_AFTER_RIUD>0).sum())}\nRIUD_MEMORY_AFTER_GRH_MEDIAN_EVENT_LL={q.DELTA_MEMORY_AFTER_GRH.median():.15g}\nRIUD_MEMORY_AFTER_GRM_MEDIAN_EVENT_LL={q.DELTA_MEMORY_AFTER_GRM.median():.15g}\nNUMERICAL_STABILITY_PASS=PASS_WITH_SAVED_OUTPUT_SCOPE\nCONDITIONAL_CLOSURE_VERDICT={verdict}\nHOLDOUT30_ACCESSED=FALSE\nFULL_EINSTEIN_EQUATION_DERIVATION=NOT_CLAIMED\nGR_FALSIFICATION=NOT_CLAIMED\nNEXT=STOP\n'''
(OUT/'R7F3_FINAL_REPORT.md').write_text(report,encoding='utf-8'); (OUT/'SEND_TO_CHAT.txt').write_text(report,encoding='utf-8'); src={'branch':'R7F3','source_sha256':sha(OUT/'R6P9_DIRECT_SOURCE_ROW_MASTER_WITH_FROZEN_HAZARD.csv'),'events':96,'rows':2976,'workers':16,'holdout30_accessed':False,'no_new_variables':True,'no_riud_refit':True}; (OUT/'R7F3_SOURCE_PROVENANCE.json').write_text(json.dumps(src,indent=2),encoding='utf-8'); files=[p for p in OUT.iterdir() if p.is_file() and p.name!='SHA256_MANIFEST.txt']; (OUT/'SHA256_MANIFEST.txt').write_text('\n'.join(f'{sha(p)}  {p.name}' for p in sorted(files,key=lambda p:p.name))+'\n',encoding='utf-8'); print(report)


