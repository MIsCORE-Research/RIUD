import hashlib, json
from pathlib import Path
import pandas as pd
OUT=Path(__file__).parent
def sha(p):
 h=hashlib.sha256(); f=open(p,'rb')
 for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 f.close(); return h.hexdigest()
pd.DataFrame([{'CONTRACT':'R7F2 exact event-held-out universe','OUTER_HELD_EVENTS':96,'ROWS':2976,'INNER_EVENT_FOLDS':5,'SELECTION':'training-event validation LL minus frozen offset LL','CANDIDATE_FAMILIES':6,'RIUD_REFIT':False,'HOLDOUT30':False},{'CONTRACT':'R7F3 conditional augmentation','MODELS':'GR0|GRH|GRM','OFFSET':'frozen ETA_RIUD_FULL or frozen ETA_RIUD_NO_MEMORY','GR_COEFFICIENTS':'training events only','R2_CONTRACT_REUSED':True}]).to_csv(OUT/'R7F3_INNER_SELECTION_AUDIT.csv',index=False)
(OUT/'R7F3_DESIGN_LOCK.md').write_text('R7F3 conditional closure uses the exact R7F2 96-event/2976-row universe, six fixed GR candidate families, GR0/GRH/GRM feature definitions, 5 inner event folds, and 96 outer held events. Frozen RIUD full predictor and term ablations are offsets; RIUD coefficients are not refit. Holdout30 is untouched.',encoding='utf-8')
(OUT/'R7F3_CLAIM_BOUNDARY.md').write_text('This is a conditional information test, not an Einstein-equation derivation, GR falsification, full-waveform exhaustion, horizon test, or Holdout30 validation. The conclusion is restricted to the tested source-waveform instantaneous/history/kernel representations.',encoding='utf-8')
(OUT/'R7F3_R7_LINEAGE_NOTE.md').write_text('R7F3 is the single conditional-closure branch after R7F2 exact GR0 identity recovery. It tests whether frozen RIUD memory remains after fixed GR source-waveform history/kernel augmentation.',encoding='utf-8')
src={'branch':'MIsCORE_RIUD_GR_MEMORY_CONDITIONAL_CLOSURE_R7F3_20260827','input':'R7F2 exact source row master','input_sha256':sha(OUT/'R6P9_DIRECT_SOURCE_ROW_MASTER_WITH_FROZEN_HAZARD.csv'),'r7f2_identity':'PASS','events':96,'rows':2976,'workers':16,'holdout30_accessed':False,'new_variables':False,'riud_refit':False}
(OUT/'R7F3_SOURCE_PROVENANCE.json').write_text(json.dumps(src,indent=2),encoding='utf-8')
files=[p for p in OUT.iterdir() if p.is_file() and p.name!='SHA256_MANIFEST.txt']; (OUT/'SHA256_MANIFEST.txt').write_text('\n'.join(f'{sha(p)}  {p.name}' for p in sorted(files,key=lambda p:p.name))+'\n',encoding='utf-8')
print('R7F3_ARTIFACTS=COMPLETE')
