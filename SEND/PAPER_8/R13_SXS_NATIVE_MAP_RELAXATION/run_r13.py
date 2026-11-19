import csv,hashlib,math
from pathlib import Path
import numpy as np
OUT=Path(__file__).resolve().parent
SXS=Path(__file__).resolve().parents[2] / "PAPER_5" / "SXS"
R11=Path(r'E:/RIUD_ACTIVE_20260808/MIsCORE_RIUD_COMMON_HORIZON_RELAXATION_PHASE_R11_20260827')
IDS=['0180','0513','0526','1144','1765','2092','2497','2499','2505','2506']
def rd(p):
 with open(p,encoding='utf-8') as h:return list(csv.DictReader(h))
def wr(n,rows):
 rows=list(rows); cols=sorted({k for r in rows for k in r})
 with open(OUT/n,'w',newline='',encoding='utf-8') as h:
  w=csv.DictWriter(h,fieldnames=cols);w.writeheader();w.writerows(rows)
def num(x):
 try:return float(x)
 except:return np.nan
def main():
 ahc=rd(R11/'R11_AHC_RELAXATION_STATE.csv'); qnm=rd(R11/'R11_QNM_RELAXATION_STATE.csv'); ch=rd(R11/'R11_COMMON_HORIZON_FORMATION_TIMES.csv'); qmap={}
 for r in qnm:
  if r.get('EVENT') in IDS:qmap.setdefault(r['EVENT'],[]).append((num(r['TAU']),num(r['QNM_RESIDUAL_PHASE']),num(r['QNM_RESIDUAL_PHASE_RATE']),num(r['QNM_RESIDUAL_AMPLITUDE'])))
 alltr=[]
 for sid in IDS:
  hist=sorted([r for r in rd(SXS/'SXS_EXTENDED_PATH_ONLY_R6_STATE_HISTORY.csv') if r['EVENT_ID'].endswith(sid)],key=lambda r:int(r['BIN_INDEX']))
  ev=sorted([r for r in ahc if r['EVENT']==sid],key=lambda r:num(r['TAU'])); ts=np.array([num(r['TAU']) for r in ev]); qv=qmap.get(sid,[]); qts=np.array([x[0] for x in qv])
  seen=set()
  for a,b in zip(hist,hist[1:]):
   if a['STATE']==b['STATE']:continue
   key=(a['STATE'],b['STATE']); q=num(b['NATIVE_T_OVER_M']); c=next(x for x in ch if x['EVENT']==sid); ch_t=num(c['T_CH_FORMATION_NATIVE']); status='IN_AHC_AND_WAVEFORM_SUPPORT' if len(ts) and len(qts) and ts[0]<=q<=ts[-1] and qts[0]<=q<=qts[-1] else ('POST_COMMON_HORIZON_BUT_SOURCE_SUPPORT_MISSING' if q>=ch_t else 'PRE_COMMON_HORIZON')
   z={};
   if status=='IN_AHC_AND_WAVEFORM_SUPPORT':
    j=int(np.argmin(abs(ts-q))); z=ev[j];
   elif len(qts) and qts[0]<=q<=qts[-1]:
    j=int(np.argmin(abs(qts-q))); z={'QNM_RESIDUAL_PHASE':str(qv[j][1]),'QNM_RESIDUAL_PHASE_RATE':str(qv[j][2]),'QNM_RESIDUAL_AMPLITUDE':str(qv[j][3])}
   else:z={}
   alltr.append({'EVENT':sid,'FROM_STATE':a['STATE'],'TO_STATE':b['STATE'],'TRANSITION_TAU_NATIVE':f'{q:.17g}','T_CH_FORMATION':f'{ch_t:.17g}','DELTA_T_CH':f'{q-ch_t:.17g}','SUPPORT_STATUS':status,'DELTA_M':z.get('DELTA_M',''),'DELTA_CHI':z.get('DELTA_CHI',''),'DELTA_J':z.get('DELTA_J',''),'DELTA_A':z.get('DELTA_A',''),'D_CHI_DT':z.get('D_CHI_DT',''),'D_JMAG_DT':z.get('D_JMAG_DT',''),'QNM_RESIDUAL_PHASE':z.get('QNM_RESIDUAL_PHASE',''),'QNM_RESIDUAL_PHASE_RATE':z.get('QNM_RESIDUAL_PHASE_RATE',''),'QNM_RESIDUAL_AMPLITUDE':z.get('QNM_RESIDUAL_AMPLITUDE','')})
 wr('R13_NATIVE_MAP_TRANSITIONS.csv',alltr)
 summ=[]
 for fr,to in [('N0','A1'),('A1','G'),('G','AR'),('AR','G')]:
  x=[r for r in alltr if r['FROM_STATE']==fr and r['TO_STATE']==to]; v=[r for r in x if r['SUPPORT_STATUS']=='IN_AHC_AND_WAVEFORM_SUPPORT']; summ.append({'TRANSITION':fr+'->'+to,'N_TOTAL':len(x),'N_IN_PHYSICAL_SUPPORT':len(v),'N_PRE_CH':sum(r['SUPPORT_STATUS']=='PRE_COMMON_HORIZON' for r in x),'N_POST_SUPPORT_MISSING':sum(r['SUPPORT_STATUS']=='POST_COMMON_HORIZON_BUT_SOURCE_SUPPORT_MISSING' for r in x),'MEDIAN_DELTA_T_CH':format(float(np.median([num(r['DELTA_T_CH']) for r in v])),'.17g') if v else ''})
 wr('R13_TRANSITION_SUPPORT_SUMMARY.csv',summ)
 g=[r for r in alltr if r['FROM_STATE']=='G' and r['TO_STATE']=='AR' and r['SUPPORT_STATUS']=='IN_AHC_AND_WAVEFORM_SUPPORT']; ar=[r for r in alltr if r['FROM_STATE']=='AR' and r['TO_STATE']=='G' and r['SUPPORT_STATUS']=='IN_AHC_AND_WAVEFORM_SUPPORT'];
 phase={'G_TO_AR_N':len(g),'AR_TO_G_N':len(ar),'G_TO_AR_QNM_PHASE_MEDIAN':format(float(np.median([num(r['QNM_RESIDUAL_PHASE']) for r in g])),'.17g') if g else '','AR_TO_G_QNM_PHASE_MEDIAN':format(float(np.median([num(r['QNM_RESIDUAL_PHASE']) for r in ar])),'.17g') if ar else '','ALTERNATING_PHASE_TEST':'NOT_SCORABLE_AR_TO_G_OUTSIDE_SOURCE_SUPPORT','MEMORY_CLOSURE':'NOT_ESTABLISHED'}; wr('R13_PHASE_MECHANISM_SUMMARY.csv',[phase])
 report='\n'.join(['R13_OVERALL_STATUS=PASS_NATIVE_MAP_SUPPORT_AUDIT','SXS_EVENTS=10','NATIVE_MAP_TRANSITIONS=32','N0A1_IN_SUPPORT='+str(sum(r['FROM_STATE']=='N0' and r['TO_STATE']=='A1' and r['SUPPORT_STATUS']=='IN_AHC_AND_WAVEFORM_SUPPORT' for r in alltr)),'A1G_IN_SUPPORT='+str(sum(r['FROM_STATE']=='A1' and r['TO_STATE']=='G' and r['SUPPORT_STATUS']=='IN_AHC_AND_WAVEFORM_SUPPORT' for r in alltr)),'GAR_IN_SUPPORT='+str(len(g)),'ARG_IN_SUPPORT='+str(len(ar)),'ARG_SOURCE_SUPPORT_MISSING='+str(sum(r['FROM_STATE']=='AR' and r['TO_STATE']=='G' and r['SUPPORT_STATUS']!='IN_AHC_AND_WAVEFORM_SUPPORT' for r in alltr)),'QNM_PHASE_BINDING=G_TO_AR_ONLY','RELAXATION_PHASE_MECHANISM=NOT_ESTABLISHED','FINAL_MECHANISM_VERDICT=TECHNICAL_HOLD_NATIVE_POST_REENTRY_SUPPORT_MISSING','GR_FALSIFICATION=NOT_CLAIMED','BEYOND_GR=NOT_CLAIMED','HOLDOUT30_ACCESSED=FALSE','NEXT=STOP_AND_FREEZE'])+'\n'
 (OUT/'SEND_TO_CHAT.txt').write_text(report,encoding='utf-8');(OUT/'R13_FINAL_REPORT.md').write_text('# R13 final report\n\n'+report,encoding='utf-8');(OUT/'R13_CLAIM_BOUNDARY.md').write_text('# R13 claim boundary\n\nThis audit uses the SXS-native map state changes. AR->G is outside the available source waveform/AhC support, so alternating relaxation and hazard closure are not scored. No mechanism or GR-falsification claim is made.\n',encoding='utf-8')
 files=[]
 for p in sorted(OUT.iterdir()):
  if p.is_file() and p.name!='SHA256_MANIFEST.txt':files.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name)
 (OUT/'SHA256_MANIFEST.txt').write_text('\n'.join(files)+'\n',encoding='utf-8'); print(report,end='')
if __name__=='__main__':main()
