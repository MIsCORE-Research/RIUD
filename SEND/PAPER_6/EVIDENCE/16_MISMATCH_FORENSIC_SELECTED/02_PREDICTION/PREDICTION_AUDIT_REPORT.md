# Integrated prediction / missingness audit

This audit uses the existing 98 PATH_FOUND event rows plus the authoritative
one NO_PATH row. It evaluates fixed branch lookups from the preceding
exploratory relation search; it does not refit, average axes, generate a new
map/path, or impute missing S/ABC/GAP values.

## Fixed branch inputs

- MAG primary: `S_RANK_BIN + frequency_span_hz_RANK_BIN + f_total_variation_hz_RANK_BIN`.
- MAG S-missing fallback: `frequency_span_hz_RANK_BIN + f_total_variation_hz_RANK_BIN + network_z_median_RANK_BIN`.
- SHAPE: `f_turns_RANK_BIN + transition_entropy_RANK_BIN + network_z_median_RANK_BIN`.
- GAP side/order: existing `FREQ_MAG + FREQ_SHAPE + ABC` family branch, with family-only fallback when ABC is absent.
- GAP numeric check: branch median of existing `GAP_TIME`; sign is compared with existing `t0=0`.

The in-sample rates are descriptive branch concordance. A fixed-specification
leave-one-event-out lookup is also reported; it is less optimistic but still
does not include a blind external validation set. These results answer whether
the assembled branch structure reproduces the existing observed
labels/directions.

## Accounting

- PATH_FOUND: 98
- NO_PATH: 1
- event rows evaluated: 99
- S missing among PATH_FOUND rows: 2
- ABC missing among PATH_FOUND rows: 2
- GAP landmark missing among PATH_FOUND rows: 2
- strict all-axis availability (S+K1+K2+K5+ABC): 16

## Agreement

               TARGET                                               METRIC  N_AVAILABLE N_AGREE AGREEMENT_RATE
                  MAG                           IN_SAMPLE_BRANCH_AGREEMENT           98      94       0.959184
                  MAG                 LEAVE_ONE_EVENT_OUT_BRANCH_AGREEMENT           98      92       0.938776
                SHAPE                           IN_SAMPLE_BRANCH_AGREEMENT           98      77       0.785714
                SHAPE                 LEAVE_ONE_EVENT_OUT_BRANCH_AGREEMENT           96      66         0.6875
          GAP_SIDE_T0                           IN_SAMPLE_BRANCH_AGREEMENT           96      96            1.0
          GAP_SIDE_T0                 LEAVE_ONE_EVENT_OUT_BRANCH_AGREEMENT           96      95       0.989583
    GAP_ORDER_MAXFLOW                           IN_SAMPLE_BRANCH_AGREEMENT           96      94       0.979167
    GAP_ORDER_MAXFLOW                 LEAVE_ONE_EVENT_OUT_BRANCH_AGREEMENT           96      93        0.96875
             GAP_TIME IN_SAMPLE_SIGN_AGREEMENT_OF_MEDIAN_BRANCH_PREDICTION           96      96            1.0
             GAP_TIME                   LEAVE_ONE_EVENT_OUT_SIGN_AGREEMENT           96      95       0.989583
STRICT_ALL_AXIS_SCOPE                         S_AND_K1_K2_K5_ABC_AVAILABLE           16    <NA>           <NA>

## Missingness rule

The two S-missing rows are never imputed. MAG uses the fixed no-S fallback
only when its primary S branch cannot be evaluated; SHAPE does not require S.
GAP is unavailable when its observed GAP landmark is missing. The NO_PATH row
is retained and marked not scorable. K1/K2 are not manufactured for the 82
rows outside their branch-local coverage.

## Claim boundary

The result is branch/ direction concordance with existing observations, not
proof of out-of-sample prediction or causality. The strict formula containing
all of S, K1, K2, K5, ABC and geometry has only 16 complete rows in
this table; missingness is part of the result, not silently filled.
