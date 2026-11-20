# Integrated relation prediction and missingness completion

This R2 release adds a fixed-specification prediction audit to the integrated
branch relation package. The preceding conditional branch definitions were
not changed. Existing observed family labels and existing GAP landmarks are
the comparison targets.

## Accounting

- authoritative PATH_FOUND: 98
- authoritative NO_PATH: 1 (`GW241230_233618`)
- event rows in audit including NO_PATH: 99
- S-missing within PATH_FOUND: 2 (`GW150914_095045`, `GW231008_142521`)
- strict complete S+K1+K2+K5+ABC rows: 16

## Fixed branch agreement

               TARGET                                               METRIC  N_AVAILABLE  N_AGREE  AGREEMENT_RATE
                  MAG                           IN_SAMPLE_BRANCH_AGREEMENT           98     94.0        0.959184
                  MAG                 LEAVE_ONE_EVENT_OUT_BRANCH_AGREEMENT           98     92.0        0.938776
                SHAPE                           IN_SAMPLE_BRANCH_AGREEMENT           98     77.0        0.785714
                SHAPE                 LEAVE_ONE_EVENT_OUT_BRANCH_AGREEMENT           96     66.0        0.687500
          GAP_SIDE_T0                           IN_SAMPLE_BRANCH_AGREEMENT           96     96.0        1.000000
          GAP_SIDE_T0                 LEAVE_ONE_EVENT_OUT_BRANCH_AGREEMENT           96     95.0        0.989583
    GAP_ORDER_MAXFLOW                           IN_SAMPLE_BRANCH_AGREEMENT           96     94.0        0.979167
    GAP_ORDER_MAXFLOW                 LEAVE_ONE_EVENT_OUT_BRANCH_AGREEMENT           96     93.0        0.968750
             GAP_TIME IN_SAMPLE_SIGN_AGREEMENT_OF_MEDIAN_BRANCH_PREDICTION           96     96.0        1.000000
             GAP_TIME                   LEAVE_ONE_EVENT_OUT_SIGN_AGREEMENT           96     95.0        0.989583
STRICT_ALL_AXIS_SCOPE                         S_AND_K1_K2_K5_ABC_AVAILABLE           16      NaN             NaN

The in-sample rows are descriptive concordance. The LOO rows use the same
fixed branch specification while excluding the event being scored; they are
not a blind external validation set.

## Missingness handling

- S is never imputed.
- The two S-missing events use a pre-specified no-S MAG fallback where the
  primary S branch is unavailable; SHAPE does not require S.
- `GW231008_142521` has no ABC/GAP landmark and is not scored for GAP.
- `GW231206_233901` is a PATH_FOUND row with missing ABC/GAP fields and is
  retained; family-only predictions are recorded where defined.
- `GW241230_233618` is the authoritative NO_PATH event and is retained as
  `NO_PATH_NOT_SCORABLE`, not silently removed from the 99-event accounting.
- K1/K2 are not manufactured outside their existing branch-local N=16 support.

## Interpretation

MAG and GAP-direction branches show high descriptive concordance under the
fixed lookup, while SHAPE is weaker in LOO. This is evidence that the branch
structure can reproduce existing observed labels/directions, not evidence of
causality or a final predictive law. The full all-axis relation remains
coverage-limited because K1/K2 exist for only 16 events.

No new map, path, null, refit, or Holdout30 access occurred.
