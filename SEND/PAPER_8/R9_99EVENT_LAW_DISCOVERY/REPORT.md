# Source-native physical transition-law discovery

This branch uses only the 96-event GWOSC raw W10 profile and the new raw-only transition table. SXS, historical node/path/state/W/GAP/S/R40 results, and Holdout30 were not read.

- Common events: 96; transition rows: 23904.
- Raw support: -300 to 300 ms; W10 only.
- Local source value: linear interpolation at raw offset `MT_MID * GLOBAL_SCALE * 1000` ms.
- OOF: 5 deterministic event folds; train-only standardization; no frozen-law refit.

## Candidate screen

                    FEATURE  VALID_ROWS  VALID_EVENTS  OOF_STATE_LL  OOF_STATE_MT_LL  OOF_FEATURE_LL  OOF_DELTA_VS_STATE  OOF_DELTA_VS_STATE_MT  ALL_FOLDS_PRESENT
         L1_FFT_CENTROID_HZ        7649            96  -4837.915962     -4838.275104    -4834.493870            3.422092               3.781234               True
                 H1_P20_100        7649            96  -4837.915962     -4838.275104    -4838.066336           -0.150374               0.208767               True
     H1_FDOT_PHASE_HZ_PER_S        7649            96  -4837.915962     -4838.275104    -4838.090236           -0.174274               0.184868               True
NETWORK_FDOT_PHASE_HZ_PER_S        7649            96  -4837.915962     -4838.275104    -4838.622174           -0.706213              -0.347071               True
      H1_LOGAMP_SLOPE_PER_S        7649            96  -4837.915962     -4838.275104    -4838.724616           -0.808654              -0.449512               True
     L1_FDOT_PHASE_HZ_PER_S        7649            96  -4837.915962     -4838.275104    -4838.985876           -1.069914              -0.710772               True
                H1_P250_512        7649            96  -4837.915962     -4838.275104    -4839.491345           -1.575383              -1.216241               True
                H1_P100_250        7649            96  -4837.915962     -4838.275104    -4839.599858           -1.683897              -1.324755               True
              L1_F_PHASE_HZ        7649            96  -4837.915962     -4838.275104    -4839.601123           -1.685161              -1.326020               True
      L1_LOGAMP_SLOPE_PER_S        7649            96  -4837.915962     -4838.275104    -4839.699076           -1.783114              -1.423972               True
              H1_F_PHASE_HZ        7649            96  -4837.915962     -4838.275104    -4840.511865           -2.595903              -2.236761               True
    NETWORK_FFT_CENTROID_HZ        7649            96  -4837.915962     -4838.275104    -4840.720598           -2.804636              -2.445494               True
  NETWORK_COMPLEX_COHERENCE        7649            96  -4837.915962     -4838.275104    -4840.995036           -3.079074              -2.719932               True
         H1_FFT_CENTROID_HZ        7649            96  -4837.915962     -4838.275104    -4841.425148           -3.509186              -3.150044               True
         NETWORK_F_PHASE_HZ        7649            96  -4837.915962     -4838.275104    -4842.651431           -4.735469              -4.376328               True
                     H1_RMS        7649            96  -4837.915962     -4838.275104    -4842.675717           -4.759755              -4.400613               True
                L1_P100_250        7649            96  -4837.915962     -4838.275104    -4845.442389           -7.526427              -7.167285               True
                 L1_P20_100        7649            96  -4837.915962     -4838.275104    -4847.200758           -9.284796              -8.925654               True
                L1_P250_512        7649            96  -4837.915962     -4838.275104    -4853.088453          -15.172492             -14.813350               True
                     L1_RMS        7649            96  -4837.915962     -4838.275104    -4858.046208          -20.130246             -19.771104               True

## Selected law

Selected source-native observable: `L1_FFT_CENTROID_HZ`.

`logit P(CHANGE=1) = state-specific intercepts + beta_MT * z(MT_FROM) + beta_X * z(X_raw)`.

                TERM  COEFFICIENT
           INTERCEPT     0.547464
            STATE_S1     0.584549
            STATE_S2     0.170979
            STATE_S3     0.423357
           MT_FROM_Z     0.004526
L1_FFT_CENTROID_HZ_Z    -0.086567

## Null and claim boundary

Event-binding permutation: 999 fixed-seed permutations; empirical p=0.103.
LOEO positive held events: 51/96.
Verdict: `NO_REPRODUCIBLE_SOURCE_NATIVE_LAW_ESTABLISHED`.

This is an effective source-native transition-propensity candidate, not a fundamental microscopic law and not a continuous-time CTMC claim.

HOLDOUT30_ACCESSED=False; SXS_USED=False; HISTORICAL_S_R40_USED=False.