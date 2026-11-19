# Effective GAP-memory equation

The frozen empirical state generator is

```text
d pi/du = pi Q
Q_ij = p_ij, i != j
Q_ii = -sum(j != i) Q_ij
logit(p_ij,e) = alpha_ij + beta_RMS (RMS_e - mean(RMS))
```

The GAP audit adds a descriptive, piecewise memory contrast rather than a newly fitted law:

```text
M_e(u) = M_pre,e,                         100*u < 41.8624764371929
         M_post,e,                        100*u >= 41.8624764371929
```

Across 96 events, the mean post-minus-pre memory magnitude is `+0.24802386879217775`; the post/pre population mean ratio is approximately `1.69`, with 91/96 events positive. This can be represented as an effective candidate multiplier `g_post ≈ 1.69`, but `g_post` is descriptive and has not been inserted into or refit against canonical R40.

## Mechanism boundary

The evidence supports a GAP-adjacent regime change in memory strength. It does not identify the microscopic carrier. Radiation, QNM relaxation, and horizon variables remain unbound to the 96 R40 rows in the available source closure.

```text
GAP_MEMORY_EFFECT=SUPPORTED_DESCRIPTIVELY
GAP_MODULATED_GENERATOR= CANDIDATE_ONLY
RADIATIVE_QNM_HORIZON_ORIGIN=UNRESOLVED
FUNDAMENTAL_GR_DERIVATION=NOT_CLAIMED
```
