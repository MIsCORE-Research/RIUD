import pandas as pd
from pathlib import Path

p=Path(r'E:\RIUD_ACTIVE_20260808\MIsCORE_MT_RAW_FROM_SOURCE_R2_20260829\RAW_FRONTEND\WINDOW_10_80_EXTENDED_DIAGNOSTIC\WINDOW_AGGREGATION_10_80_EXTENDED_DIAGNOSTIC.csv')
d=pd.read_csv(p)
l=d[d.SOURCE_DETECTOR.eq('L1')].rename(columns={'SOURCE_WIDTH_MS':'A','TARGET_WIDTH_MS':'B','FULL_MSE':'L1short_H1broad_MSE'})[['EVENT','A','B','L1short_H1broad_MSE']]
h=d[d.SOURCE_DETECTOR.eq('H1')].rename(columns={'SOURCE_WIDTH_MS':'A','TARGET_WIDTH_MS':'B','FULL_MSE':'H1broad_L1short_MSE'})[['EVENT','A','B','H1broad_L1short_MSE']]
h=h.rename(columns={'A':'B','B':'A'})
q=l.merge(h,on=['EVENT','A','B'],validate='one_to_one')
q['ADVANTAGE_LOG_MSE']=__import__('numpy').log(q.H1broad_L1short_MSE/q.L1short_H1broad_MSE)
out=p.parent/'L1_DENSE_H1_BROAD_MATCHED_PAIRS.csv'; q.to_csv(out,index=False)
s=q.groupby(['A','B'],as_index=False).agg(L1_TO_H1_MSE=('L1short_H1broad_MSE','median'),H1_TO_L1_MSE=('H1broad_L1short_MSE','median'),ADVANTAGE_LOG_MSE=('ADVANTAGE_LOG_MSE','median'),N_L1_BETTER=('ADVANTAGE_LOG_MSE',lambda x:int((x>0).sum())))
s.to_csv(p.parent/'L1_DENSE_H1_BROAD_SUMMARY.csv',index=False)
print(s.to_string(index=False)); print('EVENTS_L1_BETTER=',int((q.ADVANTAGE_LOG_MSE>0).sum()),'/',len(q)); print(out)
