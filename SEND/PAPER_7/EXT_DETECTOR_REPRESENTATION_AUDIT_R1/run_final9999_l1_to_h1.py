import os, json, time
os.environ['OMP_NUM_THREADS']='1'; os.environ['MKL_NUM_THREADS']='1'; os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np, pandas as pd
from multiprocessing import Pool
import run_audit as a

N=9999
CKPT=os.path.join(a.OUT,'pilot_checkpoint_FINAL9999_L1_TO_H1.json')
OUTCSV=os.path.join(a.OUT,'05_NULL_RESULTS_FINAL9999_L1_TO_H1.csv')

def worker(args):
    k,ids,blocks,perm=args
    fold,_=a.evaluate(ids,blocks,perm,'L1_TO_H1')
    return k,float(np.median(fold[:,3].astype(float)))

def main():
    t=time.time(); df=pd.read_csv(a.SRC); ids=sorted(df.EVENT.unique()); blocks=[]
    for eid in ids:
        g=df[df.EVENT==eid].sort_values('OFFSET_MS')
        blocks.append((g.OFFSET_MS.to_numpy(float),g[a.H].to_numpy(float),g[a.L].to_numpy(float)))
    ev=pd.read_csv(os.path.join(a.OUT,'02_EVENT_LEVEL_RESULTS.csv'))
    real=float(ev[ev.DIRECTION=='L1_TO_H1'].GAIN.median())
    rng=np.random.default_rng(20260905+9999); perms=[rng.permutation(len(ids)).tolist() for _ in range(N)]
    vals0={}
    if os.path.exists(CKPT):
        j=json.load(open(CKPT)); vals0={int(k):float(v) for k,v in j.get('values',{}).items()}
    remaining=[(k,ids,blocks,p) for k,p in enumerate(perms,1) if k not in vals0]
    vals=list(vals0.items()); started=time.time(); nw=min(20,os.cpu_count() or 1)
    print(f'FINAL_START direction=L1_TO_H1 null={N} workers={nw} RESUMED={len(vals0)} REMAINING={len(remaining)}',flush=True)
    with Pool(nw) as pool:
        for done,(k,v) in enumerate(pool.imap_unordered(worker,remaining,chunksize=1),1):
            vals.append((k,v)); json.dump({'direction':'L1_TO_H1','null_n':N,'values':{str(x):y for x,y in vals}},open(CKPT,'w'),indent=2)
            total=len(vals); rate=done/max(time.time()-started,1e-9); eta=(N-total)/rate
            if done==1 or done%25==0 or total==N:
                print(f'PROGRESS={total}/{N} RATE={rate:.4f}/s ETA_S={eta:.1f} ETA_H={eta/3600:.2f}',flush=True)
    vals=[v for k,v in sorted(vals)]; exceed=sum(v>=real for v in vals); p=(1+exceed)/(N+1)
    pd.DataFrame({'PERMUTATION':range(1,N+1),'MEDIAN_GAIN_L1_TO_H1':vals}).to_csv(OUTCSV,index=False)
    result={'DIRECTION':'L1_TO_H1','NULL_N':N,'REAL_MEDIAN_GAIN':real,'EXCEEDANCES':exceed,'EMPIRICAL_P_PLUS_ONE':p,'WORKERS':nw,'RUNTIME_S':time.time()-t,'STATUS':'PASS'}
    json.dump(result,open(os.path.join(a.OUT,'SUMMARY_FINAL9999_L1_TO_H1.json'),'w'),indent=2)
    print(json.dumps(result,indent=2)); print('RUN_FINISHED_EXIT_CODE=0')
if __name__=='__main__': main()
