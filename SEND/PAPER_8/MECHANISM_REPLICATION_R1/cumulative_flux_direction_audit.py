from pathlib import Path
import hashlib
import pandas as pd
from scipy.stats import wilcoxon, ttest_rel, binomtest

ROOT=Path(__file__).resolve().parent
INP=Path(r'E:/RIUD_ACTIVE_20260808/MIsCORE_RIUD_MECHANISM_DISCRIMINATOR_R0_20260827/MECHANISM_DISCRIMINATOR_EVENTWISE.csv')
def main():
    d=pd.read_csv(INP)
    f=d[d.MODEL=='BM_CUM_FLUX'][['EVENT','HELDOUT_LL']].rename(columns={'HELDOUT_LL':'FORWARD_CUM_FLUX_LL'})
    r=d[d.MODEL=='BM_REVERSED_CUM_FLUX'][['EVENT','HELDOUT_LL']].rename(columns={'HELDOUT_LL':'REVERSED_CUM_FLUX_LL'})
    z=f.merge(r,on='EVENT',how='inner',validate='one_to_one'); z['FORWARD_MINUS_REVERSED']=z.FORWARD_CUM_FLUX_LL-z.REVERSED_CUM_FLUX_LL; z['FORWARD_BETTER']=z.FORWARD_MINUS_REVERSED>0
    z.to_csv(ROOT/'CUMULATIVE_FLUX_DIRECTION_EVENTWISE.csv',index=False)
    w=wilcoxon(z.FORWARD_MINUS_REVERSED,alternative='greater'); t=ttest_rel(z.FORWARD_CUM_FLUX_LL,z.REVERSED_CUM_FLUX_LL); b=binomtest(int(z.FORWARD_BETTER.sum()),n=len(z),p=0.5,alternative='greater')
    lines=['# Forward versus reversed cumulative-flux audit','',f'Input SHA256: {hashlib.sha256(INP.read_bytes()).hexdigest()}',f'Events paired: {len(z)}',f'Forward better: {int(z.FORWARD_BETTER.sum())}/{len(z)}',f'Forward worse: {int((~z.FORWARD_BETTER).sum())}/{len(z)}',f'Mean forward-minus-reversed LL: {z.FORWARD_MINUS_REVERSED.mean()}',f'Median forward-minus-reversed LL: {z.FORWARD_MINUS_REVERSED.median()}',f'Wilcoxon one-sided greater statistic={w.statistic}, p={w.pvalue}',f'Exact sign/binomial one-sided p={b.pvalue}',f'Paired t statistic={t.statistic}, p={t.pvalue}',f'Whole-model incremental difference (forward - reversed): {(-103.77941922277289)-(-107.46062097573179)}','','This is a temporal-order control from an already completed R0 discriminator. No new model, refit, feature, or event selection was introduced. The result tests directional evidence only and does not establish causality.']
    (ROOT/'CUMULATIVE_FLUX_DIRECTION_AUDIT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__': main()
