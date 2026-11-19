import pandas as pd
from pathlib import Path

p=Path(r'E:\RIUD_ACTIVE_20260808\MIsCORE_MT_RAW_FROM_SOURCE_R2_20260829\RAW_FRONTEND\WINDOW_10_80_EXTENDED_DIAGNOSTIC\WINDOW_10_80_ANOMALY_AUDIT\EVENT_DIRECTIONAL_ASYMMETRY.csv')
d=pd.read_csv(p)
rows=[]
for e,g in d.groupby('EVENT'):
    x=g.loc[g.ABS_LOG_RATIO.idxmax()]
    rows.append({'EVENT':e,'SOURCE_WIDTH_MS':int(x.SW),'TARGET_WIDTH_MS':int(x.TW),'LOG_RATIO':x.DIRECTIONAL_LOG_MSE_RATIO,'L1_TO_H1_MSE':x.L1_TO_H1_MSE,'H1_TO_L1_MSE':x.H1_TO_L1_MSE})
o=pd.DataFrame(rows).sort_values('LOG_RATIO',key=lambda x:x.abs(),ascending=False)
out=p.parent/'EVENT_MAX_ASYMMETRY_PAIR.csv'
o.to_csv(out,index=False)
print(o.head(20).to_string(index=False))
print(out)
