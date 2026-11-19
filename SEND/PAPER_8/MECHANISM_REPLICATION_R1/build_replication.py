import csv, json, hashlib
from pathlib import Path
from statistics import median

BASE=Path(r'E:/RIUD_ACTIVE_20260808/MIsCORE_RIUD_AUXILIARY_HORIZONDUMP_MECHANISM_TEST_R0_20260827')
OUT=Path(__file__).resolve().parent
R8=Path(__file__).resolve().parent.parent / "R8_PHYSICAL_MECHANISM_CLOSURE"
R11=Path(r'E:/RIUD_ACTIVE_20260808/MIsCORE_RIUD_COMMON_HORIZON_RELAXATION_PHASE_R11_20260827')
def rd(p):
    with open(p,newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def f(x):
    try:return float(x)
    except:return None
def main():
    OUT.mkdir(exist_ok=True)
    tr=rd(BASE/'AUXILIARY_TRANSIENT_COMPARISON.csv'); cr=rd(BASE/'AUXILIARY_SURFACE_WAVEFORM_CROSSCHECK.csv')
    fields=sorted(set(x['VARIABLE'] for x in tr)); summary=[]
    for v in fields:
        xs=[x for x in tr if x['VARIABLE']==v]; signs=[f(x['EARLY_MINUS_LATE'])>0 for x in xs]
        summary.append({'VARIABLE':v,'EVENTS':len(xs),'EARLY_MINUS_LATE_0319':next((x['EARLY_MINUS_LATE'] for x in xs if x['EVENT']=='0319'),''),'EARLY_MINUS_LATE_0323':next((x['EARLY_MINUS_LATE'] for x in xs if x['EVENT']=='0323'),''),'SAME_DIRECTION_BOTH_EVENTS':str(len(set(signs))==1),'MEDIAN_RATIO':median([f(x['EARLY_TO_LATE_RATIO']) for x in xs])})
    with open(OUT/'AUXILIARY_REPLICATION_SUMMARY.csv','w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
    # compact cross-event waveform-correlation table
    with open(OUT/'AUXILIARY_WAVEFORM_CROSSCHECK.csv','w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=list(cr[0]));w.writeheader();w.writerows(cr)
    metrics=[
      ('R8_BM_PLUS_FLUX_INCREMENTAL_LL',9.377255076976752,'R8 frozen mechanism model summary'),
      ('R8_FULL_SOURCE_STATE_INCREMENTAL_AFTER_MEMORY_LL',-38.66994508480133,'R8 interim synthesis'),
      ('R8_HORIZON_PLUS_FLUX_INCREMENTAL_AFTER_MEMORY_LL',-42.963721545587646,'R8 interim synthesis'),
      ('R11_HORIZON_RELAXATION_PHASE_STATUS','NOT_ESTABLISHED','R11 final report'),
      ('R11_FINAL_MECHANISM_VERDICT','D_COMMON_HORIZON_REMNANT_PHASE_NOT_SUPPORTED','R11 final report'),
      ('AUXILIARY_SURFACE_FIELDS_WITH_SAME_DIRECTION_2_EVENT',sum(x['SAME_DIRECTION_BOTH_EVENTS']=='True' for x in summary),'new two-event audit'),
      ('AUXILIARY_FIELD_COUNT',len(summary),'new two-event audit'),
      ('AUXILIARY_EARLY_TRANSIENT_REPLICATION','4/4 fields same directional change','new two-event audit'),
      ('AUXILIARY_SIMPLE_WAVEFORM_CORRELATION','weak/low-magnitude and field-dependent','new two-event audit'),
    ]
    with open(OUT/'MECHANISM_REPLICATION_METRICS.csv','w',newline='',encoding='utf-8') as h:
        w=csv.writer(h);w.writerow(['METRIC','VALUE','SOURCE']);w.writerows(metrics)
    report='''# MIsCORE mechanism replication R1

## Question

Does a direct source-native horizon-surface transient repeat in independent pure-GR simulations, and does it by itself close the frozen RIUD memory/rate mechanism?

## Frozen upstream evidence

- R8 source-native mechanism closure: horizon/radiation/source-state additions did not establish a unique mechanism for the RIUD memory or S law.
- R11 common-horizon relaxation phase: not established as a sufficient explanation.
- Frozen R40 remains an exact discrete/age-structured transition-rate law within its support; it is not re-fit here.

## New deterministic auxiliary result

The same fixed comparison was applied to SXS:BBH:0319 and SXS:BBH:0323 `HorizonsDump.h5` files. For AhC, angular RMS in the first 0–5M after common-horizon formation was compared with the fixed 25–50M window.

- SpinFunction: early excess in both events.
- WeylE_NN: early excess in both events.
- DimlessRicciScalar: early excess in both events.
- WeylB_NN: early deficit in both events.

Thus 4/4 audited surface fields repeat the same directional early-to-late change in both auxiliary events. Simple correlations with asymptotic Psi4 amplitudes remain weak and field-dependent, so this is not a waveform-amplitude law.

## Mechanism boundary

The most economical surviving mechanism candidate is a short-lived common-horizon surface-geometry transient involving electric/Weyl and spin-curvature structure, with a corresponding but not yet causally identified radiative response. This is stronger than a one-event coincidence, but it does not explain the R8 memory likelihood or frozen S clock by itself: full source-state models still failed to close the mechanism, and R11 did not establish a sufficient horizon-relaxation law.

`MECHANISM_CANDIDATE=COMMON_HORIZON_SURFACE_GEOMETRY_TRANSIENT`

`DIRECT_GR_DERIVATION=NOT_ESTABLISHED`

`CAUSAL_EXPLANATION_OF_RIUD_S=NOT_ESTABLISHED`

`NEW_PHYSICS=NOT_CLAIMED`
'''
    (OUT/'R1_FINAL_REPORT.md').write_text(report,encoding='utf-8')
    prov={'inputs':[str(BASE/'AUXILIARY_TRANSIENT_COMPARISON.csv'),str(BASE/'AUXILIARY_SURFACE_WAVEFORM_CROSSCHECK.csv'),str(R8/'R8_FINAL_REPORT.md'),str(R11/'R11_FINAL_REPORT.md')],'rules':'fixed 0-5M vs 25-50M, AhC only, no refit, no labels, no Holdout30'}
    (OUT/'SOURCE_BINDING.json').write_text(json.dumps(prov,indent=2),encoding='utf-8')
    with open(OUT/'SHA256_MANIFEST.txt','w',encoding='utf-8') as h:
        for p in sorted(OUT.iterdir()):
            if p.name!='SHA256_MANIFEST.txt' and p.is_file():
                q=hashlib.sha256(p.read_bytes()).hexdigest();h.write(f'{q}  {p.name}\n')
if __name__=='__main__':main()
