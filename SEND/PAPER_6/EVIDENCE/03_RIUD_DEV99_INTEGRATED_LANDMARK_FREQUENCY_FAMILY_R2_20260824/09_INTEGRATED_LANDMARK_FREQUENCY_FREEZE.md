# Integrated landmark + frequency family freeze

R_STATUS=FROZEN
STAGE=RIUD_DEV99_INTEGRATED_LANDMARK_FREQUENCY_FAMILY_R2_20260824
COHORT=EXACT_PATH_X_A2_INTERSECTION
N_EVENTS=96

## Inputs frozen

The integrated family input contains existing frozen numerical descriptors only:

- frequency magnitude: span, total variation, absolute net change, rate MAD
- frequency shape: `f_shape_00..f_shape_31`
- GAP, T0, MT, PEAK, MAX_FLOW
- available W-boundary coordinates and support spans
- A2 descriptive score and midpoint

ABC, S, legacy H labels, width fields, node count, transition fingerprints, source paths, and hashes were not used as clustering inputs.

## Family result

- selected K=2 by the deterministic K=2..8 scan with minimum-family-size/stability gates
- `INT_1=63`
- `INT_2=33`

## Missing-field boundary

The exact A2 event-level source has incomplete values for `W2_START_NATIVE`, `W2_END_NATIVE`, `W4_START_NATIVE`, and `W4_END_NATIVE` in a subset of the 96-event intersection. Those values were not imputed or reconstructed; the complete available landmark columns are recorded in `01_INTEGRATED_INPUT_AUDIT.csv`.

The earlier frequency-only MAG/SHAPE results remain separate and are not overwritten. This integrated family is an exploratory cross-axis census, not a replacement for the frozen RIUD scientific law or existing canonical labels.

NEW_NODE=FALSE
NEW_PATH=FALSE
NEW_THRESHOLD=FALSE
NEW_S=FALSE
HOLDOUT30_ACCESSED=FALSE
