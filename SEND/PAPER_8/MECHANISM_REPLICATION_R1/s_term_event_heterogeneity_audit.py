from pathlib import Path
import hashlib
import pandas as pd

ROOT=Path(__file__).resolve().parent
S=ROOT/'S_TERM_HAZARD_DECOMPOSITION.csv'
L=Path(__file__).resolve().parents[2] / "PAPER_6" / "EVIDENCE" / "17_RIUD_ABC_INTEGRATED_MAP_LAW_LEDGER_R0_20260825" / "ABC_96_EVENT_INTEGRATED_LEDGER.csv"

def summarize(d,keys):
    return d.groupby(keys,dropna=False).agg(EVENTS=('EVENT','nunique'),SUM_S_DELTA_LL=('EVENT_S_DELTA_LL','sum'),MEDIAN_EVENT_S_DELTA_LL=('EVENT_S_DELTA_LL','median'),MEAN_EVENT_S_DELTA_LL=('EVENT_S_DELTA_LL','mean'),MIN_EVENT_S_DELTA_LL=('EVENT_S_DELTA_LL','min'),MAX_EVENT_S_DELTA_LL=('EVENT_S_DELTA_LL','max')).reset_index()
def main():
    s=pd.read_csv(S); ev=s.groupby('EVENT',as_index=False).agg(EVENT_S_DELTA_LL=('S_DELTA_LOGPROB','sum'),ROWS=('ROW_KEY','size'))
    l=pd.read_csv(L); l=l.rename(columns={'EVENT_ID':'EVENT'}); l['MAX_FLOW_PRE_T0']=l['MAX_FLOW']<l['T0']
    d=ev.merge(l[['EVENT','ABC_CLASS','MAX_FLOW_PRE_T0','PHYSICAL_SUPPORT']],on='EVENT',how='left',validate='one_to_one')
    d.to_csv(ROOT/'S_TERM_EVENT_LEVEL.csv',index=False)
    tables=[('S_TERM_BY_ABC.csv',['ABC_CLASS']),('S_TERM_BY_MAXFLOW_SIDE.csv',['MAX_FLOW_PRE_T0']),('S_TERM_BY_ABC_AND_MAXFLOW.csv',['ABC_CLASS','MAX_FLOW_PRE_T0'])]
    for n,k in tables: summarize(d,k).to_csv(ROOT/n,index=False)
    lines=['# Event-level heterogeneity of the frozen S contribution','',f'S-term input SHA256: {hashlib.sha256(S.read_bytes()).hexdigest()}',f'landmark input SHA256: {hashlib.sha256(L.read_bytes()).hexdigest()}',f'Events with S rows: {len(ev)}', '','This is a post hoc descriptive join to pre-existing frozen ABC and MAX_FLOW labels. No label, coefficient, threshold, or event selection was changed.','']
    for label,k in [('ABC',['ABC_CLASS']),('MAX_FLOW side',['MAX_FLOW_PRE_T0']),('ABC × MAX_FLOW side',['ABC_CLASS','MAX_FLOW_PRE_T0'])]:
        lines.append('## '+label)
        for _,r in summarize(d,k).iterrows(): lines.append(' - '+'; '.join(f'{x}={r[x]}' for x in k)+f"; events={int(r.EVENTS)}; sum={r.SUM_S_DELTA_LL}; median_event={r.MEDIAN_EVENT_S_DELTA_LL}; mean_event={r.MEAN_EVENT_S_DELTA_LL}; min/max=[{r.MIN_EVENT_S_DELTA_LL},{r.MAX_EVENT_S_DELTA_LL}]")
        lines.append('')
    lines += [f"Overall event-level mean={d.EVENT_S_DELTA_LL.mean()}",f"Overall event-level median={d.EVENT_S_DELTA_LL.median()}",'','Interpretation: this tests heterogeneity of the frozen rate modulation, not whether S is a physical timestamp or its microscopic source.']
    (ROOT/'S_TERM_EVENT_HETEROGENEITY_AUDIT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__': main()
