import hashlib
from pathlib import Path
import pandas as pd
from scipy.stats import spearmanr, pearsonr

INP = Path(__file__).resolve().parents[2] / "PAPER_6" / "EVIDENCE" / "17_RIUD_ABC_INTEGRATED_MAP_LAW_LEDGER_R0_20260825" / "ABC_96_EVENT_INTEGRATED_LEDGER.csv"
OUT = Path(__file__).resolve().parent
LANDMARKS = ['GAP_TIME','MT','MAX_FLOW','PEAK','W1_START_NATIVE','W2_START_NATIVE','W3_START_NATIVE','W4_START_NATIVE','W1_END_NATIVE','W2_END_NATIVE','W3_END_NATIVE','W4_END_NATIVE']

def main():
    df = pd.read_csv(INP)
    rows=[]
    for col in LANDMARKS:
        z=df[['S_A',col]].dropna()
        if len(z)<3 or z['S_A'].nunique()<2 or z[col].nunique()<2:
            rows.append({'LANDMARK':col,'N':len(z),'SPEARMAN_R':'','SPEARMAN_P':'','PEARSON_R':'','STATUS':'NOT_COMPUTABLE_CONSTANT_OR_INSUFFICIENT'})
            continue
        sr,sp=spearmanr(z['S_A'],z[col]); pr,_=pearsonr(z['S_A'],z[col])
        rows.append({'LANDMARK':col,'N':len(z),'SPEARMAN_R':sr,'SPEARMAN_P':sp,'PEARSON_R':pr,'STATUS':'COMPUTED_FROZEN_EVENT_TABLE'})
    out=OUT/'S_A_VS_LANDMARK_TIMING_AUDIT.csv'
    pd.DataFrame(rows).to_csv(out,index=False)
    h=hashlib.sha256(INP.read_bytes()).hexdigest()
    lines=['# S_A versus landmark timing audit','',f'Input rows: {len(df)}',f'S_A available rows: {df.S_A.notna().sum()}','Input SHA256: '+h,'','No refit, no new time reference, and no landmark re-selection were used. T0 is constant in this table and is therefore not a correlation target. S_A is available only for the A-only physical cohort represented in this ledger.','', 'The audit tests whether S_A is itself a timestamp. Correlation with landmarks is descriptive and does not establish causality or a time conversion.']
    for r in rows: lines.append(f"- {r['LANDMARK']}: N={r['N']}, Spearman={r['SPEARMAN_R']}, Pearson={r['PEARSON_R']}, status={r['STATUS']}")
    (OUT/'S_A_VS_LANDMARK_TIMING_AUDIT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__': main()
