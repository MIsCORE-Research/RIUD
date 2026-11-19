import csv, json, math, os, statistics, sys
WORK = r'C:\riud_audit\vii_closeout\work'
FEAT = os.path.join(WORK, 'FINE_TIME_RAW_FEATURES_10_80_EXTENDED.csv')
GAP = os.path.join(WORK, 'GAP_TABLE.csv')
WIDTHS = [10,20,40,60,80]
PRINT_NODE = {10:0.4373, 20:-0.1375, 40:-0.5696, 60:-0.7188, 80:-0.7916}
PRINT_T0 = {10:0.393, 20:-0.081, 40:-0.527, 60:-0.749, 80:-0.851}
# load features
feat = {}
nrows = 0
with open(FEAT, newline='', encoding='utf-8') as f:
    rd = csv.DictReader(f)
    cols = rd.fieldnames
    for row in rd:
        nrows += 1
        try: off = float(row['OFFSET_MS'])
        except Exception: continue
        feat[(row['EVENT'], off)] = row
print('FEAT rows=%d cols_sample=%s' % (nrows, [c for c in cols if 'P250_512' in c][:4]))
offs = sorted(set(o for (e,o) in feat.keys()))
print('OFFSET range: %s .. %s step~%s n_off=%d' % (offs[0], offs[-1], (offs[1]-offs[0]) if len(offs)>1 else '?', len(offs)))
events = sorted(set(e for (e,o) in feat.keys()))
print('FEAT events=%d' % len(events))
def logratio(row, w):
    try:
        h = float(row['H1_P250_512_%dMS' % w]); l = float(row['L1_P250_512_%dMS' % w])
        if h > 0 and l > 0: return math.log10(l/h)
    except Exception: pass
    return None
# T0 baseline: offset == 0 rows
for w in WIDTHS:
    vals = [logratio(r, w) for (e,o), r in feat.items() if o == 0.0]
    vals = [v for v in vals if v is not None]
    if vals: print('T0 w=%d n=%d median=%.4f print=%.4f' % (w, len(vals), statistics.median(vals), PRINT_T0[w]))
# GAP NODE rows
gap_rows = []
with open(GAP, newline='', encoding='utf-8') as f:
    rd = csv.DictReader(f)
    gcols = rd.fieldnames
    for row in rd:
        if row.get('MAP_OBJECT') in ('GAP_LEFT','GAP_CENTER','GAP_RIGHT'):
            gap_rows.append(row)
print('GAP cols=%s' % gcols)
print('GAP side rows total=%d' % len(gap_rows))
ev96 = set(events)
gr96 = [r for r in gap_rows if r['EVENT_ID'] in ev96]
print('GAP side rows in feat events=%d' % len(gr96))
for w in WIDTHS:
    vals = []
    miss = 0
    for r in gr96:
        off = round(float(r['NATIVE_TAU'])*1000.0, 3)
        # try exact and rounded keys
        key = None
        for cand in (off, round(off), float(int(round(off)))):
            if (r['EVENT_ID'], cand) in feat: key = (r['EVENT_ID'], cand); break
        if key is None: miss += 1; continue
        v = logratio(feat[key], w)
        if v is not None: vals.append(v)
    if vals: print('NODE w=%d n=%d miss=%d median=%.4f print=%.4f' % (w, len(vals), miss, statistics.median(vals), PRINT_NODE[w]))
