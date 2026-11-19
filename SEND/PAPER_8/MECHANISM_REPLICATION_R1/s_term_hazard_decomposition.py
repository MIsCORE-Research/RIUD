import hashlib, math
from pathlib import Path
import pandas as pd

INP=Path(r'E:/RIUD_ACTIVE_20260808/MIsCORE_R40_BLIND_ROW_IDENTITY_R2_20260827/CANONICAL_R40_EVENT_LEVEL_HAZARD.csv')
OUT=Path(__file__).resolve().parent
GAMMA=0.3162354634393393

def safe_p(lam,du): return -math.expm1(-lam*du)
def main():
    d=pd.read_csv(INP)
    d['GAMMA_S']=GAMMA*d['S_STANDARDIZED']
    d['ETA_P1_WITHOUT_S']=d['ETA_P1']-d['GAMMA_S']
    d['LAMBDA_P1_WITHOUT_S']=d['LAMBDA_P1']/d['GAMMA_S'].map(math.exp)
    d['P_P1_WITHOUT_S']=[safe_p(float(a),float(b)) for a,b in zip(d['LAMBDA_P1_WITHOUT_S'],d['DU_CANONICAL'])]
    d['LOGPROB_P1_WITHOUT_S']=[math.log(max(float(p),1e-300)) if int(y)==1 else math.log(max(1-float(p),1e-300)) for p,y in zip(d['P_P1_WITHOUT_S'],d['OBSERVED_SUCCESS'])]
    d['S_DELTA_LOGPROB']=d['LOGPROB_P1']-d['LOGPROB_P1_WITHOUT_S']
    cols=['ROW_KEY','EVENT','BIN_INDEX','SOURCE_STATE','TARGET_STATE','TRANSITION_TYPE','RUN_BUCKET','AGE_CLASS','OBSERVED_SUCCESS','DU_CANONICAL','S_STANDARDIZED','GAMMA_S','ETA_P1','ETA_P1_WITHOUT_S','LAMBDA_P1_WITHOUT_S','LAMBDA_P1','P_P1_WITHOUT_S','P_P1','S_DELTA_LOGPROB']
    out=d[cols].copy(); out.to_csv(OUT/'S_TERM_HAZARD_DECOMPOSITION.csv',index=False)
    q=d[['GAMMA_S','LAMBDA_P1_WITHOUT_S','LAMBDA_P1','P_P1_WITHOUT_S','P_P1','S_DELTA_LOGPROB']].describe(percentiles=[.01,.05,.25,.5,.75,.95,.99]).T
    q.to_csv(OUT/'S_TERM_HAZARD_DECOMPOSITION_SUMMARY.csv')
    lines=['# Frozen R40 S-term hazard decomposition','',f'Input rows: {len(d)}',f'Input SHA256: {hashlib.sha256(INP.read_bytes()).hexdigest()}',f'Frozen gamma: {GAMMA}','', 'For each frozen R40 P1 row, eta_without_S = eta_P1 - gamma*S. No coefficient, state, history, or likelihood refit was performed. The decomposition is algebraic and descriptive; it does not establish a microscopic origin.','', 'Key quantities:','- `GAMMA_S` is the additive S contribution to eta.','- `LAMBDA_P1_WITHOUT_S` and `P_P1_WITHOUT_S` are the counterfactual frozen P1 hazard/probability with only the S term removed.','- `S_DELTA_LOGPROB` is the row log-probability change attributable to restoring the frozen S term relative to that counterfactual.','']
    for _,r in q.iterrows(): lines.append(f"- {r.name}: median={r['50%']}, IQR=[{r['25%']},{r['75%']}], min/max=[{r['min']},{r['max']}]")
    lines += ['',f"Total S-only log-probability contribution: {d['S_DELTA_LOGPROB'].sum()}",f"Positive-row count: {(d['S_DELTA_LOGPROB']>0).sum()}/{len(d)}",f"Negative-row count: {(d['S_DELTA_LOGPROB']<0).sum()}/{len(d)}",'','This does not turn S into a timestamp. It quantifies its role as a multiplicative hazard-rate modifier inside the frozen R40 operator.']
    (OUT/'S_TERM_HAZARD_DECOMPOSITION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__': main()
