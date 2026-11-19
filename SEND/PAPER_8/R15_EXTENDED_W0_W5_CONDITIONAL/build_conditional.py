import csv,json,hashlib
from pathlib import Path
SRC=Path(__file__).resolve().parent.parent / "R14_EXTENDED_W0_W5_JOIN" / "ROW_SCORE_INTERVAL_JOIN.csv"
OUT=Path(__file__).resolve().parent
with SRC.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
out=[]
for ev in sorted({r['EVENT'] for r in rows}):
 for cls in ['STATE_AND_PHENOTYPE','STATE_ONLY','PHENOTYPE_ONLY','NEITHER']:
  for typ in ['01','1G','GR','RG']:
   q=[r for r in rows if r['EVENT']==ev and r['INTERVAL_CLASS']==cls and r['TRANSITION_TYPE']==typ]
   vals=[float(r['DLOG_LIK']) for r in q]
   out.append({'EVENT':ev,'INTERVAL_CLASS':cls,'TRANSITION_TYPE':typ,'N_ROWS':len(q),'SUM_DLOG_LIK':sum(vals),'MEAN_DLOG_LIK':sum(vals)/len(vals) if vals else '','POSITIVE_ROWS':sum(x>0 for x in vals),'NEGATIVE_ROWS':sum(x<0 for x in vals)})
OUT.mkdir(parents=True,exist_ok=True)
with (OUT/'CONDITIONAL_MECHANISM_SUMMARY.csv').open('w',newline='',encoding='utf-8') as f:
 fields=list(out[0]);w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
meta={'SOURCE':str(SRC),'NO_REFIT':True,'NO_NEW_LAW':True,'INTERPRETATION':'Conditional descriptive decomposition; interval labels inherited from R13 and row scores from R12/R14.'}
(OUT/'METHODS.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
(OUT/'REPORT.md').write_text('# Conditional mechanism decomposition\n\n'+json.dumps(meta,indent=2)+'\n\nDescriptive only; no microscopic causality is established.',encoding='utf-8')
lines=[]
for p in sorted(OUT.iterdir()):
 if p.name!='SHA256_MANIFEST.txt' and p.is_file():lines.append(f'{p.name}  {hashlib.sha256(p.read_bytes()).hexdigest().upper()}')
(OUT/'SHA256_MANIFEST.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('R_STATUS=PASS');print('RESULT_DIR='+str(OUT))
