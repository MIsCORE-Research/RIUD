from pathlib import Path
import csv,json,hashlib
import numpy as np,h5py
from scipy.signal import stft

ROOT=Path(__file__).resolve().parent
BIND=ROOT/'MIsCORE_FULL99_RAW_SOURCE_BINDING_AUDIT_R0_20260828'/'FULL99_RAW_SOURCE_BINDING.csv'
GAP=ROOT/'RIUD_GAP_RAW_POSITION_FULL_CORRECTED_TIME_AUDIT_R2_20260821'/'GAP_RAW_POSITION_FULL_CORRECTED_TIME_EVENT_TABLE.csv'
OUT=ROOT/'MIsCORE_RAW_EVENTWISE_FULL_TF_CHANGE_R1_20260828';OUT.mkdir(parents=True,exist_ok=True)
FS=4096.;NP=64;HOP=4;FMIN=20.;FMAX=2000.;LO=-.1;HI=.1;CENT=np.arange(LO,HI+1e-9,.001);WIDTHS=(.005,.010,.020)
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def robust(x):
 x=np.asarray(x,float);med=np.nanmedian(x);mad=np.nanmedian(np.abs(x-med))*1.4826
 return (x-med)/(mad if mad>1e-12 else (np.nanstd(x) or 1.0))
def load(p):
 with h5py.File(p,'r') as h:x=np.asarray(h['strain']['Strain'],float)
 x=x-np.nanmedian(x);t=np.arange(x.size)/FS-2.
 f,tt,z=stft(x,fs=FS,window='hann',nperseg=NP,noverlap=NP-HOP,boundary=None,padded=False);q=(f>=FMIN)&(f<=FMAX);f=f[q];z=z[q]
 pz=np.vstack([robust(np.log(np.abs(row)**2+1e-30)) for row in z])
 power=np.nanmedian(pz,axis=0)
 ph=np.unwrap(np.angle(z),axis=1);pm=np.nanmedian(np.abs(np.diff(ph,axis=1)),axis=0);pm=np.r_[pm[0],pm]
 wt=np.maximum(pz-np.nanpercentile(pz,20,axis=1)[:,None],0)+1e-6;cent=np.sum(wt*f[:,None],axis=0)/np.sum(wt,axis=0);slope=np.gradient(cent,tt)
 return tt-2.,power,robust(pm),robust(slope)
def avg(t,x,a,b):
 q=(t>=a)&(t<b);v=x[q]
 return float(np.nanmean(v)) if v.size and np.isfinite(v).any() else np.nan
with open(BIND,encoding='utf-8-sig') as f:bind=list(csv.DictReader(f))
rows=[];curves=[];errors=[]
# PHASE 1: eventwise selection. No GAP/MT/t0 distance/population statistic is read here.
for r in bind:
 try:
  for det,path in [('H1',r['H1_PATH']),('L1',r['L1_PATH'])]:
   pp=Path(path);pp=pp if pp.is_absolute() else ROOT/pp;t,power,phase,slope=load(pp)
   for w in WIDTHS:
    valid=CENT[(CENT-w>=LO)&(CENT+w<=HI)];vals=[]
    for c in valid:
     vals.append(abs(avg(t,power,c-w,c)-avg(t,power,c,c+w))+abs(avg(t,phase,c-w,c)-avg(t,phase,c,c+w))+abs(avg(t,slope,c-w,c)-avg(t,slope,c,c+w)))
    vals=np.asarray(vals);i=int(np.nanargmax(vals));rows.append({'EVENT':r['EVENT'],'DETECTOR':det,'WIDTH_MS':w*1000,'PEAK_MS':valid[i]*1000,'C_MAX':vals[i],'N_VALID_CENTERS':len(valid),'INTERIOR':True,'SELECTION_PHASE':'FROZEN_BEFORE_GAP_JOIN'})
    for c,v in zip(valid,vals):curves.append({'EVENT':r['EVENT'],'DETECTOR':det,'WIDTH_MS':w*1000,'CENTER_MS':c*1000,'C':v})
 except Exception as e:errors.append({'EVENT':r['EVENT'],'ERROR':repr(e)})
def write(n,data,fields):
 with open(OUT/n,'w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
write('EVENTWISE_H1_L1_C_LANDMARKS.csv',rows,list(rows[0]) if rows else ['EVENT','ERROR']);write('EVENTWISE_C_CURVES.csv',curves,list(curves[0]) if curves else ['EVENT','ERROR']);write('ERRORS.csv',errors,['EVENT','ERROR'])
# PHASE 2: only now evaluate against the authoritative corrected GAP_CENTER table.
g=[]
with open(GAP,encoding='utf-8-sig') as f:
 for r in csv.DictReader(f):
  if r.get('MAP_OBJECT')=='GAP_CENTER':
   try:g.append((r['EVENT_ID'],float(r['NATIVE_TAU'])*1000.))
   except:pass
gm={e:t for e,t in g};evals=[]
for r in rows:
 if r['EVENT'] in gm:
  z=dict(r);z.update({'GAP_CENTER_NATIVE_TAU_MS':gm[r['EVENT']],'TIMING_ERROR_MS':float(r['PEAK_MS'])-gm[r['EVENT']],'EVALUATION_PHASE':'POST_SELECTION_JOIN'});evals.append(z)
write('EVENTWISE_GAP_TIMING_EVALUATION.csv',evals,list(evals[0]) if evals else list(rows[0])+['GAP_CENTER_NATIVE_TAU_MS','TIMING_ERROR_MS','EVALUATION_PHASE'])
summary={'BRANCH':'MIsCORE_RAW_EVENTWISE_FULL_TF_CHANGE_R1_20260828','N_EVENTS_INPUT':len(bind),'N_EVENT_DETECTOR_ROWS':len(rows),'N_ERRORS':len(errors),'DETECTORS':['H1','L1'],'WIDTHS_MS':[5,10,20],'SUPPORT_MS':'[-100,+100]','CENTER_STEP_MS':1,'FREQUENCY_BAND_HZ':'20..2000','C_DEFINITION':'sum of absolute left/right flank changes in robust power, phase-motion, and frequency-slope summaries','SELECTION_EVENTWISE_ONLY':True,'POPULATION_AVERAGING_FOR_SELECTION':False,'T0_DISTANCE_FOR_SELECTION':False,'GAP_MT_NODE_PATH_USED_FOR_SELECTION':False,'GAP_JOIN_AFTER_FREEZE':True,'GAP_CENTER_JOIN_N':len(evals),'HISTORICAL_GAP_USED_FOR_SELECTION':False,'HISTORICAL_MT_USED_FOR_SELECTION':False,'HOLDOUT30_ACCESSED':False,'NO_FIT':True,'NO_THRESHOLD':True}
if evals:
 for det in ['H1','L1']:
  for w in WIDTHS:
   z=[float(x['TIMING_ERROR_MS']) for x in evals if x['DETECTOR']==det and float(x['WIDTH_MS'])==w*1000];summary[f'{det}_W{int(w*1000)}_N']=len(z);summary[f'{det}_W{int(w*1000)}_MEDIAN_ABS_ERROR_MS']=float(np.median(np.abs(z))) if z else None;summary[f'{det}_W{int(w*1000)}_MAE_MS']=float(np.mean(np.abs(z))) if z else None
(OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
(OUT/'METHODS.md').write_text('# Eventwise full-TF structural-change landmarks\n\nH1 and L1 are scored separately. For each event and detector, C(t) is the sum of absolute left/right flank changes in robust power, phase-motion, and frequency-slope summaries over 20-2000 Hz. The strongest complete-support interior point is frozen per event/detector/width. Population averaging, t0-distance, GAP, MT, and node/path are excluded from selection. Only after selection is frozen, the corrected GAP_CENTER NATIVE_TAU table is joined for timing-error evaluation.\n',encoding='utf-8')
man=[]
for p in sorted(OUT.iterdir()):
 if p.is_file() and p.name!='SHA256_MANIFEST.txt':man.append(f'{sha(p)}  {p.name}')
(OUT/'SHA256_MANIFEST.txt').write_text('\n'.join(man)+'\n',encoding='utf-8')
print(json.dumps(summary,indent=2))
