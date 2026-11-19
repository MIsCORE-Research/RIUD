import csv, hashlib, json, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
import sxs

ROOT=Path(__file__).resolve().parent
ARCH=ROOT/'R8_SECONDARY_NR_SOURCE_ARCHIVE'
IDS='0001 0003 0154 0153 0006 0009 0339 0179 0030 0045 0261 0260 0054 0031 1160 0165'.split()
FILES=['metadata.json','Horizons.h5','ExtraWaveforms.h5','Strain_N2.h5','Strain_N2.json']

def digest(p):
 h=hashlib.sha256(); n=0
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b); n+=len(b)
 return h.hexdigest(),n
def dl(job):
 sid,lev,fname,info=job; out=ARCH/sid/fname; out.parent.mkdir(parents=True,exist_ok=True)
 if not out.exists() or (info.get('size') is not None and out.stat().st_size!=info['size']):
  part=out.with_suffix(out.suffix+'.part'); req=Request(info['link'],headers={'User-Agent':'MIsCORE-R8-secondary-source/1.0'})
  with urlopen(req,timeout=300) as src, open(part,'wb') as dst:
   while True:
    b=src.read(1024*1024)
    if not b: break
    dst.write(b)
  part.replace(out)
 sh,n=digest(out); exp=info.get('checksum',''); exp=exp.split(':',1)[1] if ':' in exp else exp
 import hashlib as _hashlib
 md=_hashlib.md5(open(out,'rb').read()).hexdigest()
 return {'SIMULATION_ID':'SXS:BBH:'+sid,'LEVEL':lev,'FILENAME':fname,'SOURCE_KEY':f'{lev}:{fname}','SOURCE_URL':info['link'],'SIZE_BYTES':n,'EXPECTED_SIZE_BYTES':info.get('size'),'SHA256':sh,'EXPECTED_MD5':exp,'OBSERVED_MD5':md,'STATUS':'PASS' if not exp or md.lower()==exp.lower() else 'HASH_FAIL'}
def main():
 jobs=[]; sims={}
 print('METADATA_STAGE=SEQUENTIAL_CACHE_SAFE',flush=True)
 for i,sid in enumerate(IDS,1):
  sim=sxs.load('SXS:BBH:'+sid,ignore_deprecation=True); lev=sim.location.split('/')[-1]; fs=sim.metadata.get('files',{}); sims[sid]=(sim,lev)
  for fn in FILES:
   key=f'{lev}:{fn}'
   if key in fs: jobs.append((sid,lev,fn,fs[key]))
   else: print('SOURCE_MISSING',sid,key,flush=True)
  print(f'METADATA_PROGRESS={i}/{len(IDS)} {sid} {lev}',flush=True)
 print(f'DOWNLOAD_JOBS={len(jobs)} WORKERS=16',flush=True)
 out=[]
 with ThreadPoolExecutor(max_workers=16,thread_name_prefix='r8-secondary') as pool:
  fs=[pool.submit(dl,j) for j in jobs]
  for i,f in enumerate(as_completed(fs),1):
   x=f.result(); out.append(x); print(f'DOWNLOAD_PROGRESS={i}/{len(jobs)} {x["SIMULATION_ID"]} {x["FILENAME"]} {x["STATUS"]}',flush=True)
 out.sort(key=lambda x:(x['SIMULATION_ID'],x['FILENAME']))
 with open(ARCH/'SOURCE_INDEX.csv','w',newline='',encoding='utf-8') as h:
  w=csv.DictWriter(h,fieldnames=sorted({k for r in out for k in r})); w.writeheader(); w.writerows(out)
 with open(ARCH/'SHA256_MANIFEST.txt','w',encoding='utf-8') as h:
  for r in out: h.write(f"{r['SHA256']}  {r['SIMULATION_ID'].replace(':','_')}/{r['FILENAME']}\n")
 (ARCH/'PROVENANCE.json').write_text(json.dumps({'cohort':IDS,'generated_utc':datetime.now(timezone.utc).isoformat(),'selection':'R8_SECONDARY_COHORT_SELECTION.md','records':out},indent=2),encoding='utf-8')
 print(f'ACQUISITION_STATUS={"PASS" if len(out)==80 and all(r["STATUS"]=="PASS" for r in out) else "REVIEW"} FILES={len(out)} HASH_PASS={sum(r["STATUS"]=="PASS" for r in out)}',flush=True)
if __name__=='__main__': main()
