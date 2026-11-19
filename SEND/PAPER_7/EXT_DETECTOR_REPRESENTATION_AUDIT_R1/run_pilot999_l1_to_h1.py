import os, json, time
os.environ['OMP_NUM_THREADS']='1'; os.environ['MKL_NUM_THREADS']='1'; os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np, pandas as pd
from multiprocessing import Pool
import run_audit as a

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
    rng=np.random.default_rng(20260905+999); perms=[rng.permutation(len(ids)).tolist() for _ in range(999)]
    ckpt=os.path.join(a.OUT,'pilot_checkpoint_L1_TO_H1.json')
    if os.path.exists(ckpt):
        saved=json.load(open(ckpt)); vals0={int(k):float(v) for k,v in saved.get('values',{}).items()}
    else: vals0={}
    remaining=[(k,ids,blocks,p) for k,p in enumerate(perms,1) if k not in vals0]
    vals=list(vals0.items()); started=time.time(); nworkers=min(20,os.cpu_count() or 1)
    print(f'PILOT_START direction=L1_TO_H1 null=999 workers={nworkers} RESUMED={len(vals0)} REMAINING={len(remaining)}',flush=True)
    with Pool(nworkers) as pool:
        for done,(k,v) in enumerate(pool.imap_unordered(worker,remaining,chunksize=1),1):
            vals.append((k,v))
            vals_map={str(x):y for x,y in vals}
            json.dump({'direction':'L1_TO_H1','null_n':999,'values':vals_map},open(ckpt,'w'),indent=2)
            total_done=len(vals); rate=done/max(time.time()-started,1e-9); eta=(999-total_done)/rate
            if done==1 or done%10==0 or total_done==999:
                print(f'PROGRESS={total_done}/999 RATE={rate:.3f}/s ETA_S={eta:.1f} ETA_MIN={eta/60:.1f}',flush=True)
    vals=[v for k,v in sorted(vals)]
    exceed=sum(v>=real for v in vals); p=(1+exceed)/(len(vals)+1)
    out=os.path.join(a.OUT,'05_NULL_RESULTS_PILOT999_L1_TO_H1.csv')
    pd.DataFrame({'PERMUTATION':range(1,1000),'MEDIAN_GAIN_L1_TO_H1':vals}).to_csv(out,index=False)
    result={'DIRECTION':'L1_TO_H1','NULL_N':999,'REAL_MEDIAN_GAIN':real,'EXCEEDANCES':exceed,'EMPIRICAL_P_PLUS_ONE':p,'WORKERS':min(16,os.cpu_count() or 1),'RUNTIME_S':time.time()-t,'STATUS':'PASS'}
    json.dump(result,open(os.path.join(a.OUT,'SUMMARY_PILOT999_L1_TO_H1.json'),'w'),indent=2)
    print(json.dumps(result,indent=2)); print('RUN_FINISHED_EXIT_CODE=0')
if __name__=='__main__': main()
