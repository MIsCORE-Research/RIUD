# Frequency MAG/SHAPE morphology freeze

R_STATUS=FROZEN
STAGE=RIUD_DEV99_FREQUENCY_MAG_SHAPE_CENSUS_R0_20260824
DEV99_TOTAL=99
PATH_FOUND=98
NO_PATH_EVENT=GW241230_233618

## Frozen axes

`FREQ_MAG` and `FREQ_SHAPE` are retained as two separate frequency-only axes.

- `FREQ_MAG`: frequency movement magnitude only: span, total variation, absolute net change, and rate MAD.
- `FREQ_SHAPE`: within-event normalized frequency trajectory profile `f_shape_00..f_shape_31` only.
- Width fields: not used.
- Node count: not used.
- Transition fingerprint: not used.
- ABC/A2/S/legacy H labels: not used.

## Frozen family counts

- `FREQ_MAG`: K=2; `FREQ_MAG_1=34`, `FREQ_MAG_2=64`.
- `FREQ_SHAPE`: K=2; `FREQ_SHAPE_1=63`, `FREQ_SHAPE_2=35`.

The K value was selected by the frequency-only K=2..8 scan with the predeclared minimum-family-size/stability gates. It was not supplied as an external classification label.

## Interpretation boundary

The MAG and SHAPE axes are not identical classifications. Their cross-tab is preserved in `09_FREQ_MAG_X_SHAPE_CROSSTAB.csv`. The earlier `RIUD_DEV99_FREQUENCY_ONLY_MORPHOLOGY_CENSUS_R0_20260824` 90/8 result used a frequency fusion view and is retained as a superseded diagnostic, not as the pure MAG result.

NEW_NODE=FALSE
NEW_PATH=FALSE
NEW_THRESHOLD=FALSE
HOLDOUT30_ACCESSED=FALSE
