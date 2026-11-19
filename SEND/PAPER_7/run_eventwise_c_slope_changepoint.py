from pathlib import Path
import csv, json, hashlib
import numpy as np

ROOT=Path(__file__).resolve().parent
CUR = ROOT/'MIsCORE_RAW_EVENTWISE_FULL_TF_CHANGE_R1_20260828'/'EVENTWISE_C_CURVES.csv'
GAP = ROOT/'RIUD_GAP_RAW_POSITION_FULL_CORRECTED_TIME_AUDIT_R2_20260821'/'GAP_RAW_POSITION_FULL_CORRECTED_TIME_EVENT_TABLE.csv'
OUT = ROOT/'MIsCORE_RAW_EVENTWISE_C_SLOPE_CHANGEPOINT_R0_20260828'
OUT.mkdir(parents=True, exist_ok=True)

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

with open(CUR, encoding='utf-8-sig') as f: raw = list(csv.DictReader(f))
groups = {}
for r in raw:
    groups.setdefault((r['EVENT'], r['DETECTOR'], float(r['WIDTH_MS'])), []).append((float(r['CENTER_MS']), float(r['C'])))

rows, curves, errors = [], [], []
for (event, det, width), vals in groups.items():
    try:
        vals = sorted(vals)
        x = np.array([a for a, b in vals]); y = np.array([b for a, b in vals])
        slope = np.gradient(y, x)
        change = np.full(len(y), np.nan)
        change[1:-1] = np.abs(slope[2:] - slope[:-2]) / (x[2:] - x[:-2]) * 2.0
        i = int(np.nanargmax(change[1:-1])) + 1
        rows.append({'EVENT': event, 'DETECTOR': det, 'WIDTH_MS': width,
                     'SLOPE_CHANGEPOINT_MS': x[i], 'SLOPE_CHANGE_SCORE': change[i],
                     'LOCAL_SLOPE_LEFT': slope[i-1], 'LOCAL_SLOPE_RIGHT': slope[i+1],
                     'SLOPE_JUMP': slope[i+1]-slope[i-1], 'N_CENTERS': len(x),
                     'BOUNDARY_HIT': False, 'SELECTION_PHASE': 'FROZEN_EVENTWISE_BEFORE_GAP_JOIN'})
        for a, b, c in zip(x, y, change):
            curves.append({'EVENT': event, 'DETECTOR': det, 'WIDTH_MS': width,
                           'CENTER_MS': a, 'C': b, 'ABS_SLOPE_CHANGE': c})
    except Exception as e:
        errors.append({'EVENT': event, 'DETECTOR': det, 'WIDTH_MS': width, 'ERROR': repr(e)})

def write(name, data, fields):
    with open(OUT/name, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(data)

write('EVENTWISE_SLOPE_CHANGEPOINT.csv', rows, list(rows[0]) if rows else ['EVENT', 'ERROR'])
write('SLOPE_CHANGEPOINT_CURVES.csv', curves, list(curves[0]) if curves else ['EVENT', 'ERROR'])
write('ERRORS.csv', errors, ['EVENT', 'DETECTOR', 'WIDTH_MS', 'ERROR'])

gap = {}
with open(GAP, encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):
        if r.get('MAP_OBJECT') == 'GAP_CENTER':
            try: gap[r['EVENT_ID']] = float(r['NATIVE_TAU']) * 1000.0
            except Exception: pass
evaluation = []
for r in rows:
    if r['EVENT'] in gap:
        z = dict(r); z.update({'GAP_CENTER_NATIVE_TAU_MS': gap[r['EVENT']],
            'TIMING_ERROR_MS': float(r['SLOPE_CHANGEPOINT_MS']) - gap[r['EVENT']],
            'EVALUATION_PHASE': 'POST_SELECTION_JOIN'}); evaluation.append(z)
write('EVENTWISE_GAP_TIMING_EVALUATION.csv', evaluation,
      list(evaluation[0]) if evaluation else list(rows[0]) + ['GAP_CENTER_NATIVE_TAU_MS', 'TIMING_ERROR_MS', 'EVALUATION_PHASE'])

summary = {'BRANCH': 'MIsCORE_RAW_EVENTWISE_C_SLOPE_CHANGEPOINT_R0_20260828',
    'INPUT_CURVE': str(CUR), 'N_INPUT_CURVE_ROWS': len(raw),
    'N_EVENT_DETECTOR_WIDTH_GROUPS': len(rows), 'N_ERRORS': len(errors),
    'SUPPORT_MS': '[-100,+100]', 'WIDTHS_MS': [5, 10, 20], 'CENTER_STEP_MS': 1,
    'CHANGEPOINT': 'maximum absolute local slope change / centered second difference',
    'SELECTION_EVENTWISE_ONLY': True, 'POPULATION_AVERAGING_FOR_SELECTION': False,
    'T0_DISTANCE_FOR_SELECTION': False, 'GAP_MT_NODE_PATH_USED_FOR_SELECTION': False,
    'GAP_JOIN_AFTER_FREEZE': True, 'GAP_CENTER_EVALUATION_ROWS': len(evaluation),
    'HISTORICAL_GAP_USED_FOR_SELECTION': False, 'HISTORICAL_MT_USED_FOR_SELECTION': False,
    'HOLDOUT30_ACCESSED': False, 'NO_FIT': True, 'NO_THRESHOLD': True}
for det in ['H1', 'L1']:
    for width in [5, 10, 20]:
        z = [float(r['TIMING_ERROR_MS']) for r in evaluation if r['DETECTOR'] == det and float(r['WIDTH_MS']) == width]
        summary[f'{det}_W{width}_N'] = len(z)
        summary[f'{det}_W{width}_MEDIAN_ABS_ERROR_MS'] = float(np.median(np.abs(z))) if z else None
        summary[f'{det}_W{width}_MAE_MS'] = float(np.mean(np.abs(z))) if z else None
(OUT/'SUMMARY.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
(OUT/'METHODS.md').write_text('# Eventwise C slope-change changepoint\n\nThe prior eventwise C(t) curves are used without combining events. For each event, detector, and width, the interior maximum of absolute local slope change is selected. This detects where the way C changes changes, rather than the largest C amplitude. Corrected GAP_CENTER is joined only after selection freeze.\n', encoding='utf-8')
with open(OUT/'SHA256_MANIFEST.txt', 'w', encoding='utf-8') as f:
    for p in sorted(OUT.iterdir()):
        if p.is_file() and p.name != 'SHA256_MANIFEST.txt': f.write(f'{sha(p)}  {p.name}\n')
print(json.dumps(summary, indent=2))
