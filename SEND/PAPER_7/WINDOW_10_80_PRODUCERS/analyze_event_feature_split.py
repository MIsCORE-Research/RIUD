from pathlib import Path
import numpy as np
import pandas as pd
from analyze_window_feature_anomalies import one, FEATURES, SRC

OUT=SRC.parent/'WINDOW_FEATURE_ANOMALY_AUDIT'
df=pd.read_csv(SRC); rows=[]
for w in [40,50,60,70,80]:
    a=one(df,'L1',10,'H1',w).set_index('EVENT'); b=one(df,'H1',w,'L1',10).set_index('EVENT')
    for e in a.index:
        r={'EVENT':e,'H1_TARGET_MS':w}
        for f in FEATURES:
            r[f+'_ADV']=float(np.log(b.loc[e,'MSE_'+f]/a.loc[e,'MSE_'+f]))
        r['HIGH_FREQ_MEAN']=np.mean([r[x+'_ADV'] for x in ['FDOT_PHASE_HZ_PER_S','FFT_PEAK_HZ','P100_250','P250_512']])
        r['ENVELOPE_MEAN']=np.mean([r[x+'_ADV'] for x in ['LOGAMP_SLOPE_PER_S','FFT_CENTROID_HZ','RMS']])
        r['SPLIT_SIGN']=('OPPOSITE' if r['HIGH_FREQ_MEAN']*r['ENVELOPE_MEAN']<0 else 'SAME')
        rows.append(r)
q=pd.DataFrame(rows); q.to_csv(OUT/'EVENT_FEATURE_SPLIT_BY_WIDTH.csv',index=False)
for w,g in q.groupby('H1_TARGET_MS'):
    print('WIDTH',w,'OPPOSITE',int((g.SPLIT_SIGN=='OPPOSITE').sum()),'SAME',int((g.SPLIT_SIGN=='SAME').sum()),'high_median',g.HIGH_FREQ_MEAN.median(),'env_median',g.ENVELOPE_MEAN.median())
print(q.sort_values(['H1_TARGET_MS','HIGH_FREQ_MEAN'],key=lambda s:s if s.name=='H1_TARGET_MS' else s.abs(),ascending=False).head(20).to_string(index=False))
print('RUN_FINISHED_EXIT_CODE=0')
