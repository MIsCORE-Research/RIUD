import csv
from pathlib import Path
import h5py
import numpy as np

BASE = Path(r'E:/RIUD_ACTIVE_20260808/MIsCORE_RIUD_AUXILIARY_HORIZONDUMP_MECHANISM_TEST_R0_20260827')
OUT = Path(__file__).resolve().parent
EVENTS = ['0319', '0323', '0320']
SURFACE = ['SpinFunction', 'WeylE_NN', 'WeylB_NN', 'DimlessRicciScalar']

def td(f, key):
    idx = np.asarray(f[key + '/index.dat'][:], float)
    dat = np.asarray(f[key + '/data.dat'][:], float).ravel()
    out = []
    for q in idx:
        end = int(q[1]); n = int(q[2] * q[3])
        x = dat[end-n:end]
        out.append((q[0], float(np.sqrt(np.mean(x*x)))))
    return np.asarray(out)

def corr(a, b):
    a = a - np.mean(a); b = b - np.mean(b)
    den = np.sqrt(np.dot(a, a) * np.dot(b, b))
    return float(np.dot(a, b) / den) if den else float('nan')

def main():
    zero, lag = [], []
    for ev in EVENTS:
        root = BASE / ev
        with h5py.File(root/'HorizonsDump.h5', 'r') as f:
            surface = {v: td(f, 'AhC.dir/' + v + '.tdm') for v in SURFACE}
        t_ahc = float(surface['SpinFunction'][0, 0])
        with h5py.File(root/'rMPsi4_Asymptotic_GeometricUnits.h5', 'r') as f:
            modes = {}
            for mode, key in [('h22_amp','Extrapolated_N2.dir/Y_l2_m2.dat'), ('h44_amp','Extrapolated_N2.dir/Y_l4_m4.dat')]:
                x = np.asarray(f[key][:], float)
                modes[mode] = np.column_stack((x[:,0], np.hypot(x[:,1], x[:,2])))
        lo = max([t_ahc] + [x[:,0].min() for x in surface.values()] + [x[:,0].min() for x in modes.values()])
        hi = min([t_ahc + 80.0] + [x[:,0].max() for x in surface.values()] + [x[:,0].max() for x in modes.values()])
        grid = np.arange(lo, hi, 0.5)
        series = {v: np.interp(grid, surface[v][:,0], surface[v][:,1]) for v in SURFACE}
        series.update({v: np.interp(grid, modes[v][:,0], modes[v][:,1]) for v in modes})
        for a in SURFACE:
            for b in modes:
                zero.append({'EVENT':ev,'VAR_A':a,'VAR_B':b,'WINDOW':'AHC_0_80M','ZERO_LAG_CORR':corr(series[a],series[b]),'N':len(grid)})
                for lm in range(-20, 21):
                    if lm >= 0:
                        x, y = series[a][:-lm or None], series[b][lm:]
                    else:
                        x, y = series[a][-lm:], series[b][:lm or None]
                    lag.append({'EVENT':ev,'VAR_A':a,'VAR_B':b,'LAG_M':lm,'CORR':corr(x,y),'WINDOW':'AHC_0_80M'})
    with (OUT/'SURFACE_WAVEFORM_ZERO_LAG_CORRELATIONS.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(zero[0])); w.writeheader(); w.writerows(zero)
    with (OUT/'SURFACE_WAVEFORM_LAG_CORRELATIONS.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(lag[0])); w.writeheader(); w.writerows(lag)
    summary = []
    for ev in EVENTS:
        for a in SURFACE:
            for b in modes:
                q = [r for r in lag if r['EVENT']==ev and r['VAR_A']==a and r['VAR_B']==b]
                m = max(q, key=lambda r: abs(float(r['CORR'])))
                z = next(r for r in zero if r['EVENT']==ev and r['VAR_A']==a and r['VAR_B']==b)
                summary.append({'EVENT':ev,'VAR_A':a,'VAR_B':b,'ZERO_LAG_CORR':z['ZERO_LAG_CORR'],'MAX_ABS_CORR_FIXED_LAG':m['CORR'],'LAG_AT_MAX_ABS_CORR_M':m['LAG_M']})
    with (OUT/'SURFACE_WAVEFORM_LAG_SUMMARY.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0])); w.writeheader(); w.writerows(summary)
    lines = ['# Surface-to-waveform cross-correlation audit', '', 'Fixed AhC-relative 0–80M window and 0.5M grid. Surface angular RMS fields were compared with h22/h44 amplitude. Lag scan was prespecified at −20M..+20M in 1M increments and is descriptive; no lag or coefficient was fitted.']
    for r in summary:
        lines.append(f"- {r['EVENT']} {r['VAR_A']} vs {r['VAR_B']}: zero-lag={float(r['ZERO_LAG_CORR']):.6g}; max-|r|={float(r['MAX_ABS_CORR_FIXED_LAG']):.6g} at lag={r['LAG_AT_MAX_ABS_CORR_M']}M")
    lines += ['', 'Interpretation is limited to temporal co-variation. Correlation does not establish causality or identity with the observational RIUD GAP/MT/S law.']
    (OUT/'SURFACE_WAVEFORM_CROSS_CORRELATION_AUDIT.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')

if __name__ == '__main__':
    main()
