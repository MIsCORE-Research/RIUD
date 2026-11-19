import csv, json, os, importlib.util
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
ARCH=ROOT/'R8_SECONDARY_NR_SOURCE_ARCHIVE'
OUT=ROOT/'R8_SECONDARY_REPLAY'
IDS='0001 0003 0154 0153 0006 0009 0339 0179 0030 0045 0261 0260 0054 0031 1160 0165'.split()
LEVELS={'0001':5,'0003':5,'0154':4,'0153':4,'0006':5,'0009':5,'0339':3,'0179':4,'0030':5,'0045':5,'0261':5,'0260':5,'0054':5,'0031':5,'1160':3,'0165':3}

def loadmod(name,path):
 s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def main():
 OUT.mkdir(parents=True,exist_ok=True); (OUT/'waveforms').mkdir(exist_ok=True)
 panel=[]; hs=[]
 for sid in IDS:
  m=json.loads((ARCH/sid/'metadata.json').read_text(encoding='utf-8'))
  masses=[float(m['initial_mass1']),float(m['initial_mass2'])]; spins=[m['initial_dimensionless_spin1'],m['initial_dimensionless_spin2']]
  hi=int(max(range(2),key=lambda i:masses[i])); lo=1-hi
  row={'CATEGORY_INDEX':'','CATEGORY_NAME':'SECONDARY_METADATA_STRATUM','SXS_ID':'SXS:BBH:'+sid,'LEV':str(LEVELS[sid]),'Q':str(m.get('reference_mass_ratio',m.get('initial_mass_ratio',''))),'ECCENTRICITY':str(m.get('reference_eccentricity','')),'M_HEAVY':str(masses[hi]),'M_LIGHT':str(masses[lo])}
  for prefix,i in [('H',hi),('L',lo)]:
   for ax,j in zip('XYZ',range(3)): row['CHI_'+prefix+'_'+ax]=str(float(spins[i][j]))
  panel.append(row)
  rv=m['remnant_dimensionless_spin']; hs.append({'SXS_ID':'SXS:BBH:'+sid,'CATEGORY':'SECONDARY_METADATA_STRATUM','AHC_FINAL_CHRISTODOULOUS_MASS':str(m['remnant_mass']),'AHC_FINAL_SPIN_MAG':str(float(np.linalg.norm(np.asarray(rv,float))))})
 with open(OUT/'SXS_SECONDARY_PANEL.csv','w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(panel[0])); w.writeheader(); w.writerows(panel)
 with open(OUT/'SXS_SECONDARY_HORIZON_SUMMARY.csv','w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(hs[0])); w.writeheader(); w.writerows(hs)
 replay=loadmod('sxs_secondary_replay',str(Path(__file__).resolve().parents[2] / "PAPER_5" / "PRODUCTION_CODE" / "run_sxs_native_replay.py"))
 replay.PANEL_ROOT=OUT; replay.PANEL=OUT/'SXS_SECONDARY_PANEL.csv'; replay.HORIZON_SUMMARY=OUT/'SXS_SECONDARY_HORIZON_SUMMARY.csv'; replay.OUT=OUT
 def fast_channel_map(t, x, centers_s):
  # Algebraically identical to the frozen implementation: vectorize only
  # the frequency accumulation; preserve centers, widths, normalization and
  # phase convention exactly.
  t=np.asarray(t,float); x=np.asarray(x,complex); centers_native=centers_s/replay.M_SEC; widths_native=replay.WIDTH_S/replay.M_SEC; freqs_native=replay.FREQ_HZ*replay.M_SEC
  all_centers=np.unique(np.round(np.concatenate([centers_s,(centers_s[:,None]+replay.LAG_S[None,:]).ravel()]),9)); out=np.zeros((len(all_centers),len(replay.FREQ_HZ),len(replay.WIDTH_S)),complex)
  for ci,cs in enumerate(all_centers):
   c=float(cs/replay.M_SEC)
   for wi,width in enumerate(widths_native):
    sigma=max(float(width)/2.355,float(np.median(np.diff(t)))); g=np.exp(-0.5*((t-c)/sigma)**2); denom=np.sqrt(float(np.sum(g*g)))+replay.EPS
    phase=np.exp(-2j*np.pi*(t-c)[:,None]*freqs_native[None,:])
    out[ci,:,wi]=(np.sum((x*g)[:,None]*phase,axis=0)/denom)
  return all_centers,out
 replay.channel_map=fast_channel_map
 def requested_map(t,x,centers_s):
  t=np.asarray(t,float); x=np.asarray(x,complex); out=np.zeros((len(centers_s),len(replay.FREQ_HZ),len(replay.WIDTH_S)),complex); fn=replay.FREQ_HZ*replay.M_SEC; wn=replay.WIDTH_S/replay.M_SEC; dt=float(np.median(np.diff(t)))
  for ci,cs in enumerate(centers_s):
   c=float(cs/replay.M_SEC)
   for wi,width in enumerate(wn):
    sigma=max(float(width)/2.355,dt); g=np.exp(-0.5*((t-c)/sigma)**2); phase=np.exp(-2j*np.pi*(t-c)[:,None]*fn[None,:]); out[ci,:,wi]=np.sum((x*g)[:,None]*phase,axis=0)/(np.sqrt(float(np.sum(g*g)))+replay.EPS)
  return out
 def fast_source_state(t,q0,q1):
  allc=np.unique(np.round(np.concatenate([replay.CENTER_S,(replay.CENTER_S[:,None]+replay.LAG_S[None,:]).ravel()]),9)); m0=requested_map(t,q0,replay.CENTER_S); m1=requested_map(t,q1,allc); idx={round(float(x),9):i for i,x in enumerate(allc)}
  score=np.full((len(replay.CENTER_S),len(replay.FREQ_HZ),len(replay.WIDTH_S)),-np.inf,float); cl=np.zeros_like(score); cm=np.empty(score.shape,dtype=object)
  for ci,c in enumerate(replay.CENTER_S):
   for fi in range(len(replay.FREQ_HZ)):
    for wi in range(len(replay.WIDTH_S)):
     best=(-np.inf,0.0,''); a=m0[ci,fi,wi]
     for lag in replay.LAG_S:
      b=m1[idx[round(float(c+lag),9)],fi,wi]; bal=min(abs(a),abs(b))/(max(abs(a),abs(b))+replay.EPS)
      for md in replay.MODES:
       val=abs(a+(1.0 if md=='same' else -1.0)*b)/np.sqrt(2.0)*bal
       if val>best[0]: best=(float(val),float(lag),md)
     score[ci,fi,wi]=best[0]; cl[ci,fi,wi]=best[1]; cm[ci,fi,wi]=best[2]
  null=np.stack([np.roll(score,int((b*7)%len(replay.CENTER_S)),axis=0) for b in range(replay.NULL_N)],axis=0); mean=np.mean(null,axis=0); std=np.std(null,axis=0,ddof=0); positive=std[np.isfinite(std)&(std>0)]; floor=max(float(np.quantile(positive,.05)) if len(positive) else 1e-6,1e-6); state=((score-mean)/np.maximum(std,floor)).astype(np.float32)
  return state,score,cl,cm,floor
 replay.source_state=fast_source_state
 def secondary_run_event(row, horizons, coord, rule):
  sid=row['SXS_ID']; short=sid.split(':')[-1]; source=ARCH/short/'Strain_N2.h5'
  t,q0,q1,meta=replay.load_mode(source); state,score,lag,mode,floor=replay.source_state(t,q0,q1)
  res=rule.search_hypergrid(state,replay.CENTER_S,replay.FREQ_HZ,replay.WIDTH_S,rule.SCENARIOS[0],return_path=True)
  t_i=np.asarray(res.get('candidate_t_i',[]),int); f_i=np.asarray(res.get('candidate_f_i',[]),int); w_i=np.asarray(res.get('candidate_w_i',[]),int); pidx=[int(x) for x in res.get('path_node_indices',[])]
  path_freq=[float(replay.FREQ_HZ[f_i[j]]) for j in pidx] if len(f_i) else []; path_tau=[float(replay.CENTER_S[t_i[j]]) for j in pidx] if len(t_i) else []
  inc=sum(b>a for a,b in zip(path_freq,path_freq[1:])); dec=sum(b<a for a,b in zip(path_freq,path_freq[1:]))
  R,chi_a,S=replay.physical_s(row,horizons[sid],coord); direction='UP' if replay.GAMMA*S>0 else ('DOWN' if replay.GAMMA*S<0 else 'NEUTRAL')
  result={'SXS_ID':sid,'CATEGORY':row['CATEGORY_NAME'],'SOURCE_SHA256':replay.sha256(source),'N_TIME':meta['N_TIME'],'N_MODES':meta['N_MODES'],'SOURCE_TIME_UNIT':'M','SOURCE_CHANNELS':'Re(h22),Im(h22)','SOURCE_PEAK_ORIGIN':'argmax(abs(h22))','NODE_STATUS':'PATH_FOUND' if res.get('status')=='PATH_FOUND' else 'NO_PATH','CANDIDATE_COUNT':int(res.get('candidate_count',0)),'PATH_NODE_COUNT':int(res.get('path_nodes',0)),'PATH_SCORE':float(res.get('score',0.0)),'PATH_TAU_START_S':path_tau[0] if path_tau else '','PATH_TAU_END_S':path_tau[-1] if path_tau else '','PATH_FREQUENCY_INCREASES':inc,'PATH_FREQUENCY_DECREASES':dec,'INTRINSIC_ORDERING':'INCREASING' if inc>dec else ('DECREASING' if dec>inc else 'MIXED_OR_EMPTY'),'R_MIRR_RATIO':R,'CHI_A_NORMALIZED':chi_a,'S_FROZEN':S,'GAMMA_S':replay.GAMMA*S,'S_RATE_DIRECTION':direction,'SOURCE_NULL200':'CIRCULAR_CENTER_SHIFT_200','ROBUST_SCALE_FLOOR':floor,'OBSERVED_TOPOLOGY':'NOT_ESTABLISHED_FROM_SINGLE_SOURCE_PATH'}
  nodes=[]; pathset=set(pidx); cz=np.asarray(res.get('candidate_z',[]),float); cp=np.asarray(res.get('candidate_persistence',[]),int)
  for j in range(len(t_i)): nodes.append({'SXS_ID':sid,'CENTER_S':replay.CENTER_S[t_i[j]],'FREQUENCY_AXIS':replay.FREQ_HZ[f_i[j]],'WIDTH_S':replay.WIDTH_S[w_i[j]],'STATE_Z':cz[j],'WIDTH_PERSISTENCE':cp[j],'IS_PATH_NODE':int(j in pathset)})
  with open(OUT/(short+'_NODES.csv'),'w',newline='',encoding='utf-8') as h:
   w=csv.DictWriter(h,fieldnames=['SXS_ID','CENTER_S','FREQUENCY_AXIS','WIDTH_S','STATE_Z','WIDTH_PERSISTENCE','IS_PATH_NODE']); w.writeheader(); w.writerows(nodes)
  with open(OUT/(short+'_PATH.csv'),'w',newline='',encoding='utf-8') as h:
   w=csv.DictWriter(h,fieldnames=['SXS_ID','PATH_INDEX','CENTER_S','FREQUENCY_AXIS','WIDTH_S']); w.writeheader();
   for k,j in enumerate(pidx): w.writerow({'SXS_ID':sid,'PATH_INDEX':k,'CENTER_S':replay.CENTER_S[t_i[j]],'FREQUENCY_AXIS':replay.FREQ_HZ[f_i[j]],'WIDTH_S':replay.WIDTH_S[w_i[j]]})
  return result
 replay.run_event=secondary_run_event
 replay.main()
 topo=loadmod('sxs_secondary_topology',str(Path(r'E:/RIUD_ACTIVE_20260808/RIUD_SXS_NATIVE_RIUD_REPLAY_SYM_0P3S_R0_20260823/apply_frozen_r6_topology_sxs_extended.py')))
 topo.ROOT=OUT; topo.main()
 closure=loadmod('sxs_secondary_closure',str(ROOT/'R8_MECHANISM_CLOSURE_TEST.py'))
 closure.ROOT=OUT; closure.ARCH=ARCH; closure.SXSROOT=OUT; closure.STATEFILE=OUT/'SXS_EXTENDED_PATH_ONLY_R6_STATE_HISTORY.csv'; closure.IDS=IDS
 closure.main()
 print('SECONDARY_R8_COMPLETE=TRUE')
if __name__=='__main__': main()
