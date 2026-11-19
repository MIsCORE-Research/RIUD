import hashlib
from pathlib import Path
import pandas as pd

INP=Path(__file__).resolve().parent / "S_TERM_HAZARD_DECOMPOSITION.csv"
OUT=Path(__file__).resolve().parent

def agg(df, keys):
    g=df.groupby(keys,dropna=False).agg(N=('ROW_KEY','size'),EVENTS=('EVENT','nunique'),S_DELTA_LL=('S_DELTA_LOGPROB','sum'),MEDIAN_S_DELTA_LL=('S_DELTA_LOGPROB','median'),POSITIVE_ROWS=('S_DELTA_LOGPROB',lambda x:int((x>0).sum())),NEGATIVE_ROWS=('S_DELTA_LOGPROB',lambda x:int((x<0).sum()))).reset_index()
    g['ABS_SHARE_OF_TOTAL']=g.S_DELTA_LL.abs()/max(df.S_DELTA_LOGPROB.sum().__abs__(),1e-300)
    return g
def main():
    d=pd.read_csv(INP)
    tables=[('S_TERM_BY_SOURCE_STATE.csv',['SOURCE_STATE']),('S_TERM_BY_TRANSITION.csv',['TRANSITION_TYPE']),('S_TERM_BY_OBSERVED_SUCCESS.csv',['OBSERVED_SUCCESS']),('S_TERM_BY_RUN_BUCKET.csv',['RUN_BUCKET']),('S_TERM_BY_AGE_CLASS.csv',['AGE_CLASS'])]
    for name,keys in tables: agg(d,keys).to_csv(OUT/name,index=False)
    lines=['# Frozen S-term concentration audit','',f'Input rows: {len(d)}',f'Input SHA256: {hashlib.sha256(INP.read_bytes()).hexdigest()}','', 'This is an algebraic grouping of the previously generated frozen S-term decomposition. No new variables, fit, threshold, state rule, or event selection was introduced.','',f"TOTAL_S_ONLY_DELTA_LL={d.S_DELTA_LOGPROB.sum()}",f"TOTAL_POSITIVE_ROWS={(d.S_DELTA_LOGPROB>0).sum()}",f"TOTAL_NEGATIVE_ROWS={(d.S_DELTA_LOGPROB<0).sum()}",'']
    for label,keys in [('source state',['SOURCE_STATE']),('transition type',['TRANSITION_TYPE']),('observed success',['OBSERVED_SUCCESS']),('run bucket',['RUN_BUCKET']),('age class',['AGE_CLASS'])]:
        lines.append('## '+label)
        for _,r in agg(d,keys).iterrows(): lines.append(' - '+'; '.join(f'{k}={r[k]}' for k in keys)+f"; N={int(r.N)}; events={int(r.EVENTS)}; S_delta_LL={r.S_DELTA_LL}; abs_share={r.ABS_SHARE_OF_TOTAL}")
        lines.append('')
    lines.append('Interpretation is limited to where the frozen R40 hazard receives its S contribution; it is not a source-level causal attribution.')
    (OUT/'S_TERM_CONCENTRATION_AUDIT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__': main()
