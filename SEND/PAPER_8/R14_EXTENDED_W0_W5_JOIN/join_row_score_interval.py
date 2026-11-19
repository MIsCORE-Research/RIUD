import csv,json,hashlib
from pathlib import Path
SRC=Path(r'E:\RIUD_ACTIVE_20260808\MIsCORE_RIUD_EXTENDED_W0_W5_ROW_LEVEL_R12_20260827')
INT=Path(r'E:\RIUD_ACTIVE_20260808\MIsCORE_RIUD_EXTENDED_W0_W5_INTERVAL_COLOCATION_R13_20260827')
OUT=Path(__file__).resolve().parent
def read(p):
    with p.open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
rows=read(SRC/'EXTENDED_W0_W5_ROW_LEVEL_DLOG_LIK.csv')
ints=read(INT/'NODE_INTERVAL_COLOCATION.csv')
for r in rows:
    x=float(r['U_PCT']); cand=[i for i in ints if i['EVENT']==r['EVENT'] and float(i['PRE_PCT'])<x<=float(i['POST_PCT'])]
    if len(cand)!=1: raise RuntimeError(f'INTERVAL_KEY_NOT_UNIQUE:{r["EVENT"]}:{x}:{len(cand)}')
    i=cand[0]; r['INTERVAL_CLASS']=i['INTERVAL_CLASS'];r['PRE_NODE_INDEX']=i['PRE_NODE_INDEX'];r['POST_NODE_INDEX']=i['POST_NODE_INDEX'];r['STATE_CHANGE_COUNT']=i['STATE_CHANGE_COUNT'];r['FREQ_CHANGE_HZ']=i['FREQ_CHANGE_HZ'];r['WIDTH_CHANGE_S']=i['WIDTH_CHANGE_S'];r['STATE_CHANGES']=i['STATE_CHANGES']
OUT.mkdir(parents=True,exist_ok=True)
with (OUT/'ROW_SCORE_INTERVAL_JOIN.csv').open('w',newline='',encoding='utf-8') as f:
    fields=list(rows[0]);w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
groups=[]
for ev in sorted({r['EVENT'] for r in rows}):
  for cls in ['STATE_AND_PHENOTYPE','STATE_ONLY','PHENOTYPE_ONLY','NEITHER']:
    q=[r for r in rows if r['EVENT']==ev and r['INTERVAL_CLASS']==cls]
    groups.append({'EVENT':ev,'INTERVAL_CLASS':cls,'N_ROWS':len(q),'SUM_DLOG_LIK':sum(float(r['DLOG_LIK']) for r in q),'MEAN_DLOG_LIK':(sum(float(r['DLOG_LIK']) for r in q)/len(q) if q else ''),'POSITIVE_ROWS':sum(float(r['DLOG_LIK'])>0 for r in q),'NEGATIVE_ROWS':sum(float(r['DLOG_LIK'])<0 for r in q)})
with (OUT/'ROW_SCORE_INTERVAL_SUMMARY.csv').open('w',newline='',encoding='utf-8') as f:
 fields=list(groups[0]);w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(groups)
meta={'METHOD':'Exact join of R12 frozen row-level DLOG_LIK to R13 adjacent-node interval by EVENT and PRE_PCT < U_PCT <= POST_PCT. No refit, new law, threshold, or GAP-based selection.','ROWS':len(rows),'INTERVALS':len(ints),'JOIN_FAILURES':0}
(OUT/'METHODS.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
(OUT/'REPORT.md').write_text('# W0-W5 row score to node-interval mechanism join\n\n'+json.dumps(meta,indent=2)+'\n\nThis is descriptive and does not establish causality.',encoding='utf-8')
lines=[]
for p in sorted(OUT.iterdir()):
 if p.name!='SHA256_MANIFEST.txt' and p.is_file():lines.append(f'{p.name}  {hashlib.sha256(p.read_bytes()).hexdigest().upper()}')
(OUT/'SHA256_MANIFEST.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('R_STATUS=PASS');print('ROWS='+str(len(rows)));print('INTERVALS='+str(len(ints)));print('RESULT_DIR='+str(OUT))
