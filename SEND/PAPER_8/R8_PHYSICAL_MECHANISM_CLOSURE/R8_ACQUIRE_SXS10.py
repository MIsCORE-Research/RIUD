import csv, hashlib, json, os, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
import sxs

ROOT = Path(__file__).resolve().parent
ARCH = ROOT / 'R8_EXTERNAL_NR_SOURCE_ARCHIVE'
IDS = ['0180','0513','0526','1144','1765','2092','2497','2499','2505','2506']
FILES = ['metadata.json','Horizons.h5','ExtraWaveforms.h5','Strain_N2.h5','Strain_N2.json']

def sha256_md5(path):
    h=hashlib.sha256(); m=hashlib.md5(); n=0
    with open(path,'rb') as f:
        while True:
            b=f.read(1024*1024)
            if not b: break
            h.update(b); m.update(b); n += len(b)
    return h.hexdigest(), m.hexdigest(), n

def download(url, out, expected_size=None):
    part = out.with_suffix(out.suffix+'.part')
    if part.exists(): part.unlink()
    req=Request(url, headers={'User-Agent':'MIsCORE-R8-source-acquisition/1.0'})
    with urlopen(req, timeout=120) as src, open(part,'wb') as dst:
        total=0; last=0; started=time.time()
        while True:
            b=src.read(1024*1024)
            if not b: break
            dst.write(b); total += len(b)
            now=time.time()
            if now-last>2:
                rate=total/max(now-started,1e-9)
                print(f'GLOBAL_PROGRESS=DOWNLOAD_BYTES:{total} EXPECTED:{expected_size} RATE_BPS:{rate:.0f}', flush=True)
                last=now
    part.replace(out)

def main():
    ARCH.mkdir(parents=True, exist_ok=True)
    rows=[]; prov=[]
    for ix, sid in enumerate(IDS,1):
        sim=sxs.load('SXS:BBH:'+sid, ignore_deprecation=True)
        level=sim.location.split('/')[-1]
        files=sim.metadata.get('files',{})
        event_dir=ARCH / sid
        event_dir.mkdir(exist_ok=True)
        print(f'GLOBAL_PROGRESS={ix}/{len(IDS)} CURRENT_SIMULATION={sid} CURRENT_SOURCE=SXS', flush=True)
        for fname in FILES:
            key=f'{level}:{fname}'
            if key not in files:
                rows.append({'SIMULATION_ID':'SXS:BBH:'+sid,'LEVEL':level,'FILENAME':fname,'STATUS':'SOURCE_MISSING','SOURCE_KEY':key})
                continue
            info=files[key]; url=info['link']; expected=info.get('size'); checksum=info.get('checksum','')
            out=event_dir/fname
            if not out.exists() or (expected is not None and out.stat().st_size != expected):
                print(f'CURRENT_DOWNLOAD_OR_TEST=DOWNLOAD {sid} {key}', flush=True)
                download(url,out,expected)
            sh, md, size=sha256_md5(out)
            mdexp=checksum.split(':',1)[1] if ':' in checksum else checksum
            status='HASH_PASS' if (not mdexp or md.lower()==mdexp.lower()) else 'HASH_FAIL'
            row={'SIMULATION_ID':'SXS:BBH:'+sid,'LEVEL':level,'FILENAME':fname,'SOURCE_KEY':key,
                 'SOURCE_URL_OR_IDENTIFIER':url,'DOWNLOAD_DATE':datetime.now(timezone.utc).isoformat(),
                 'ORIGINAL_FILENAME':fname,'SIZE_BYTES':size,'EXPECTED_SIZE_BYTES':expected,
                 'MD5_EXPECTED':mdexp,'MD5_OBSERVED':md,'SHA256':sh,'STATUS':status,
                 'TIME_COORDINATE':'SXS source-native dimensionless simulation time',
                 'EXTRACTION_LEVEL':'raw public file','RESOLUTION_LEVEL':level,
                 'PROVENANCE_STATUS':status,'DOI':sim.metadata.get('doi','')}
            rows.append(row); prov.append(row)
    with open(ROOT/'R8_EXTERNAL_NR_SOURCE_ARCHIVE'/'SOURCE_INDEX.csv','w',newline='',encoding='utf-8') as f:
        cols=sorted({k for r in rows for k in r}); w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
    with open(ROOT/'R8_EXTERNAL_NR_SOURCE_ARCHIVE'/'DOWNLOAD_PROVENANCE.json','w',encoding='utf-8') as f:
        json.dump({'generated_utc':datetime.now(timezone.utc).isoformat(),'cohort':IDS,'records':prov},f,indent=2)
    with open(ROOT/'R8_EXTERNAL_NR_SOURCE_ARCHIVE'/'LICENSE_OR_ACCESS_NOTE.md','w',encoding='utf-8') as f:
        f.write('# R8 external NR source archive\n\nOriginal public SXS files are preserved unchanged. Sources are identified by the SXS simulation ID, resolution-level file key, public link, expected MD5, observed MD5, and SHA256. Derived tables are stored outside this archive.\n')
    with open(ROOT/'R8_EXTERNAL_NR_SOURCE_ARCHIVE'/'SHA256_MANIFEST.txt','w',encoding='utf-8') as f:
        for r in prov: f.write(f"{r['SHA256']}  {r['SIMULATION_ID'].replace(':','_')}/{r['FILENAME']}\n")
    print('R8_ACQUISITION_STATUS=PASS' if all(r.get('STATUS')=='HASH_PASS' for r in prov) else 'R8_ACQUISITION_STATUS=REVIEW')
    print(f'FILES_ACQUIRED={len(prov)}')
    print(f'FILES_HASH_PASS={sum(r.get("STATUS")=="HASH_PASS" for r in prov)}')

if __name__=='__main__': main()
