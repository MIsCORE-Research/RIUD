import os, sys, json, hashlib, time
os.environ.setdefault('OMP_NUM_THREADS','1'); os.environ.setdefault('MKL_NUM_THREADS','1'); os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, pearsonr
from multiprocessing import Pool

SRC = r'E:\RIUD_ACTIVE_20260808\MIsCORE_RAW_EXTENDED_600MS_GAP_MT_SPECIFICITY_FINAL_R0_20260829\03_EXTENDED_RAW_PROFILE.csv'
OUT = r'E:\RIUD_ACTIVE_20260808\EXT_DETECTOR_REPRESENTATION_AUDIT_R1'
FEATURES=['F_PHASE_HZ','FDOT_PHASE_HZ_PER_S','LOGAMP_SLOPE_PER_S','FFT_CENTROID_HZ','FFT_PEAK_HZ','P20_100','P100_250','P250_512','RMS']
H=['H1_'+x for x in FEATURES]; L=['L1_'+x for x in FEATURES]
LAGS=(-10.0,0.0,10.0)

def robust_fit_scale(x):
    med=np.nanmedian(x,axis=0); mad=np.nanmedian(np.abs(x-med),axis=0); mad=np.where(mad>0,mad,1.0)
    return med,mad
def z(x,med,mad): return (x-med)/mad
def fit_predict(x,y,full):
    # x/y already finite and train-only standardized; affine fit, no regularization/refit on test
    X=np.column_stack([np.ones(len(x)),x])
    if full:
        b=np.linalg.solve(X.T@X, X.T@y)
        return X@b,b
    pred=np.empty_like(y); b=np.zeros((2,y.shape[1]))
    for j in range(y.shape[1]):
        xx=X[:,[0,j+1]]; bj=np.linalg.solve(xx.T@xx, xx.T@y[:,j])
        pred[:,j]=bj[0]+bj[1]*x[:,j]; b[:,j]=bj
    return pred,b
def aligned(offsets_a,offsets_b,lag):
    # H1 at offset t mapped to L1 at t+lag; exact offset keys only
    idx={float(t):i for i,t in enumerate(offsets_b)}
    ii=[]; jj=[]
    for i,t in enumerate(offsets_a):
        j=idx.get(float(t+lag))
        if j is not None: ii.append(i); jj.append(j)
    return np.asarray(ii,dtype=int),np.asarray(jj,dtype=int)

def evaluate(ids, blocks, perm, direction):
    # blocks keyed source event index: (offsets,H,L); perm maps H event -> L event
    fold=[]; feat=[]
    for e in range(len(ids)):
        train=[i for i in range(len(ids)) if i!=e]
        test=blocks[e]; test_y=blocks[perm[e]][2] if direction=='H1_TO_L1' else blocks[perm[e]][1]
        test_x=test[1] if direction=='H1_TO_L1' else test[2]
        best=None
        for lag in LAGS:
            tx,ty=aligned(test[0],blocks[perm[e]][0],lag) if direction=='H1_TO_L1' else aligned(test[0],blocks[perm[e]][0],lag)
            # same offset grid in this file; use explicit matching for each direction
            if direction=='H1_TO_L1':
                xte=blocks[e][1][tx]; yte=blocks[perm[e]][2][ty]
            else:
                xte=blocks[perm[e]][2][ty]; yte=blocks[e][1][tx]
            train_x=[]; train_y=[]
            for i in train:
                ii,jj=aligned(blocks[i][0],blocks[perm[i]][0],lag)
                if direction=='H1_TO_L1': train_x.append(blocks[i][1][ii]); train_y.append(blocks[perm[i]][2][jj])
                else: train_x.append(blocks[perm[i]][2][jj]); train_y.append(blocks[i][1][ii])
            x=np.concatenate(train_x); y=np.concatenate(train_y)
            tr_ok=np.isfinite(x).all(1)&np.isfinite(y).all(1); x=x[tr_ok];y=y[tr_ok]
            te_ok=np.isfinite(xte).all(1)&np.isfinite(yte).all(1); xte=xte[te_ok];yte=yte[te_ok]
            xm,xs=robust_fit_scale(x); ym,ys=robust_fit_scale(y)
            xx=z(x,xm,xs); yy=z(y,ym,ys); xxt=z(xte,xm,xs)
            for full in (False,True):
                _,coef=fit_predict(xx,yy,full)
                Xte=np.column_stack([np.ones(len(xxt)),xxt])
                if full: predte=Xte@coef
                else:
                    predte=np.column_stack([coef[0,j]+coef[1,j]*xxt[:,j] for j in range(9)])
                mse=float(np.mean((predte-z(yte,ym,ys))**2))
                key='F' if full else 'D'
                if best is None: best={}
                best.setdefault(key,[]).append((mse,lag,predte,z(yte,ym,ys)))
        # choose each model's best lag on the held-out event
        dm=min(best['D'],key=lambda q:q[0]); fm=min(best['F'],key=lambda q:q[0])
        gain=dm[0]-fm[0]
        fold.append((ids[e],dm[0],fm[0],gain,dm[1],fm[1]))
        # featurewise correlations from selected full prediction
        for j,f in enumerate(FEATURES):
            a=fm[2][:,j]; b=fm[3][:,j]
            feat.append((ids[e],f,pearsonr(a,b).statistic if len(a)>2 else np.nan,spearmanr(a,b).statistic if len(a)>2 else np.nan))
    return np.asarray(fold,dtype=object), np.asarray(feat,dtype=object)

def null_worker(args):
    ids, blocks, perm, direction = args
    fold, _ = evaluate(ids, blocks, perm, direction)
    return float(np.median(fold[:,3].astype(float)))

def main():
    t0=time.time(); df=pd.read_csv(SRC)
    with open(os.path.join(OUT,'01_COLUMN_CONTRACT.txt'),'w',encoding='utf-8') as f:
        f.write('SOURCE='+SRC+'\nN_EVENTS=%d\nN_ROWS=%d\nWINDOW_MS=-300..300\nWIDTH_MS=%s\n\n'%(df.EVENT.nunique(),len(df),','.join(map(str,sorted(df.WIDTH_MS.unique())))))
        f.write('H1/L1 FEATURE MAPPING\n')
        for a,b in zip(H,L): f.write(a+' <-> '+b+'\n')
        f.write('\nALL COLUMNS\n'+'\n'.join(df.columns)+'\n')
    ids=sorted(df.EVENT.unique()); blocks=[]
    for eid in ids:
        g=df[df.EVENT==eid].sort_values('OFFSET_MS'); blocks.append((g.OFFSET_MS.to_numpy(float),g[H].to_numpy(float),g[L].to_numpy(float)))
    identity=list(range(len(ids)))
    allfold=[]; allfeat=[]
    for direction in ('H1_TO_L1','L1_TO_H1'):
        fold,feat=evaluate(ids,blocks,identity,direction); allfold.append((direction,fold)); allfeat.append((direction,feat))
    rows=[]
    for direction,fold in allfold:
        for x in fold: rows.append([direction,*x])
    ev=pd.DataFrame(rows,columns=['DIRECTION','EVENT','DIAGONAL_MSE','FULL_MSE','GAIN','DIAGONAL_LAG_MS','FULL_LAG_MS']); ev.to_csv(os.path.join(OUT,'02_EVENT_LEVEL_RESULTS.csv'),index=False)
    fr=[]
    for direction,feat in allfeat:
        for x in feat: fr.append([direction,*x])
    pd.DataFrame(fr,columns=['DIRECTION','EVENT','FEATURE','PEARSON','SPEARMAN']).to_csv(os.path.join(OUT,'03_FEATUREWISE_RESULTS.csv'),index=False)
    # matrices from pooled standardized identity fit, diagnostic only
    for direction,srcx,srcy,name in [('H1_TO_L1',H,L,'H1_TO_L1'),('L1_TO_H1',L,H,'L1_TO_H1')]:
        x=df[srcx].to_numpy(float);y=df[srcy].to_numpy(float);xm,xs=robust_fit_scale(x);ym,ys=robust_fit_scale(y);_,coef=fit_predict(z(x,xm,xs),z(y,ym,ys),True)
        fname='06_TRANSFORM_MATRIX_H1_TO_L1.csv' if name=='H1_TO_L1' else '07_TRANSFORM_MATRIX_L1_TO_H1.csv'
        pd.DataFrame(coef[1:],index=FEATURES,columns=FEATURES).to_csv(os.path.join(OUT,fname))
    # null worker
    seed=20260905; rng=np.random.default_rng(seed); perms=[rng.permutation(len(ids)).tolist() for _ in range(99)]
    args=[(ids,blocks,p,'H1_TO_L1') for p in perms]
    with Pool(min(16,os.cpu_count() or 1)) as pool: nullh=pool.map(null_worker,args)
    args=[(ids,blocks,p,'L1_TO_H1') for p in perms]
    with Pool(min(16,os.cpu_count() or 1)) as pool: nulll=pool.map(null_worker,args)
    realh=float(ev[ev.DIRECTION=='H1_TO_L1'].GAIN.median()); reall=float(ev[ev.DIRECTION=='L1_TO_H1'].GAIN.median())
    pd.DataFrame({'PERMUTATION':range(1,100),'MEDIAN_GAIN_H1_TO_L1':nullh,'MEDIAN_GAIN_L1_TO_H1':nulll}).to_csv(os.path.join(OUT,'05_NULL_RESULTS.csv'),index=False)
    summ={'N_EVENTS':len(ids),'N_ROWS':len(df),'WINDOW_MS':'-300..300','WIDTH_MS':sorted(df.WIDTH_MS.unique().tolist()),'MODEL_DIAGONAL_OOF_ERROR':{},'MODEL_FULL_OOF_ERROR':{},'MEDIAN_GAIN_H1_TO_L1':realh,'MEDIAN_GAIN_L1_TO_H1':reall,'N_POSITIVE_GAIN_H1_TO_L1':int((ev[ev.DIRECTION=='H1_TO_L1'].GAIN>0).sum()),'N_POSITIVE_GAIN_L1_TO_H1':int((ev[ev.DIRECTION=='L1_TO_H1'].GAIN>0).sum()),'NULL_N':99,'EMPIRICAL_P_H1_TO_L1':(1+sum(v>=realh for v in nullh))/100,'EMPIRICAL_P_L1_TO_H1':(1+sum(v>=reall for v in nulll))/100,'DIRECTIONAL_STATISTIC':float(ev[ev.DIRECTION=='L1_TO_H1'].FULL_MSE.median()-ev[ev.DIRECTION=='H1_TO_L1'].FULL_MSE.median()),'RUNTIME_S':time.time()-t0}
    for d in ('H1_TO_L1','L1_TO_H1'):
        q=ev[ev.DIRECTION==d];summ['MODEL_DIAGONAL_OOF_ERROR'][d]=float(q.DIAGONAL_MSE.mean());summ['MODEL_FULL_OOF_ERROR'][d]=float(q.FULL_MSE.mean())
    summ['FINAL_VERDICT']='PILOT_ONLY_PENDING_999_NULL'; json.dump(summ,open(os.path.join(OUT,'SUMMARY.json'),'w'),indent=2)
    with open(os.path.join(OUT,'04_DIRECTIONAL_RESULTS.csv'),'w') as f:
        f.write('DIRECTION,MEDIAN_DIAGONAL_MSE,MEDIAN_FULL_MSE,MEDIAN_GAIN\n')
        for d in ('H1_TO_L1','L1_TO_H1'):
            q=ev[ev.DIRECTION==d];f.write(f'{d},{q.DIAGONAL_MSE.median()},{q.FULL_MSE.median()},{q.GAIN.median()}\n')
    print(json.dumps(summ,indent=2)); print('RUN_FINISHED_EXIT_CODE=0')
if __name__=='__main__': main()
