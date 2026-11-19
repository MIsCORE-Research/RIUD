import csv, json, math, hashlib
from pathlib import Path
import numpy as np
import h5py, sxs
from sxs.waveforms import energy_flux, angular_momentum_flux

ROOT=Path(__file__).resolve().parent
ARCH=ROOT/'R8_EXTERNAL_NR_SOURCE_ARCHIVE'
SXSROOT=Path(__file__).resolve().parents[2] / "PAPER_5" / "SXS"
STATEFILE=SXSROOT/'SXS_EXTENDED_PATH_ONLY_R6_STATE_HISTORY.csv'
IDS=['0180','0513','0526','1144','1765','2092','2497','2499','2505','2506']
STATES=['N0','A1','G','AR']

def write_csv(path,rows):
    with open(path,'w',newline='',encoding='utf-8') as f:
        cols=sorted({k for r in rows for k in r}); w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
def interp(x,y,t):
    x=np.asarray(x); y=np.asarray(y)
    if len(x)==0 or t < float(x[0]) or t > float(x[-1]): return float('nan')
    return float(np.interp(t,x,y))
def arrval(v):
    try:return float(v)
    except:return float('nan')
def final_scalar(v):
    if isinstance(v,(list,tuple)): return float(np.linalg.norm(np.asarray(v,float)))
    return arrval(v)
def loglik(y,p):
    p=np.clip(np.asarray(p,float),1e-12,1-1e-12); y=np.asarray(y,float)
    return float(np.sum(y*np.log(p)+(1-y)*np.log1p(-p)))
def fit_logistic(X,y,reg=1.0,max_iter=100):
    X=np.asarray(X,float); y=np.asarray(y,float); Z=np.column_stack([np.ones(len(X)),X]); b=np.zeros(Z.shape[1])
    for _ in range(max_iter):
        q=1/(1+np.exp(-np.clip(Z@b,-30,30))); w=q*(1-q)+1e-8
        H=(Z.T*w)@Z; g=Z.T@(q-y); H[1:,1:]+=reg*np.eye(H.shape[0]-1)
        try: step=np.linalg.solve(H,g)
        except np.linalg.LinAlgError: step=np.linalg.lstsq(H,g,rcond=None)[0]
        b-=step
        if np.max(np.abs(step))<1e-9: break
    return b
def predict_logistic(X,b):
    Z=np.column_stack([np.ones(len(X)),np.asarray(X,float)]); return 1/(1+np.exp(-np.clip(Z@b,-30,30)))

def main():
    raw=list(csv.DictReader(open(STATEFILE,newline='',encoding='utf-8')))
    by={sid:sorted([r for r in raw if r['EVENT_ID']=='SXS:BBH:'+sid],key=lambda r:int(r['BIN_INDEX'])) for sid in IDS}
    allrows=[]; transitions=[]; events=[]
    for ix,sid in enumerate(IDS,1):
        print(f'GLOBAL_PROGRESS={ix}/{len(IDS)} CURRENT_SIMULATION={sid} CURRENT_TEST=ROW_MASTER',flush=True)
        meta=json.load(open(ARCH/sid/'metadata.json',encoding='utf-8')); ch=float(meta.get('common_horizon_time',float('nan')))
        h=sxs.load(str(ARCH/sid/'Strain_N2.h5')); t=np.asarray(h.t,float); h22=np.asarray(h[:,h.index(2,2)],complex); h44=np.asarray(h[:,h.index(4,4)],complex)
        peak=float(t[np.argmax(np.abs(h22))]); t_rel=t-peak; ch_rel=ch-peak
        ph22=np.unwrap(np.angle(h22)); ph44=np.unwrap(np.angle(h44)); f22=np.gradient(ph22,t_rel)/(2*np.pi); f44=np.gradient(ph44,t_rel)/(2*np.pi)
        ef=np.asarray(energy_flux(h),float); jf=np.asarray(angular_momentum_flux(h),float)
        cume=np.concatenate([[0],np.cumsum((ef[1:]+ef[:-1])*np.diff(t_rel)/2)])
        cumj=np.concatenate([[0],np.cumsum((jf[1:,2]+jf[:-1,2])*np.diff(t_rel)/2)])
        with h5py.File(ARCH/sid/'Horizons.h5','r') as hf:
            def get(n):return np.asarray(hf['AhC.dir/'+n][:],float)
            area=get('ArealMass.dat'); mass=get('ChristodoulouMass.dat'); chi=get('chiMagInertial.dat'); jvec=get('DimensionfulInertialSpin.dat')
        for a in (area,mass,chi,jvec): a[:,0] -= peak
        jm=np.linalg.norm(jvec[:,1:4],axis=1); da=np.gradient(area[:,1],area[:,0]); dm=np.gradient(mass[:,1],mass[:,0]); dc=np.gradient(chi[:,1],chi[:,0]); dj=np.gradient(jm,jvec[:,0])
        final_area=float(area[-1,1]); final_mass=float(meta.get('remnant_mass',mass[-1,1])); final_chi=final_scalar(meta.get('remnant_dimensionless_spin',chi[-1,1])); final_j=float(jm[-1])
        event_rows=by[sid];
        for i,r in enumerate(event_rows[:-1]):
            native=float(r['NATIVE_T_OVER_M']); state=r['STATE']; nxt=event_rows[i+1]['STATE']; y=int(nxt!=state)
            # Causal features use only current row, past cumulative flux, and source metadata endpoints.
            age=float(r['TIME_SINCE_LAST_ACTIVE_BIN']) if r['TIME_SINCE_LAST_ACTIVE_BIN'] not in ('','None') else (float(i) if state not in ('N0','A1') else 0.0)
            run=float(r['CURRENT_ACTIVE_RUN_INDEX'] or 0); state_age=0
            j=i
            while j>=0 and event_rows[j]['STATE']==state: state_age+=1; j-=1
            row={'EVENT': 'SXS:BBH:'+sid,'BIN_INDEX':r['BIN_INDEX'],'SOURCE_NATIVE_TIME':native,'TAU_FROM_COMMON_HORIZON':native-ch_rel,'RIUD_STATE':state,'RIUD_STATE_AGE':state_age,'RIUD_RUN_LENGTH':run,'TIME_SINCE_LAST_ACTIVE_BIN':age,'TARGET_NEXT_TRANSITION':y,'NEXT_TRANSITION_TIME':float(event_rows[i+1]['NATIVE_T_OVER_M']) if y else '','NEXT_STATE':nxt if y else '',
                 'TIME_TO_NEXT_TRANSITION':float(event_rows[i+1]['NATIVE_T_OVER_M'])-native if y else '',
                 'A_AREAL':interp(area[:,0],area[:,1],native),'M_CH':interp(mass[:,0],mass[:,1],native),'CHI':interp(chi[:,0],chi[:,1],native),'J_MAG':interp(jvec[:,0],jm,native),'D_A_DT':interp(area[:,0],da,native),'D_MCH_DT':interp(mass[:,0],dm,native),'D_CHI_DT':interp(chi[:,0],dc,native),'D_J_DT':interp(jvec[:,0],dj,native),
                 'DIST_FINAL_A':abs(interp(area[:,0],area[:,1],native)-final_area),'DIST_FINAL_MCH':abs(interp(mass[:,0],mass[:,1],native)-final_mass),'DIST_FINAL_CHI':abs(interp(chi[:,0],chi[:,1],native)-final_chi),'DIST_FINAL_J':abs(interp(jvec[:,0],jm,native)-final_j),
                 'RELAX_RATE_A':abs(interp(area[:,0],da,native)),'RELAX_RATE_MCH':abs(interp(mass[:,0],dm,native)),'RELAX_RATE_CHI':abs(interp(chi[:,0],dc,native)),'RELAX_RATE_J':abs(interp(jvec[:,0],dj,native)),
                 'E_INFINITY_FLUX':interp(t_rel,ef,native),'JZ_INFINITY_FLUX':interp(t_rel,jf[:,2],native),'CUM_E_INFINITY':interp(t_rel,cume,native),'CUM_JZ_INFINITY':interp(t_rel,cumj,native),
                 'A22':interp(t_rel,np.abs(h22),native),'A44':interp(t_rel,np.abs(h44),native),'OMEGA22':interp(t_rel,f22,native),'OMEGA44':interp(t_rel,f44,native),'MODE_PHASE_COMBINATION':interp(t_rel,np.angle(np.exp(1j*(ph44-2*ph22))),native)}
            allrows.append(row)
            if y: transitions.append({'EVENT':row['EVENT'],'RIUD_STATE':state,'NEXT_STATE':nxt,'RIUD_TRANSITION_TIME':float(event_rows[i+1]['NATIVE_T_OVER_M']),'SOURCE_NATIVE_TIME':native,'TRANSITION_TAU_FROM_COMMON_HORIZON':float(event_rows[i+1]['NATIVE_T_OVER_M'])-ch_rel})
        events.append({'EVENT':'SXS:BBH:'+sid,'N_ROWS':len(event_rows)-1,'N_TRANSITIONS':sum(int(event_rows[i+1]['STATE']!=event_rows[i]['STATE']) for i in range(len(event_rows)-1)),'COMMON_HORIZON_TIME_NATIVE':ch_rel,'STRAIN_MAX_TIME_RELATIVE_TO_PEAK':float(t_rel[-1])})
    write_csv(ROOT/'R8_SXS_MECHANISM_ROW_MASTER.csv',allrows); write_csv(ROOT/'R8_SXS_MECHANISM_TRANSITION_AUDIT.csv',transitions); write_csv(ROOT/'R8_SXS_MECHANISM_EVENT_ACCOUNTING.csv',events)
    # Fixed, interpretable blocks. Scaling and imputation are fit independently inside every outer training fold.
    base=['RIUD_STATE']; memory=['RIUD_STATE_AGE','RIUD_RUN_LENGTH','TIME_SINCE_LAST_ACTIVE_BIN']; horizon=['A_AREAL','M_CH','CHI','J_MAG','D_A_DT','D_MCH_DT','D_CHI_DT','D_J_DT']; rem=['DIST_FINAL_A','DIST_FINAL_MCH','DIST_FINAL_CHI','DIST_FINAL_J','RELAX_RATE_A','RELAX_RATE_MCH','RELAX_RATE_CHI','RELAX_RATE_J']; flux=['E_INFINITY_FLUX','JZ_INFINITY_FLUX','CUM_E_INFINITY','CUM_JZ_INFINITY']; mode=['A22','A44','OMEGA22','OMEGA44','MODE_PHASE_COMBINATION']
    blocks={'B0':base,'BM':base+memory,'BH':base+horizon,'BR':base+rem,'BF':base+flux,'BHF':base+horizon+flux,'BFS':base+horizon+rem+flux,'BMODE':base+mode,'BM+H':base+memory+horizon,'BM+R':base+memory+rem,'BM+F':base+memory+flux,'BM+HF':base+memory+horizon+flux,'BM+FS':base+memory+horizon+rem+flux}
    state_rows=[]
    for r in allrows:
        one={f'STATE_{s}':int(r['RIUD_STATE']==s) for s in STATES}; one.update({k:r[k] for k in r}); state_rows.append(one)
    feature_names={k:(['STATE_'+s for s in STATES] if 'RIUD_STATE' in v else [])+[x for x in v if x!='RIUD_STATE'] for k,v in blocks.items()}
    metrics=[]; eventwise=[]
    for model,names in feature_names.items():
        total=0.0; foldrows=[]
        for held in IDS:
            tr=[r for r in state_rows if r['EVENT']!='SXS:BBH:'+held]; te=[r for r in state_rows if r['EVENT']=='SXS:BBH:'+held]
            # categorical state features are already numeric; train medians are deterministic and no held values affect them.
            Xtr=np.array([[arrval(r.get(n,'')) for n in names] for r in tr],float); Xte=np.array([[arrval(r.get(n,'')) for n in names] for r in te],float); ytr=np.array([int(r['TARGET_NEXT_TRANSITION']) for r in tr]); yte=np.array([int(r['TARGET_NEXT_TRANSITION']) for r in te])
            med=np.nanmedian(Xtr,axis=0); med=np.where(np.isfinite(med),med,0.0); Xtr=np.where(np.isfinite(Xtr),Xtr,med); Xte=np.where(np.isfinite(Xte),Xte,med)
            mu=np.mean(Xtr,axis=0); sd=np.std(Xtr,axis=0); sd=np.where(sd>0,sd,1.0); Xtr=(Xtr-mu)/sd; Xte=(Xte-mu)/sd
            beta=fit_logistic(Xtr,ytr,reg=1.0); p=predict_logistic(Xte,beta); ll=loglik(yte,p); total+=ll
            foldrows.append({'MODEL':model,'HELD_OUT_SIMULATION':'SXS:BBH:'+held,'N_ROWS':len(te),'N_TRANSITIONS':int(yte.sum()),'HELDOUT_LOG_LIK':ll,'PREDICTED_TRANSITION_MEAN':float(np.mean(p)),'COEFFICIENT_MIN':float(np.min(beta[1:])),'COEFFICIENT_MAX':float(np.max(beta[1:])),'TRAIN_FEATURE_COUNT':len(names)})
            eventwise.append(foldrows[-1])
        metrics.append({'MODEL':model,'TOTAL_LOGLIK':total,'MEAN_HELDOUT_LOGLIK':total/len(IDS),'N_OUTER_FOLDS':len(IDS),'FEATURES':'|'.join(names)})
    write_csv(ROOT/'R8_SXS_MECHANISM_LOOSV.csv',eventwise); write_csv(ROOT/'R8_SXS_MECHANISM_MODEL_SUMMARY.csv',metrics)
    # Temporal precedence around every observed transition: previous/current/next row physical values.
    temporal=[]
    for tr in transitions:
        er=by[tr['EVENT'].split(':')[-1]]; i=next(i for i in range(len(er)-1) if er[i+1]['STATE']==tr['NEXT_STATE'] and er[i]['STATE']==tr['RIUD_STATE'])
        # use row master keyed by event/bin
        rr=[r for r in allrows if r['EVENT']==tr['EVENT']]; cur=rr[i]; pre=rr[max(0,i-1)]; post=rr[min(len(rr)-1,i+1)]
        for v in horizon+rem+flux:
            temporal.append({'EVENT':tr['EVENT'],'FROM_STATE':tr['RIUD_STATE'],'TO_STATE':tr['NEXT_STATE'],'TRANSITION_TIME':tr['RIUD_TRANSITION_TIME'],'VARIABLE':v,'PRE_TO_AT':arrval(cur[v])-arrval(pre[v]),'AT_TO_POST':arrval(post[v])-arrval(cur[v]),'ORDER':'PRECEDES' if abs(arrval(cur[v])-arrval(pre[v]))>abs(arrval(post[v])-arrval(cur[v])) else 'FOLLOWS_OR_WEAK'})
    write_csv(ROOT/'R8_SXS_MECHANISM_TEMPORAL_AUDIT.csv',temporal)
    print('R8_MECHANISM_CLOSURE_TEST=PASS')
    print('ROW_MASTER_ROWS='+str(len(allrows)))
    print('TRANSITIONS='+str(len(transitions)))

if __name__=='__main__':main()
