import json
from pathlib import Path
import numpy as np
import pandas as pd

SRC=Path(r'E:\RIUD_ACTIVE_20260808\MIsCORE_MT_RAW_FROM_SOURCE_R2_20260829\RAW_FRONTEND\WINDOW_10_80_EXTENDED_DIAGNOSTIC\FINE_TIME_RAW_FEATURES_10_80_EXTENDED.csv')
OUT=SRC.with_name('WINDOW_AGGREGATION_10_80_EXTENDED_DIAGNOSTIC.csv')
FEATURES=['F_PHASE_HZ','FDOT_PHASE_HZ_PER_S','LOGAMP_SLOPE_PER_S','FFT_CENTROID_HZ','FFT_PEAK_HZ','P20_100','P100_250','P250_512','RMS']
WIDTHS=[10,20,30,40,50,60,70,80]

def fit(df, sd, sw, td, tw):
    sc=[f'{sd}_{f}_{sw}MS' for f in FEATURES]; tc=[f'{td}_{f}_{tw}MS' for f in FEATURES]
    m=df[['EVENT','OFFSET_MS',*sc,*tc]].copy(); ev=sorted(m.EVENT.unique()); rows=[]
    for e in ev:
        tr=m.EVENT!=e; te=m.EVENT==e; x=m.loc[tr,sc].to_numpy(float); y=m.loc[tr,tc].to_numpy(float); xt=m.loc[te,sc].to_numpy(float); yt=m.loc[te,tc].to_numpy(float)
        ok=np.isfinite(x).all(1)&np.isfinite(y).all(1); okt=np.isfinite(xt).all(1)&np.isfinite(yt).all(1); x,y,xt,yt=x[ok],y[ok],xt[okt],yt[okt]
        xm=x.mean(0); xs=x.std(0); xs[xs==0]=1; ym=y.mean(0); ys=y.std(0); ys[ys==0]=1; x=(x-xm)/xs; y=(y-ym)/ys; xt=(xt-xm)/xs; yt=(yt-ym)/ys
        X=np.column_stack([np.ones(len(x)),x]); Xt=np.column_stack([np.ones(len(xt)),xt]); pdg=np.empty_like(yt)
        for j in range(9): pdg[:,j]=np.column_stack([Xt[:,0],Xt[:,j+1]])@np.linalg.lstsq(np.column_stack([X[:,0],X[:,j+1]]),y[:,j],rcond=None)[0]
        pf=Xt@np.linalg.lstsq(X,y,rcond=None)[0]
        rows.append({'EVENT':e,'SOURCE_DETECTOR':sd,'SOURCE_WIDTH_MS':sw,'TARGET_DETECTOR':td,'TARGET_WIDTH_MS':tw,'N_TEST_ROWS':len(yt),'DIAGONAL_MSE':float(np.mean((pdg-yt)**2)),'FULL_MSE':float(np.mean((pf-yt)**2)),'FULL_GAIN':float(np.mean((pdg-yt)**2)-np.mean((pf-yt)**2))})
    return rows

def main():
    df=pd.read_csv(SRC); rows=[]
    # Full ordered width-pair audit: do not impose monotone source/target widths.
    for sw in WIDTHS:
        for tw in WIDTHS:
            rows+=fit(df,'L1',sw,'H1',tw)
    for sw in WIDTHS:
        for tw in WIDTHS:
            rows+=fit(df,'H1',sw,'L1',tw)
    out=pd.DataFrame(rows); out.to_csv(OUT,index=False)
    s=[]
    for k,g in out.groupby(['SOURCE_DETECTOR','SOURCE_WIDTH_MS','TARGET_DETECTOR','TARGET_WIDTH_MS']):
        s.append(dict(zip(['SOURCE_DETECTOR','SOURCE_WIDTH_MS','TARGET_DETECTOR','TARGET_WIDTH_MS'],k),EVENTS=len(g),ROWS=int(g.N_TEST_ROWS.sum()),MEDIAN_DIAGONAL_MSE=float(g.DIAGONAL_MSE.median()),MEDIAN_FULL_MSE=float(g.FULL_MSE.median()),MEDIAN_FULL_GAIN=float(g.FULL_GAIN.median()),POSITIVE_GAIN_EVENTS=int((g.FULL_GAIN>0).sum())))
    Path(str(OUT)+'.summary.json').write_text(json.dumps(s,indent=2),encoding='utf-8'); print(json.dumps(s,indent=2)); print('RUN_FINISHED_EXIT_CODE=0')
if __name__=='__main__': main()
