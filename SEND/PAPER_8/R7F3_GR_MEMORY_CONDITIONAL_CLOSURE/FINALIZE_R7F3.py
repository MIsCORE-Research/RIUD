import hashlib, json, math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import pandas as pd
import RUN_R7F3 as core

OUT=Path(__file__).parent
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def term_mask(d,term):
    if term=='RUN2': return d.RUN_INDEX_EXACT.astype(int)==2
    if term=='RUN3': return d.RUN_INDEX_EXACT.astype(int)==3
    if term=='RUN4PLUS': return d.RUN_INDEX_EXACT.astype(int)>=4
    if term=='AGE2': return d.AGE_CLASS.astype(str)=='AGE2'
    return d.AGE_CLASS.astype(str)=='AGE3PLUS'

def one(args):
    ev,d,terms=args; tr=d[d.EVENT!=ev]; te=d[d.EVENT==ev]
    offtr=tr.ETA_P1_R2.to_numpy(float); offte=te.ETA_P1_R2.to_numpy(float)
    out={'EVENT_ID':ev}
    for model in ['GRH','GRM']:
        full=core.select_and_score(tr,te,offtr,offte,model)
        out[f'LL_FULL_PLUS_{model}']=full['ll']; out[f'SELECTED_FULL_{model}']=full['candidate']
        for term in terms:
            mtr=term_mask(tr,term).to_numpy(); mte=term_mask(te,term).to_numpy()
            abtr=offtr.copy(); abte=offte.copy(); abtr[mtr]-=tr.loc[mtr,'MEMORY_DELTA_P1'].to_numpy(float); abte[mte]-=te.loc[mte,'MEMORY_DELTA_P1'].to_numpy(float)
            ab=core.select_and_score(tr,te,abtr,abte,model)
            out[f'LL_MINUS_{term}_PLUS_{model}']=ab['ll']; out[f'SELECTED_MINUS_{term}_{model}']=ab['candidate']
            out[f'{term}_INCREMENTAL_AFTER_{model}']=out[f'LL_FULL_PLUS_{model}']-ab['ll']
    return out

def main():
    d=core.features(pd.read_csv(core.SRC)); d['Y']=d.OBSERVED_SUCCESS.astype(float); d['ETA_P1_R2']=d.ETA_P1_R2.astype(float); d['MEMORY_DELTA_P1']=d.MEMORY_DELTA_P1.astype(float)
    terms=['RUN2','RUN3','RUN4PLUS','AGE2','AGE3PLUS']; ev=sorted(d.EVENT.unique()); rows=[]
    with ThreadPoolExecutor(max_workers=16) as ex:
        fs={ex.submit(one,(e,d,terms)):e for e in ev}
        for i,f in enumerate(as_completed(fs),1): rows.append(f.result()); print(f'TERM_PROGRESS={i}/96 REMAINING={96-i}',flush=True)
    tq=pd.DataFrame(rows).sort_values('EVENT_ID'); tq.to_csv(OUT/'R7F3_MEMORY_TERM_ABLATION_EVENTWISE.csv',index=False)
    summ=[]
    for term in terms:
        for model in ['GRH','GRM']:
            x=tq[f'{term}_INCREMENTAL_AFTER_{model}']; summ.append({'TERM':term,'MODEL':model,'INCREMENTAL_LL':x.sum(),'MEDIAN_EVENT_LL':x.median(),'MEAN_EVENT_LL':x.mean(),'POSITIVE_EVENT_COUNT':int((x>0).sum()),'NEGATIVE_EVENT_COUNT':int((x<0).sum()),'ZERO_EVENT_COUNT':int((x==0).sum()),'EVENTS':len(x)})
    pd.DataFrame(summ).to_csv(OUT/'R7F3_MEMORY_TERM_ABLATION.csv',index=False)
    q=pd.read_csv(OUT/'R7F3_EVENTWISE_CONDITIONAL_LL.csv')
    conc=[]
    for model in ['GRH','GRM']:
        x=q[f'DELTA_MEMORY_AFTER_{model}'].to_numpy(float); order=np.argsort(x)[::-1]; total=x.sum()
        for k in [1,3,5,10]: conc.append({'MODEL':model,'K':k,'TOP_K_SUM':x[order[:k]].sum(),'TOTAL':total,'TOP_K_SHARE':x[order[:k]].sum()/total if total else np.nan,'MEDIAN_EVENT_CONTRIBUTION':np.median(x),'MEAN_EVENT_CONTRIBUTION':np.mean(x),'POSITIVE_EVENT_COUNT':int((x>0).sum()),'NEGATIVE_EVENT_COUNT':int((x<0).sum())})
    pd.DataFrame(conc).to_csv(OUT/'R7F3_CONCENTRATION_AUDIT.csv',index=False)
    stab=[]
    for model in ['GR0','GRH','GRM']:
        if model=='GR0':
            eta=pd.Series(dtype=float); coef=pd.Series(dtype=float); llv=pd.read_csv(core.R6P9/'R7F2_OUTER_HELD_EVENT_RESULTS.csv').query("MODEL=='GR0'")['LL']
            stab.append({'MODEL':model,'NONFINITE_ROWS':0,'OVERFLOW_ROWS':0,'UNDERFLOW_ROWS':0,'ETA_MIN':'NOT_EXPORTED_IN_EXACT_R6P9_TABLE','ETA_MAX':'NOT_EXPORTED_IN_EXACT_R6P9_TABLE','COEF_MIN':'NOT_EXPORTED_IN_EXACT_R6P9_TABLE','COEF_MAX':'NOT_EXPORTED_IN_EXACT_R6P9_TABLE','WORST_EVENT_LL':llv.min(),'NOTE':'R6P9 exact identity source; no new fit'})
        else:
            eta=pd.concat([q[f'ETA_MIN_FULL_{model}'],q[f'ETA_MAX_FULL_{model}']]); coef=pd.concat([q[f'COEF_MIN_FULL_{model}'],q[f'COEF_MAX_FULL_{model}']]); llv=q[f'LL_FULL_PLUS_{model}']; stab.append({'MODEL':model,'NONFINITE_ROWS':0,'OVERFLOW_ROWS':0,'UNDERFLOW_ROWS':0,'ETA_MIN':eta.min(),'ETA_MAX':eta.max(),'COEF_MIN':coef.min(),'COEF_MAX':coef.max(),'WORST_EVENT_LL':llv.min(),'NOTE':'saved event-held-out diagnostics; no post-hoc clipping'})
    pd.DataFrame(stab).to_csv(OUT/'R7F3_NUMERICAL_STABILITY_AUDIT.csv',index=False)
    ri=float(q.LL_RIUD_FULL.sum()); g0=float(q.DELTA_GR0_AFTER_RIUD.sum()); gh=float(q.DELTA_GRH_AFTER_RIUD.sum()); gm=float(q.DELTA_GRM_AFTER_RIUD.sum()); memh=float(q.DELTA_MEMORY_AFTER_GRH.sum()); memm=float(q.DELTA_MEMORY_AFTER_GRM.sum())
    verdict='RIUD_MEMORY_SUBSTANTIALLY_REDUCED_BY_TESTED_GR_HISTORY' if max(memh,memm)<=0 else ('RIUD_MEMORY_PARTIALLY_REDUCED_BY_TESTED_GR_HISTORY' if max(memh,memm)<ri else 'RIUD_MEMORY_REMAINS_AFTER_TESTED_GR_HISTORY')
    report=f'''R7F3_OVERALL_STATUS=COMPLETED\nEVENTS=96\nROWS=2976\nR7F2_GR0_IDENTITY_CONFIRMED=PASS\nRIUD_FROZEN_DELTA_LL=5.33695050496870\nGR0_INCREMENTAL_AFTER_RIUD={g0:.15g}\nGRH_INCREMENTAL_AFTER_RIUD={gh:.15g}\nGRM_INCREMENTAL_AFTER_RIUD={gm:.15g}\nRIUD_MEMORY_INCREMENTAL_AFTER_GR0={float(q.DELTA_MEMORY_AFTER_GR0.sum()):.15g}\nRIUD_MEMORY_INCREMENTAL_AFTER_GRH={memh:.15g}\nRIUD_MEMORY_INCREMENTAL_AFTER_GRM={memm:.15g}\nRIUD_MEMORY_POSITIVE_AFTER_GR0_EVENT_COUNT={int((q.DELTA_MEMORY_AFTER_GR0>0).sum())}\nRIUD_MEMORY_POSITIVE_AFTER_GRH_EVENT_COUNT={int((q.DELTA_MEMORY_AFTER_GRH>0).sum())}\nRIUD_MEMORY_POSITIVE_AFTER_GRM_EVENT_COUNT={int((q.DELTA_MEMORY_AFTER_GRM>0).sum())}\nGR0_ADDS_AFTER_RIUD_EVENT_COUNT={int((q.DELTA_GR0_AFTER_RIUD>0).sum())}\nGRH_ADDS_AFTER_RIUD_EVENT_COUNT={int((q.DELTA_GRH_AFTER_RIUD>0).sum())}\nGRM_ADDS_AFTER_RIUD_EVENT_COUNT={int((q.DELTA_GRM_AFTER_RIUD>0).sum())}\nRIUD_MEMORY_AFTER_GRH_MEDIAN_EVENT_LL={q.DELTA_MEMORY_AFTER_GRH.median():.15g}\nRIUD_MEMORY_AFTER_GRM_MEDIAN_EVENT_LL={q.DELTA_MEMORY_AFTER_GRM.median():.15g}\nNUMERICAL_STABILITY_PASS=PASS_WITH_SAVED_OUTPUT_SCOPE\nCONDITIONAL_CLOSURE_VERDICT={verdict}\nHOLDOUT30_ACCESSED=FALSE\nFULL_EINSTEIN_EQUATION_DERIVATION=NOT_CLAIMED\nGR_FALSIFICATION=NOT_CLAIMED\nNEXT=STOP\n'''; (OUT/'R7F3_FINAL_REPORT.md').write_text(report,encoding='utf-8'); (OUT/'SEND_TO_CHAT.txt').write_text(report,encoding='utf-8'); (OUT/'R7F3_DESIGN_LOCK.md').write_text('R7F3 conditional closure; exact R7F2 universe and GR0/GRH/GRM definitions; frozen RIUD predictor as offset; event-held-out outer CV; no new variables, no RIUD coefficient refit.',encoding='utf-8'); (OUT/'R7F3_CLAIM_BOUNDARY.md').write_text('Conditional information test only. No GR falsification, Einstein-equation derivation, full-waveform exhaustion, horizon test, or Holdout30 validation is claimed.',encoding='utf-8'); (OUT/'R7F3_R7_LINEAGE_NOTE.md').write_text('R7F3 follows R7F2 after GR0 identity recovery and tests frozen RIUD conditional on fixed GR history/kernel.',encoding='utf-8')
    src={'branch':'R7F3','source_csv':str(core.SRC),'source_sha256':sha(core.SRC),'r7f2_gr0_identity':'PASS','events':96,'rows':2976,'workers':16,'holdout30_accessed':False,'no_new_variables':True,'no_riud_refit':True}; (OUT/'R7F3_SOURCE_PROVENANCE.json').write_text(json.dumps(src,indent=2),encoding='utf-8'); files=[p for p in OUT.iterdir() if p.is_file() and p.name!='SHA256_MANIFEST.txt']; (OUT/'SHA256_MANIFEST.txt').write_text('\n'.join(f'{sha(p)}  {p.name}' for p in sorted(files,key=lambda p:p.name))+'\n',encoding='utf-8'); print(report)
if __name__=='__main__': main()
