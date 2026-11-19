# DEV99 Frequency × ABC Nonlinear-Phenotype Side Analysis

Status: descriptive side analysis; no new law, threshold, refit, null, or node/path discovery.

## Scope

- Frequency trajectory source: 98 events.
- Exact dynamics join: 97 events.
- ABC A/B/C joint analysis: 89 events; 7 OTHER events excluded.
- Raw amplitude/energy exact join: 12 events.
- Reference landmarks: existing GAP, t0, MT, MAX_FLOW, and PEAK fields.

## Frequency family counts

| family | N |
|---|---:|
| FREQ_MAG_1 | 34 |
| FREQ_MAG_2 | 64 |
| FREQ_SHAPE_1 | 63 |
| FREQ_SHAPE_2 | 35 |

## ABC within frequency family

| family | ABC | N | median MAX_FLOW (ms) | median span (Hz) | median variation (Hz) | median transitions | median nodes |
|---|---|---:|---:|---:|---:|---:|---:|
| MAG_1 | A | 27 | 22.50 | 100 | 130 | 13.0 | 14.0 |
| MAG_1 | B | 2 | -2.50 | 135 | 150 | 13.5 | 14.5 |
| MAG_1 | C | 4 | -10.00 | 85 | 185 | 15.0 | 16.0 |
| MAG_2 | A | 47 | 27.50 | 40 | 50 | 9.0 | 10.0 |
| MAG_2 | B | 3 | -2.50 | 50 | 100 | 15.0 | 16.0 |
| MAG_2 | C | 6 | -6.25 | 40 | 50 | 10.0 | 11.0 |
| SHAPE_1 | A | 47 | 22.50 | 70 | 80 | 10.0 | 11.0 |
| SHAPE_1 | B | 2 | -2.50 | 135 | 150 | 13.5 | 14.5 |
| SHAPE_1 | C | 7 | -5.00 | 40 | 70 | 13.0 | 14.0 |
| SHAPE_2 | A | 27 | 22.50 | 60 | 70 | 10.0 | 11.0 |
| SHAPE_2 | B | 3 | -2.50 | 50 | 100 | 15.0 | 16.0 |
| SHAPE_2 | C | 3 | -12.50 | 70 | 140 | 10.0 | 11.0 |

## Association checks

```text
FREQ_MAG × ABC chi-square p = 0.9675422104
FREQ_SHAPE × ABC chi-square p = 0.5086808166
FREQUENCY_DIRECTION × ABC chi-square p = 0.0646727855
```

Direction counts (A/B/C): rising 44/2/6, falling 21/0/2, flat 9/3/2.

## Raw cross-check

Only 12 events have exact joins to the existing raw feature matrix. Median post-minus-pre envelope change was 0 for A (N=10), 0 for B (N=1), and approximately 0 for C (N=1). The B/C amplitude result is therefore not generalizable.

## Interpretation

Frequency magnitude and shape are distinct descriptive axes. MAX_FLOW timing separates ABC more clearly than MT, while frequency families describe within-ABC trajectory complexity. A localized nonlinear-like phenotype is present in some small cells, but direct parent/child QNM coupling is not established.

```text
DIRECT_NONLINEAR_MODE_COUPLING = NOT_ESTABLISHED
NONLINEAR_PHENOTYPE = DESCRIPTIVE_ONLY
NEW_S_OR_LAW = FALSE
NEW_THRESHOLD = FALSE
NEW_NODE_PATH_DISCOVERY = FALSE
HOLDOUT30_ACCESSED = FALSE
```

## Source files

- `E:\RIUD_ACTIVE_20260808\RIUD_DEV99_FREQUENCY_ONLY_MORPHOLOGY_CENSUS_R0_20260824\06_FREQUENCY_ONLY_ASSIGNMENTS.csv`
- `E:\RIUD_ACTIVE_20260808\RIUD_DEV99_FREQUENCY_MAG_SHAPE_CENSUS_R0_20260824\07_FREQ_MAG_SHAPE_ASSIGNMENTS.csv`
- `E:\RIUD_ACTIVE_20260808\RIUD_DEV99_DYNAMICS_REPRESENTATION_FREEZE_R10J0R2_PCA90_FIX_PAR16_20260811\01_FREEZE\R10J0R2_EVENT_DYNAMICS_FEATURES.csv`
- `E:\RIUD_ACTIVE_20260808\RIUD_ABC_INTEGRATED_MAP_LAW_LEDGER_R0_20260825\ABC_96_EVENT_INTEGRATED_LEDGER.csv`

## Frequency-direction turn ↔ GAP-adjacent transition ↔ node-link audit

Using the existing transition rows and existing event GAP bounds, no new node or transition rows were generated. The transition table contains 985 rows; 965 rows bind to the event landmark table. A frequency-sign change relative to the preceding transition was used only as a descriptive direction-turn marker.

```text
BOUND_TRANSITION_ROWS = 965
SIGN_TURN_ROWS = 439
EVENTS_WITH_SIGN_TURNS = 92
SIGN_TURNS_WITHIN_10MS_OF_GAP_CENTER = 98
EVENTS_WITH_SIGN_TURN_WITHIN_10MS = 72
TURN_TO_GAP_DISTANCE_MEDIAN = 2.918 ms
ALL_TRANSITION_TO_GAP_DISTANCE_MEDIAN = 1.822 ms
```

The sign-turn rows are therefore present near the GAP in many events, but the simple 10-ms proximity count is not by itself evidence that the GAP causes the turn: ordinary transitions can be even closer under this distance definition. The result supports a structural co-location/association audit, not a causal or nonlinear-mode claim.

```text
FREQUENCY_TURN_NEAR_GAP = DESCRIPTIVELY_PRESENT
GAP_ADJACENT_NODE_LINK = OBSERVED_IN_EXISTING_TRANSITION_ROWS
CAUSAL_INTERPRETATION = NOT_ESTABLISHED
DIRECT_NONLINEAR_MODE_COUPLING = NOT_ESTABLISHED
```

## Stratified frequency-direction turn / GAP adjacency

The same existing sign-turn and 10-ms GAP-center rule was stratified by ABC and frequency family.

```text
ABC=A: turns=330, near-GAP turns=72, near-turn rate=0.2182, near-GAP events=52/74
ABC=B: turns=29,  near-GAP turns=8,  near-turn rate=0.2759, near-GAP events=5/5
ABC=C: turns=66,  near-GAP turns=12, near-turn rate=0.1818, near-GAP events=9/10
```

By frequency magnitude:

```text
MAG_1/A: 26/143 = 0.1818
MAG_1/B:  3/13  = 0.2308
MAG_1/C:  6/34  = 0.1765
MAG_2/A: 46/187 = 0.2460
MAG_2/B:  5/16  = 0.3125
MAG_2/C:  6/32  = 0.1875
```

By frequency shape:

```text
SHAPE_1/A: 51/218 = 0.2339
SHAPE_1/B:  3/13  = 0.2308
SHAPE_1/C:  9/50  = 0.1800
SHAPE_2/A: 21/112 = 0.1875
SHAPE_2/B:  5/16  = 0.3125
SHAPE_2/C:  3/16  = 0.1875
```

The B rates are based on only five events and are unstable. No subgroup-specific causal or nonlinear claim is made.

## GAP two-sided frequency convergence audit

The existing 32-bin absolute-frequency profile was sampled at the existing event GAP coordinate after deterministic linear placement over the event's frozen `time_start_s`–`time_end_s` support. No new GAP or node was selected.

```text
EVENTS_WITH_TWO_SIDED_PROFILE_SAMPLE = 96
MEDIAN_ABS_F_LEFT_MINUS_F_RIGHT = 2.258065 Hz
F_LEFT/F_RIGHT_DIFFERENCE <= 10 Hz = 73/96
OPPOSITE_SLOPE_SIGN = 0/96
```

The stored profiles contain plateaus and are coarse 32-bin summaries; the median left/right slope values are both 0 under the native sampled-bin calculation. Therefore the data show a descriptive tendency toward similar left/right frequency values at the GAP sample, but do not establish convergent slopes or a unique frequency-contact point. This is not evidence of nonlinear coupling.

## Native pre-robust path GAP contact audit

The pre-robust `EXPANDED_EXACT_ORIGINAL_PATH.csv` rows were used where non-empty, selecting the nearest native path row on each side of the frozen GAP bounds. This is distinct from the robust 32-bin profile audit.

```text
EVENTS_WITH_NATIVE_TWO_SIDED_ROWS = 93
MEDIAN_ABS_F_LEFT_MINUS_F_RIGHT = 0 Hz
DELTA_F <= 10 Hz = 65/93
OPPOSITE-SIGN_CONVERGENT_SLOPES = 3/93
```

The native rows frequently have equal/plateau frequency values at the two selected sides, but genuine opposite-sign slope convergence is rare under the fixed nearest-row rule. Thus the original data do not support a general claim that two frequency flows converge to a single GAP contact.
