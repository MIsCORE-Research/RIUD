from pathlib import Path
import hashlib
import pandas as pd

ROOT=Path(__file__).resolve().parent
INP=ROOT/'S_TERM_HAZARD_DECOMPOSITION.csv'
def main():
    d=pd.read_csv(INP)
    g=d.groupby(['BIN_INDEX','TRANSITION_TYPE'],dropna=False).agg(ROWS=('ROW_KEY','size'),EVENTS=('EVENT','nunique'),SUM_S_DELTA_LL=('S_DELTA_LOGPROB','sum'),MEDIAN_S_DELTA_LL=('S_DELTA_LOGPROB','median'),POSITIVE_ROWS=('S_DELTA_LOGPROB',lambda x:int((x>0).sum())),NEGATIVE_ROWS=('S_DELTA_LOGPROB',lambda x:int((x<0).sum()))).reset_index()
    g.to_csv(ROOT/'S_TERM_BINWISE_PROFILE.csv',index=False)
    b=d.groupby('BIN_INDEX',as_index=False).agg(ROWS=('ROW_KEY','size'),EVENTS=('EVENT','nunique'),SUM_S_DELTA_LL=('S_DELTA_LOGPROB','sum'),MEDIAN_S_DELTA_LL=('S_DELTA_LOGPROB','median'),POSITIVE_ROWS=('S_DELTA_LOGPROB',lambda x:int((x>0).sum())),NEGATIVE_ROWS=('S_DELTA_LOGPROB',lambda x:int((x<0).sum())))
    b['CUMULATIVE_S_DELTA_LL']=b.SUM_S_DELTA_LL.cumsum(); b.to_csv(ROOT/'S_TERM_BINWISE_TOTAL.csv',index=False)
    lines=['# Frozen S-term binwise profile','',f'Input SHA256: {hashlib.sha256(INP.read_bytes()).hexdigest()}',f'Rows: {len(d)}','', 'Bin index is inherited from the frozen R40 hazard table. No time re-registration, window change, or change-point selection was performed.','', '## Total by bin']
    for _,r in b.iterrows(): lines.append(f"- bin={int(r.BIN_INDEX)}; rows={int(r.ROWS)}; events={int(r.EVENTS)}; sum={r.SUM_S_DELTA_LL}; median={r.MEDIAN_S_DELTA_LL}; cumulative={r.CUMULATIVE_S_DELTA_LL}; positive/negative={int(r.POSITIVE_ROWS)}/{int(r.NEGATIVE_ROWS)}")
    lines += ['', '## Interpretation','', 'The table is a descriptive profile of where the already-frozen S term changes row likelihood. It does not establish a source mechanism or create a new physical law.']
    (ROOT/'S_TERM_BINWISE_PROFILE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__': main()
