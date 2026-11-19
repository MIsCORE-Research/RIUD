import json, hashlib, re
from pathlib import Path
import numpy as np
import pandas as pd
import h5py
from scipy.signal import hilbert

AUDIT = Path(r'E:\RIUD_ACTIVE_20260808\MIsCORE_MT_RAW_FROM_SOURCE_R2_20260829\RAW_FRONTEND\FINE_TIME_INPUT_AUDIT.csv')
OUTDIR = Path(r'E:\RIUD_ACTIVE_20260808\MIsCORE_MT_RAW_FROM_SOURCE_R2_20260829\RAW_FRONTEND\WINDOW_10_80_EXTENDED_DIAGNOSTIC')
FEATURES = ['F_PHASE_HZ','FDOT_PHASE_HZ_PER_S','LOGAMP_SLOPE_PER_S','FFT_CENTROID_HZ','FFT_PEAK_HZ','P20_100','P100_250','P250_512','RMS']
WIDTHS = [10.,20.,30.,40.,50.,60.,70.,80.]
OFFSETS = np.arange(-15., 15.0001, 1.)

def local_path(event, det):
    base = Path(r'E:\RIUD_ACTIVE_20260808\RIUD_DEV99_PATH_ONLY_CPU_ADAPTIVE_R10G_20260811_WORK\runtime') / event / 'engine' / 'work' / event / 'regenerated_residuals'
    # The available source is posterior-median residual, kept separate from the frozen 10--40 table.
    hits = list(base.glob(f'*/{event}_{det}_*_POSTERIOR_MEDIAN_RESIDUAL.h5'))
    if not hits:
        raise FileNotFoundError(f'NO_RESIDUAL:{event}:{det}')
    # Prefer XPHM when both families are available; record this choice in the manifest.
    hits.sort(key=lambda p: ('IMRPhenomXPHM' not in str(p), str(p)))
    return hits[0]

def read(path):
    with h5py.File(path, 'r') as h:
        d = h['strain/Strain']; x = np.asarray(d[()], float)
        return x, float(d.attrs.get('sample_rate', d.attrs.get('sampling_rate', 4096.0))), float(d.attrs.get('gps_start', d.attrs.get('Xstart')))

def features(x, zall, fs, center_idx, width_ms):
    n = max(3, int(round(width_ms * fs / 1000.0)))
    lo = int(center_idx - n//2); hi = lo + n
    if lo < 1 or hi >= len(x)-1: return [np.nan]*len(FEATURES)
    # Use a globally computed analytic signal so the phase at each local window is not an edge artifact.
    z = zall[lo:hi]; xx = x[lo:hi]
    t = np.arange(len(z), dtype=float) / fs
    phase = np.unwrap(np.angle(z)); amp = np.abs(z)
    f = float(np.polyfit(t-t.mean(), phase, 1)[0] / (2*np.pi))
    inst = np.gradient(phase, 1/fs) / (2*np.pi)
    fdot = float(np.polyfit(t-t.mean(), inst, 1)[0]) if len(inst) > 2 else np.nan
    slope = float(np.polyfit(t-t.mean(), np.log(np.maximum(amp, 1e-18)), 1)[0])
    win = np.hanning(len(xx)); power = np.abs(np.fft.rfft(xx*win))**2
    freq = np.fft.rfftfreq(len(xx), 1/fs); den = float(power.sum())
    centroid = float((freq*power).sum()/den) if den > 0 else np.nan
    peak = float(freq[np.argmax(power)]) if len(power) else np.nan
    bands=[]
    for a,b in [(20,100),(100,250),(250,512)]: bands.append(float(power[(freq>=a)&(freq<b)].sum()))
    return [f,fdot,slope,centroid,peak,*bands,float(np.sqrt(np.mean(xx*xx)))]

def main():
    q = pd.read_csv(AUDIT)
    rows=[]; manifest=[]
    for event in q.EVENT.astype(str):
        t0 = float(q.loc[q.EVENT.astype(str).eq(event),'H1_T0_GPS'].iloc[0])
        loaded={}
        for det in ('H1','L1'):
            p=local_path(event,det); x,fs,gps=read(p); idx=int(round((t0-gps)*fs)); loaded[det]=(x,hilbert(x),fs,idx)
            manifest.append({'EVENT':event,'DETECTOR':det,'SOURCE':str(p),'FS_HZ':fs,'GPS_START':gps,'T0_GPS':t0,'T0_INDEX':idx,'FAMILY':p.parent.name})
        for off in OFFSETS:
            r={'EVENT':event,'OFFSET_MS':float(off)}
            for w in WIDTHS:
                for det in ('H1','L1'):
                    x,zall,fs,idx=loaded[det]; vals=features(x,zall,fs,idx+int(round(off*fs/1000.0)),w)
                    for k,v in zip(FEATURES,vals): r[f'{det}_{k}_{int(w)}MS']=v
            rows.append(r)
    OUTDIR.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(OUTDIR/'FINE_TIME_RAW_FEATURES_10_80_EXTENDED.csv',index=False)
    pd.DataFrame(manifest).to_csv(OUTDIR/'SOURCE_MANIFEST.csv',index=False)
    meta={'BRANCH':'EXTENDED_WINDOW_DIAGNOSTIC','EVENTS':int(q.EVENT.nunique()),'WIDTHS_MS':WIDTHS,'OFFSETS_MS':[-15,15],'FS_HZ':4096.0,'T0_RULE':'H1_T0_GPS from existing input audit; L1 T0 checked in source manifest','RESIDUAL_FAMILY':'prefer IMRPhenomXPHM posterior-median residual','NO_R40':True,'NO_HOLDOUT5':True,'NO_HOLDOUT30':True}
    (OUTDIR/'MANIFEST.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    print(json.dumps(meta)); print('RUN_FINISHED_EXIT_CODE=0')
if __name__=='__main__': main()
