# Prior source-native law overlap cross-check

The overlap is MT in [-0.1, 0.03] and is audited only after the current law fit. The earlier RMS branch is not used as an input, predictor, or selection criterion.

                   SOURCE            OBJECT  ROWS  EVENTS    MT_MIN   MT_MAX   VALUE_1   VALUE_2                                                                               NOTE
         PRIOR_RMS_BRANCH           PROFILE  2528      96 -0.099872 0.029998  0.149597 -0.035000                 Read-only prior source-native result; not used in current law fit.
         PRIOR_RMS_BRANCH        TRANSITION  2529      96 -0.100000 0.029946 -0.050501  0.011085                              Spearman(RMS_RATIO_FROM, TRANSITION) on overlap only.
         PRIOR_RMS_BRANCH EVENTWISE_PROFILE  2496      96 -0.100000 0.025000  0.149597  0.145740                  Maximum across MT points of event-level Spearman; N=96 per point.
CURRENT_SOURCE_NATIVE_LAW        TRANSITION  1248      96 -0.095000 0.025000  0.448051 -0.790723 OOF delta for L1_FFT_CENTROID_HZ; source-native recomputation from current branch.

Earlier branch headline: MT_LOCAL_BEST_RHO=0.14959692320080503, MT_LOCAL_BEST_MT_TAU=-0.03499999999999995
Event-level correction: max rho=0.149596923, p=0.14574 at MT=-0.035; this is not significant after treating events as the unit.
Current source-native candidate: L1_FFT_CENTROID_HZ; overlap OOF delta vs state+MT=0.448051232.

The two branches use different raw state targets and bin contracts, so this is a consistency/provenance audit, not a pooled likelihood comparison.
SXS_USED=False; HOLDOUT30_ACCESSED=False.