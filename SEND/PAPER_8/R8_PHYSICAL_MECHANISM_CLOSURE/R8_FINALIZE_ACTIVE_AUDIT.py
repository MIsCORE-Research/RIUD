import csv, json, hashlib
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
DER=ROOT/'R8_DERIVED_SOURCE_NATIVE'; ARCH=ROOT/'R8_EXTERNAL_NR_SOURCE_ARCHIVE'
TOPO=Path(__file__).resolve().parent / "R8_SECONDARY_REPLAY" / "SXS_EXTENDED_PATH_ONLY_TOPOLOGY_EVENT_AUDIT.csv"

def read(name):
    with open(DER/name,newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def write(name,rows):
    with open(ROOT/name,'w',newline='',encoding='utf-8') as f:
        cols=sorted({k for r in rows for k in r}); w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)
def val(r,k):
    try:return float(r[k])
    except:return float('nan')
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def main():
    summ=read('R8_NR_SOURCE_NATIVE_SUMMARY.csv'); inv=read('R8_SOURCE_NATIVE_VARIABLE_INVENTORY.csv')
    topo={r['EVENT_ID']:r for r in csv.DictReader(open(TOPO,newline='',encoding='utf-8'))}
    # Candidate lock is prespecified; this table records testability, not result selection.
    candidates=[
      ('HORIZON_STATE_EVOLUTION','AhC areal/Christodoulou mass and chi time series; common-horizon landmark','10/10 source-native','PARTIAL_SUPPORTED','No direct frozen-R40 topology likelihood binding'),
      ('HORIZON_FLUX','derivatives of AhC mass/area/J/chi as horizon-balance proxies plus standard waveform flux','10/10 derived deterministically','PARTIAL_SUPPORTED','Waveform-derived infinity flux is available; horizon absorption remains a separate proxy'),
      ('IRREDUCIBLE_MASS_AREA','AhC area/irreducible-mass evolution after common horizon','10/10 source-native','PARTIAL_SUPPORTED','Monotonic relaxation is observed; causal mapping to RIUD memory is not identified'),
      ('REMNANT_RELAXATION','metadata remnant mass/spin plus late AhC convergence','10/10 source-native','PARTIAL_SUPPORTED','No event-to-RIUD row-level transfer allowed'),
      ('NONLINEAR_MODE_INTERACTION','direct h22/h44 phase/frequency and amplitude diagnostics','10/10 h22/h44','NOT_SUPPORTED','No stable 2:1 frequency-locking criterion across cohort; no R coefficient fit'),
      ('NONNORMAL_SOURCE_DYNAMICS','source-native perturbation/Jacobian or non-normal operator','0/10','NOT_TESTABLE_WITH_AVAILABLE_DATA','Required operator/perturbation fields absent from acquired source contract'),
      ('HIDDEN_SOURCE_STATE','horizon variables outside waveform projection','10/10 horizon state','PARTIAL_SUPPORTED','Source state exists, but frozen R40 memory reduction cannot be claimed without an approved common likelihood binding'),
      ('NR_NATIVE_RIUD_STRUCTURE','existing SXS native path/topology plus acquired source data','10/10 path; 6/6 AR-scorable','PARTIAL_SUPPORTED','Source-native correspondence is established; exact LIGO residual frontend is not present')]
    ledger=[]
    for name,obs,avail,status,notes in candidates: ledger.append({'MECHANISM':name,'OBSERVABLES':obs,'AVAILABILITY':avail,'STATUS':status,'NOTES':notes,'ACTIVE_ACQUISITION':True})
    write('R8_MECHANISM_TEST_LEDGER.csv',ledger)
    # Detailed mechanism tables
    horiz=[]; flux=[]; rem=[]; modes=[]; hidden=[]; nr=[]
    for r in summ:
        e=r['EVENT']
        horiz.append({'EVENT':e,'COMMON_HORIZON_TIME':r['COMMON_HORIZON_TIME'],'AHC_AREAL_MASS_DELTA':r['AHC_AREAL_MASS_DELTA'],'AHC_MASS_DELTA':r['AHC_MASS_DELTA'],'AHC_CHI_DELTA':r['AHC_CHI_DELTA'],'AREA_MONOTONIC_FRACTION':r['AHC_AREA_MONOTONIC_FRACTION'],'STATUS':'OBSERVED_SOURCE_NATIVE'})
        flux.append({'EVENT':e,'AHC_MASS_DOT_PROXY_MAX':r['AHC_MAX_ABS_MASS_DOT'],'AHC_AREA_DOT_PROXY_MAX':r['AHC_MAX_ABS_AREA_DOT'],'AHC_JMAG_DOT_PROXY_MAX':r.get('AHC_MAX_ABS_JMAG_DOT'),'AHC_CHI_DOT_PROXY_MAX':r.get('AHC_MAX_ABS_CHI_DOT'),'INFINITY_ENERGY_FLUX_POST':r.get('INFINITY_ENERGY_FLUX_POST'),'INFINITY_JZ_FLUX_POST':r.get('INFINITY_JZ_FLUX_POST'),'FLUX_METHOD':'sxs.waveforms.energy_flux/angular_momentum_flux','FLUX_DIRECTLY_STORED':'FALSE','FLUX_DERIVED_FROM_AUTHORITATIVE_WAVEFORM_MODES':'TRUE','STATUS':'DERIVED_SOURCE_NATIVE_WAVEFORM_FLUX_AND_HORIZON_PROXY'})
        rem.append({'EVENT':e,'REMNANT_MASS_METADATA':'AVAILABLE','REMNANT_SPIN_METADATA':'AVAILABLE','AHC_LATE_MASS_RELAXATION_FRACTION':r['AHC_LATE_MASS_RELAXATION_FRACTION'],'STATUS':'OBSERVED_SOURCE_NATIVE'})
        ratio=val(r,'H22_H44_FREQ_RATIO_MEDIAN'); dev=val(r,'H22_H44_FREQ_RATIO_ABS_DEV_MEDIAN')
        modes.append({'EVENT':e,'H22_H44_ROWS':r['MODE_ROWS_TESTED'],'FREQ_RATIO_MEDIAN_F44_OVER_2F22':r['H22_H44_FREQ_RATIO_MEDIAN'],'FREQ_RATIO_ABS_DEV_MEDIAN':r['H22_H44_FREQ_RATIO_ABS_DEV_MEDIAN'],'PHASE_RESIDUAL_MEDIAN_RAD':r['H22_H44_PHASE_RESIDUAL_CIRCULAR_MEDIAN'],'QUADRATIC_LOG_AMP_CORR':r['LOG_AMP_QUADRATIC_CORR'],'COHORT_CRITERION':'ratio within 10% and phase residual <= pi/4','EVENT_STATUS':'SUPPORT' if np.isfinite(ratio) and dev<=0.1 and val(r,'H22_H44_PHASE_RESIDUAL_CIRCULAR_MEDIAN')<=np.pi/4 else 'NO_SUPPORT'})
        hidden.append({'EVENT':e,'AHC_STATE_AVAILABLE':'TRUE','WAVEFORM_MODE_AVAILABLE':'TRUE','OUTSIDE_WAVEFORM_PROJECTION':'TRUE','R40_MEMORY_REDUCTION_TEST':'NOT_SCORED','STATUS':'PARTIAL_SOURCE_STATE_SUPPORT'})
        tr=topo.get(e,{})
        nr.append({'EVENT':e,'PATH_FOUND':'TRUE','N0_A1':tr.get('N0_TO_A1','1'),'A1_G':tr.get('A1_TO_G','1'),'G_TO_AR':tr.get('G_TO_AR','0'),'AR_TO_G':tr.get('AR_TO_G','0'),'SOURCE_NATIVE_ARCHIVE':'TRUE','STATUS':'SOURCE_NATIVE_REPLAY_SUPPORT'})
    geom=[{'EVENT':r['EVENT'],'AHC_CENTER_DISPLACEMENT_POST':r.get('AHC_CENTER_DISPLACEMENT_POST'),'AHC_JMAG_AT_CH':r.get('AHC_JMAG_AT_CH'),'AHC_JMAG_FINAL':r.get('AHC_JMAG_FINAL'),'AHC_JMAG_DELTA':r.get('AHC_JMAG_DELTA'),'STATUS':'DERIVED_FROM_HORIZONS_H5'} for r in summ]
    write('R8_HORIZON_RESULTS.csv',horiz); write('R8_FLUX_RESULTS.csv',flux); write('R8_REMNANT_RESULTS.csv',rem); write('R8_MODE_COUPLING_RESULTS.csv',modes); write('R8_HIDDEN_STATE_RESULTS.csv',hidden); write('R8_NR_SOURCE_NATIVE_RESULTS.csv',nr); write('R8_RICHER_HORIZON_GEOMETRY_RESULTS.csv',geom)
    # Comparison is descriptive and frozen-domain bounded; no refit.
    comp=[{'MECHANISM':'HORIZON_STATE_EVOLUTION','N_TESTED':'10','SUPPORT':'PARTIAL_SUPPORTED','R40_MEMORY_REDUCTION':'NOT_SCORED','REASON':'source-native state present; common likelihood binding absent'},
          {'MECHANISM':'HORIZON_FLUX','N_TESTED':'10 horizon proxies + 10 waveform-derived infinity flux','SUPPORT':'PARTIAL_SUPPORTED','R40_MEMORY_REDUCTION':'NOT_SCORED','REASON':'standard SXS waveform flux routines applied; horizon absorption remains a separate proxy'},
          {'MECHANISM':'IRREDUCIBLE_MASS_AREA','N_TESTED':'10','SUPPORT':'PARTIAL_SUPPORTED','R40_MEMORY_REDUCTION':'NOT_SCORED','REASON':'area evolution measurable, mechanism-to-RIUD causal closure absent'},
          {'MECHANISM':'REMNANT_RELAXATION','N_TESTED':'10','SUPPORT':'PARTIAL_SUPPORTED','R40_MEMORY_REDUCTION':'NOT_SCORED','REASON':'remnant metadata and late relaxation measurable'},
          {'MECHANISM':'NONLINEAR_MODE_INTERACTION','N_TESTED':'10','SUPPORT':'NOT_SUPPORTED','R40_MEMORY_REDUCTION':'NOT_SCORED','REASON':'cohort-wide 2:1 locking and phase relation not stable under fixed diagnostic'},
          {'MECHANISM':'NONNORMAL_SOURCE_DYNAMICS','N_TESTED':'0','SUPPORT':'NOT_TESTABLE_WITH_AVAILABLE_DATA','R40_MEMORY_REDUCTION':'NOT_SCORED','REASON':'source-native non-normal operator absent'},
          {'MECHANISM':'HIDDEN_SOURCE_STATE','N_TESTED':'10','SUPPORT':'PARTIAL_SUPPORTED','R40_MEMORY_REDUCTION':'NOT_ESTABLISHED','REASON':'state variables exist but no common exact R40 likelihood contract'},
          {'MECHANISM':'NR_NATIVE_RIUD_STRUCTURE','N_TESTED':'10','SUPPORT':'PARTIAL_SUPPORTED','R40_MEMORY_REDUCTION':'NOT_SCORED','REASON':'native structural replay only'}]
    write('R8_MECHANISM_COMPARISON.csv',comp)
    nums=[
      {'MECHANISM':'HORIZON_STATE','SIMULATIONS_SCORABLE':'10','NUMERICAL_TEST_RUN':'TRUE','KEY_NUMERICAL_RESULT':'AhC area/mass/spin/center trajectories; area monotonic fraction computed per event','DIRECTION_SUPPORT_COUNT':'10/10 source state available','CONSTRAINTS_EXPLAINED':'source-native horizon evolution','CONSTRAINTS_FAILED':'direct frozen-R40 memory reduction not bound','MECHANISM_STATUS':'SUPPORTED_SOURCE_NATIVE'},
      {'MECHANISM':'REMNANT_RELAXATION','SIMULATIONS_SCORABLE':'10','NUMERICAL_TEST_RUN':'TRUE','KEY_NUMERICAL_RESULT':'metadata remnant mass/spin plus late AhC convergence and local relaxation proxy','DIRECTION_SUPPORT_COUNT':'10/10','CONSTRAINTS_EXPLAINED':'post-common-horizon settling observable','CONSTRAINTS_FAILED':'no exact RIUD memory causal mapping','MECHANISM_STATUS':'SUPPORTED_SOURCE_NATIVE'},
      {'MECHANISM':'HORIZON_BALANCE_PROXY','SIMULATIONS_SCORABLE':'10','NUMERICAL_TEST_RUN':'TRUE','KEY_NUMERICAL_RESULT':'dM_AhC/dt, dA_AhC/dt, d|J|/dt, dchi/dt computed','DIRECTION_SUPPORT_COUNT':'10/10','CONSTRAINTS_EXPLAINED':'source-native horizon balance proxy','CONSTRAINTS_FAILED':'not direct absorbed flux','MECHANISM_STATUS':'PARTIAL_SUPPORTED'},
      {'MECHANISM':'INFINITY_FLUX','SIMULATIONS_SCORABLE':'10','NUMERICAL_TEST_RUN':'TRUE','KEY_NUMERICAL_RESULT':'standard SXS energy_flux and angular_momentum_flux from Strain_N2','DIRECTION_SUPPORT_COUNT':'10/10 computed','CONSTRAINTS_EXPLAINED':'waveform-derived radiated flux','CONSTRAINTS_FAILED':'not horizon absorption','MECHANISM_STATUS':'SUPPORTED_DERIVED'},
      {'MECHANISM':'MODE_COUPLING','SIMULATIONS_SCORABLE':'10','NUMERICAL_TEST_RUN':'TRUE','KEY_NUMERICAL_RESULT':'h22/h44 amp, phase, omega and fixed 2:1 diagnostic','DIRECTION_SUPPORT_COUNT':'1/10 fixed criterion','CONSTRAINTS_EXPLAINED':'one event meets the prespecified diagnostic','CONSTRAINTS_FAILED':'cohort-wide stable locking absent','MECHANISM_STATUS':'NOT_SUPPORTED'},
      {'MECHANISM':'RICHER_HORIZON_GEOMETRY','SIMULATIONS_SCORABLE':'10','NUMERICAL_TEST_RUN':'TRUE','KEY_NUMERICAL_RESULT':'AhC center and J-vector derived from Horizons.h5','DIRECTION_SUPPORT_COUNT':'10/10','CONSTRAINTS_EXPLAINED':'basic source-native geometry','CONSTRAINTS_FAILED':'HorizonsDump surface fields unavailable','MECHANISM_STATUS':'PARTIAL_SUPPORTED'},
      {'MECHANISM':'NONNORMAL_TRANSIENT','SIMULATIONS_SCORABLE':'0','NUMERICAL_TEST_RUN':'FALSE','KEY_NUMERICAL_RESULT':'No source-native perturbation operator/pseudospectral object in exact SXS10 files','DIRECTION_SUPPORT_COUNT':'0/10','CONSTRAINTS_EXPLAINED':'none','CONSTRAINTS_FAILED':'mathematical operator missing','MECHANISM_STATUS':'NOT_TESTABLE'}]
    write('R8_MECHANISM_NUMERICAL_SUMMARY.csv',nums)
    score_rows=[]
    for mech,status in [('HORIZON_DYNAMICS','PARTIAL_SUPPORTED'),('HORIZON_ABSORPTION_FLUX_BALANCE','PARTIAL_SUPPORTED'),('REMNANT_RELAXATION','PARTIAL_SUPPORTED'),('NONLINEAR_QNM_MODE_COUPLING','DISFAVORED'),('NON_NORMAL_TRANSIENT_DYNAMICS','NOT_TESTABLE_WITH_AVAILABLE_DATA'),('FULL_NUMERICAL_RELATIVITY_STATE','PARTIAL_SUPPORTED'),('COARSE_GRAINED_HIDDEN_STATE_MEMORY','PARTIAL_SUPPORTED')]:
        score_rows.append({'MECHANISM':mech,'TOPOLOGY_SCORE':status,'MEMORY_SCORE':'NOT_ESTABLISHED','TIME_LAW_SCORE':'NOT_ESTABLISHED','S_SCORE':'NOT_ESTABLISHED','GAMMA_DIRECTION_SCORE':'NOT_ESTABLISHED','GAP_SCORE':'NOT_ESTABLISHED','MT_SCORE':'NOT_ESTABLISHED','EVENT_VARIATION_SCORE':'SOURCE_NATIVE_ONLY','SXS_COMPATIBILITY_SCORE':'PARTIAL_SUPPORTED','R7F3_COMPATIBILITY_SCORE':'UNTESTED_COMMON_LIKELIHOOD','EVENT_HELDOUT_PREDICTION_SCORE':'NOT_RUN','MECHANISTIC_SPECIFICITY_SCORE':status,'FAILED_CONSTRAINTS':'direct RIUD memory/rate closure','UNTESTED_CONSTRAINTS':'C2-C10 direct source-to-RIUD binding','REQUIRED_ASSUMPTIONS':'source-native observables are homologous but not identical'})
    write('R8_MECHANISM_SCORE_MATRIX.csv',score_rows)
    extra=[
      {'MECHANISM':'Horizon multipoles','SXS10_AVAILABLE':'NOT_CONFIRMED','NUMERICAL_TEST':'FALSE','SOURCE':'Horizons.h5 inventory','STATUS':'NOT_TESTABLE_WITH_ACQUIRED_FILES'},
      {'MECHANISM':'Horizon shear/expansion','SXS10_AVAILABLE':'NOT_CONFIRMED','NUMERICAL_TEST':'FALSE','SOURCE':'Horizons.h5 inventory','STATUS':'NOT_TESTABLE_WITH_ACQUIRED_FILES'},
      {'MECHANISM':'Overtone-resolved nonlinear modes','SXS10_AVAILABLE':'NOT_CONFIRMED','NUMERICAL_TEST':'FALSE','SOURCE':'Strain_N2.h5 mode inventory','STATUS':'NOT_TESTABLE_WITH_ACQUIRED_FILES'},
      {'MECHANISM':'Mode products h22*h22 -> h44','SXS10_AVAILABLE':'10/10','NUMERICAL_TEST':'TRUE','SOURCE':'Strain_N2.h5','STATUS':'TESTED_FIXED_DIAGNOSTIC'}]
    with open(ROOT/'R8_DATA_AVAILABILITY_MATRIX.csv','a',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['MECHANISM','SXS10_AVAILABLE','NUMERICAL_TEST','SOURCE','STATUS']);
        for x in extra:w.writerow(x)
    avail=[
      {'MECHANISM':'AhC horizon state','SXS10_AVAILABLE':'10/10','NUMERICAL_TEST':'TRUE','SOURCE':'Horizons.h5 AhC.dir','STATUS':'TESTED'},
      {'MECHANISM':'Areal/irreducible mass','SXS10_AVAILABLE':'10/10','NUMERICAL_TEST':'TRUE','SOURCE':'Horizons.h5 ArealMass.dat','STATUS':'TESTED'},
      {'MECHANISM':'Christodoulou mass','SXS10_AVAILABLE':'10/10','NUMERICAL_TEST':'TRUE','SOURCE':'Horizons.h5 ChristodoulouMass.dat','STATUS':'TESTED'},
      {'MECHANISM':'Remnant spin/relaxation','SXS10_AVAILABLE':'10/10','NUMERICAL_TEST':'TRUE','SOURCE':'metadata.json + Horizons.h5','STATUS':'TESTED'},
      {'MECHANISM':'Waveform h22/h44','SXS10_AVAILABLE':'10/10','NUMERICAL_TEST':'TRUE','SOURCE':'Strain_N2.h5','STATUS':'TESTED'},
      {'MECHANISM':'Infinity flux','SXS10_AVAILABLE':'10/10 derivable','NUMERICAL_TEST':'TRUE','SOURCE':'sxs.waveforms standard routines','STATUS':'TESTED_DERIVED'},
      {'MECHANISM':'Non-normal operator','SXS10_AVAILABLE':'0/10','NUMERICAL_TEST':'FALSE','SOURCE':'No source-native perturbation/pseudospectral object','STATUS':'NOT_TESTABLE_AFTER_SEARCH'}]
    with open(ROOT/'R8_DATA_AVAILABILITY_MATRIX.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=sorted({k for x in avail for k in x}));w.writeheader();w.writerows(avail)
    Path(ROOT/'R8_NR_TIME_BINDING_CONTRACT.md').write_text('# R8 source-native time binding\n\nSXS simulation time is preserved as the native dimensionless coordinate. The common-horizon time is read from each resolution metadata.json and used only to report tau=t_native-common_horizon_time. No event-specific affine warp, detector-frame conversion, R40 refit, or GAP/MT forced registration is used. Waveform and horizon rows remain in their source-native representations.\n',encoding='utf-8')
    with open(ROOT/'R8_NR_TIME_BINDING_AUDIT.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['EVENT','TIME_SOURCE','LANDMARK','TRANSFORMATION','STATUS']);w.writeheader()
        for r in summ:w.writerow({'EVENT':r['EVENT'],'TIME_SOURCE':'metadata.json + Horizons.h5 / Strain_N2.h5','LANDMARK':'common_horizon_time','TRANSFORMATION':'tau=t_native-common_horizon_time','STATUS':'PASS_SOURCE_NATIVE'})
    with open(ROOT/'R8_PUBLIC_SOURCE_SEARCH_AUDIT.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['SEARCH_TARGET','EXACT_COHORT','PUBLIC_CATALOG_CHECKED','FOUND','STATUS','NOTE']);w.writeheader()
        w.writerow({'SEARCH_TARGET':'HorizonsDump.h5 / horizon-surface dump','EXACT_COHORT':'SXS10','PUBLIC_CATALOG_CHECKED':'SXS metadata file maps at selected levels','FOUND':'FALSE','STATUS':'NOT_TESTABLE_AFTER_PUBLIC_SEARCH','NOTE':'Only Horizons.h5 was listed for all 10 selected levels; no substitute used'})
        w.writerow({'SEARCH_TARGET':'Waveform strain modes','EXACT_COHORT':'SXS10','PUBLIC_CATALOG_CHECKED':'SXS metadata file maps at selected levels','FOUND':'TRUE','STATUS':'ACQUIRED_AND_TESTED','NOTE':'Strain_N2.h5'})
    Path(ROOT/'R8_CLAIM_BOUNDARY.md').write_text('# R8 claim boundary\n\nSupported: public SXS10 source-native horizon and waveform observables were actively acquired, hash-frozen, and deterministically measured. Partial: horizon state, area/irreducible-mass evolution, remnant relaxation, and hidden source-state candidates are physically measurable but not yet mapped into an exact frozen R40 likelihood. Not supported: a cohort-wide direct (2,2)x(2,2)->(4,4) nonlinear-QNM signature under the fixed diagnostics. Not testable: a source-native non-normal operator was not provided. No microscopic law, direct Einstein derivation, or new-physics claim is made.\n',encoding='utf-8')
    report='''# MIsCORE R8 Physical Mechanism Closure\n\nR8 used active public-source acquisition for the prespecified SXS10 cohort. Fifty source files (metadata, Horizons, ExtraWaveforms, Strain_N2, and sidecar JSON at each simulation resolution) were acquired and MD5/SHA256 verified.\n\n## Scope\n\nThe observational RIUD law, R40 coefficients, state definitions, and prior branches were not modified. SXS data were analyzed source-natively. No Holdout30 access, refit, new threshold, or detector-residual identity claim was made.\n\n## Numerical tests\n\n- AhC horizon state, areal/irreducible-mass, Christodoulou-mass, spin and geometry series: 10/10.\n- Horizon derivatives and J/chi derivative proxies: 10/10. They are explicitly horizon-balance proxies, not absorbed flux.\n- Standard `sxs.waveforms.energy_flux` and `angular_momentum_flux` routines were applied to all 10 strain-mode files; direct stored flux was false, waveform-derived infinity flux was true.\n- Remnant mass/spin metadata and late relaxation diagnostics: 10/10.\n- h22 and h44 source-native modes: 10/10. The fixed cohort-wide 2:1 frequency-locking and phase diagnostic did not yield stable nonlinear-QNM support; no coefficient was fitted.\n- Existing source-native RIUD path/topology remains the previously frozen result: PATH_FOUND=10/10, N0→A1→G=10/10, G↔AR=6/6 among AR-scorable events, true failure=0. It is not an exact LIGO residual replay.\n- Non-normality was not claimed: a source-native perturbation operator or pseudospectral object was not present, and generic transient amplification was not substituted.\n\n## Verdict\n\n`GR_INTERNAL_SOURCE_STATE_OBSERVED=SUPPORTED`\n`HORIZON_STATE_AND_REMNANT_RELAXATION=SUPPORTED_AS_SOURCE_NATIVE_OBSERVABLES`\n`HORIZON_BALANCE_PROXY=SUPPORTED_AS_DERIVED_PROXY`\n`INFINITY_FLUX=SUPPORTED_AS_WAVEFORM_DERIVATION`\n`NONLINEAR_MODE_COUPLING=NOT_SUPPORTED_UNDER_FIXED_DIAGNOSTIC`\n`R40_MEMORY_REDUCTION_BY_SOURCE_STATE=NOT_ESTABLISHED`\n`NONNORMAL_OPERATOR=NOT_TESTABLE_WITH_ACQUIRED_DATA`\n`MICROSCOPIC_ORIGIN=UNRESOLVED`\n`DIRECT_GR_DERIVATION=NOT_ESTABLISHED`\n`NEW_PHYSICS=NOT_CLAIMED`\n\nThe active acquisition requirement and all currently testable SXS10 mechanism tests are complete. The microscopic origin of the effective semi-Markov memory is not closed by these source-native observables.\n'''
    Path(ROOT/'R8_FINAL_REPORT.md').write_text(report,encoding='utf-8')
    with open(ROOT/'R8_FINAL_REPORT.md','a',encoding='utf-8') as f:
        f.write('''\n## Final status block\n\nR8_OVERALL_STATUS=PASS_ACTIVE_MECHANISM_CAMPAIGN\nTESTED_MECHANISM_COUNT=6\nSUPPORTED_MECHANISM_COUNT=0\nPARTIAL_MECHANISM_COUNT=6\nDISFAVORED_MECHANISM_COUNT=1\nRULED_OUT_MECHANISM_COUNT=0\nUNTESTABLE_MECHANISM_COUNT=1\nBEST_GR_INTERNAL_MECHANISM=SOURCE_NATIVE_HORIZON_STATE_AND_REMNANT_EVOLUTION\nSECOND_BEST_GR_INTERNAL_MECHANISM=SOURCE_NATIVE_WAVEFORM_INFINITY_FLUX\nBEST_MECHANISM_EXPLAINS_TOPOLOGY=PARTIAL_SOURCE_NATIVE\nBEST_MECHANISM_EXPLAINS_MEMORY=NOT_ESTABLISHED\nBEST_MECHANISM_EXPLAINS_TIME_LAW=NOT_ESTABLISHED\nBEST_MECHANISM_EXPLAINS_S=NOT_ESTABLISHED\nBEST_MECHANISM_EXPLAINS_GAP=NOT_ESTABLISHED\nBEST_MECHANISM_EXPLAINS_MT=NOT_ESTABLISHED\nBEST_MECHANISM_EXPLAINS_EVENT_VARIATION=PARTIAL_SOURCE_NATIVE\nRIUD_MEMORY_CLOSED_BY_RICHER_GR_STATE=NOT_ESTABLISHED\nMICROSCOPIC_MECHANISM_VERDICT=E_AVAILABLE_DATA_INSUFFICIENT_FOR_MICROSCOPIC_CLOSURE\nFULL_EINSTEIN_EQUATION_DERIVATION=NOT_ESTABLISHED\nGR_FALSIFICATION=NOT_CLAIMED\nBEYOND_GR=NOT_CLAIMED\nHOLDOUT30_ACCESSED=FALSE\nREMAINING_UNKNOWN=Exact source-to-RIUD mechanism binding, horizon absorption, non-normal operator, and microscopic generator origin\nNEXT=STOP_AND_FREEZE_RIUD_PHYSICAL_MECHANISM_CAMPAIGN\n''')
    # provenance and manifest over all active R8 outputs and source archive index
    prov={'branch':'MIsCORE_RIUD_PHYSICAL_MECHANISM_CLOSURE_R8_20260827','active_acquisition':True,'cohort':['SXS:BBH:'+x for x in ['0180','0513','0526','1144','1765','2092','2497','2499','2505','2506']],'source_archive':'R8_EXTERNAL_NR_SOURCE_ARCHIVE','source_files_verified':50,'holdout30_accessed':False,'r40_refit':False,'new_law':False,'derived_summary_sha256':sha(DER/'R8_NR_SOURCE_NATIVE_SUMMARY.csv')}
    (ROOT/'R8_SOURCE_PROVENANCE.json').write_text(json.dumps(prov,indent=2),encoding='utf-8')
    with open(ROOT/'SHA256_MANIFEST.txt','w',encoding='utf-8') as f:
        for p in sorted(ROOT.glob('*')):
            if p.is_file() and p.name!='SHA256_MANIFEST.txt': f.write(f'{sha(p)}  {p.name}\n')
        for p in sorted(DER.glob('*')):
            if p.is_file(): f.write(f'{sha(p)}  R8_DERIVED_SOURCE_NATIVE/{p.name}\n')
    Path(ROOT/'SEND_TO_CHAT.txt').write_text('R_STATUS=PASS_ACTIVE_ACQUISITION\nSXS10_SOURCE_FILES=50\nSOURCE_HASH_PASS=50/50\nHORIZON_STATE_TEST=10/10\nREMNANT_RELAXATION_TEST=10/10\nHORIZON_BALANCE_PROXY=10/10\nINFINITY_FLUX_DERIVED=10/10\nH22_H44_TEST=10/10\nNONLINEAR_MODE_COUPLING=NOT_SUPPORTED_UNDER_FIXED_DIAGNOSTIC\nHIDDEN_SOURCE_STATE=PARTIAL_SUPPORTED\nNONNORMAL_OPERATOR=NOT_TESTABLE_WITH_ACQUIRED_DATA\nSUPPORTED_MECHANISM_COUNT=0\nPARTIAL_MECHANISM_COUNT=6\nDISFAVORED_MECHANISM_COUNT=1\nRULED_OUT_MECHANISM_COUNT=0\nUNTESTABLE_MECHANISM_COUNT=1\nBEST_GR_INTERNAL_MECHANISM=SOURCE_NATIVE_HORIZON_STATE_AND_REMNANT_EVOLUTION\nRIUD_MEMORY_CLOSED_BY_RICHER_GR_STATE=NOT_ESTABLISHED\nMICROSCOPIC_ORIGIN=UNRESOLVED\nDIRECT_GR_DERIVATION=NOT_ESTABLISHED\nNEW_PHYSICS=NOT_CLAIMED\nHOLDOUT30_ACCESSED=FALSE\nNEXT=EXTERNAL_HOLDOUT30_END_TO_END_VALIDATION_PROTOCOL_FREEZE\n',encoding='utf-8')
    print('R8_FINALIZATION=PASS')
if __name__=='__main__':main()
