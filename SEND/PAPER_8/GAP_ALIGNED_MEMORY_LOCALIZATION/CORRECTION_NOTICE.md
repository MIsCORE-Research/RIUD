# Coordinate correction notice

The file `GAP_ALIGNED_R40_MEMORY_ROWS_NATIVE.csv` and the associated native-delay calculation are withdrawn. `U_SOURCE` is defined by the R40 producer as `GLOBAL_MID_PCT / 100`, not as `LATENT_COORD`; multiplying it by `GLOBAL_SCALE` and adding `GLOBAL_SHIFT` was therefore invalid.

The valid GAP-relative analysis uses the frozen global progression coordinate:

```text
RELATIVE_GAP_PROGRESS_PCT = 100 * U_SOURCE - GAP_MID_GLOBAL_PCT
GAP_MID_GLOBAL_PCT = 41.8624764371929
```

All final claims must use this corrected coordinate only. The valid eventwise post-minus-pre memory contrast is mean `+0.24802386879217775`, median `+0.18107055419088022`, with 91/96 events positive and 9999-event bootstrap 95% CI `[+0.21230465, +0.28602148]`.
