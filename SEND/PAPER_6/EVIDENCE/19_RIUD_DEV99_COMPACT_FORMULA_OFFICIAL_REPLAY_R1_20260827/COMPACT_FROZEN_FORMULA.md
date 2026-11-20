# DEV99 Compact Frozen Formula

This is a compact transcription of the final DEV99 rule/model lock used by
the R9 Holdout5 official replay. It is an application contract, not a new
fit and not a new scientific law.

## Frequency families

`FREQ_MAG_FAMILY` is K=2 on the frozen frequency-variation representation:
`frequency_span_hz`, `frequency_total_variation_hz`, `abs_net_change_hz`, and
`rate_mad_hz_per_s`.

`FREQ_SHAPE_FAMILY` is K=2 on the within-event normalized profile
`f_shape_00` through `f_shape_31`.

## DEV99 fixed-form Holdout5 predictor

For either model, `p = sigmoid(logit)`. Family 2 is selected when `p >= 0.5`;
otherwise family 1 is selected. Inputs are standardized with the DEV99-only
means and standard deviations stored in `DEV99_FIXED_FORM_MODEL_R5`.

MAG:

```text
logit_mag = 0.6252753405791113
          + 0.11190848908902203*S_K5
          - 0.25829593337044654*f_total_variation_hz
          - 0.04075116908267855*network_z_median
          - 0.055737569477874754*f_turns
          - 0.1287602615712552*support_complexity
```

SHAPE:

```text
logit_shape = -0.596964714165367
            + 0.08130927169026472*f_turns
            - 0.07108151393761716*transition_entropy
            - 0.050562664183970665*network_z_median
            + 0.0012501039571087187*support_complexity
            - 0.004270395289538118*MAG2
            + 0.012219925507401417*ABC_B
            - 0.006990858295139147*ABC_C
            - 0.01462797851438039*ABC_OTHER
            + 0.019733275854400652*MAG2_X_ABC_B
            - 0.012084775199117666*MAG2_X_ABC_C
            - 0.01462797851438039*MAG2_X_ABC_OTHER
```

## ABC and GAP branch

```text
A = GAP_TIME < T0 < MAX_FLOW
B = GAP_TIME < MAX_FLOW < T0
C = MAX_FLOW < GAP_TIME < T0
OTHER = all other or unavailable orderings

GAP_TRIGGER = MAG2 AND (ABC in {C, OTHER}) AND (path_nodes <= 9)
```

The GAP expression is a forensic branch flag, not a causal GAP law.

## R9 scope

R9 reuses the R7 result table. It reports fixed-form predictions and the
ABC/GAP rule applications. It does not establish independent Holdout5 family
labels or MAG/SHAPE observational MATCH/TOTAL values.

`NO_REFIT=TRUE`, `NO_NEW_MAP=TRUE`, `NO_NEW_PATH=TRUE`, and
`HOLDOUT30_ACCESSED=FALSE`.
