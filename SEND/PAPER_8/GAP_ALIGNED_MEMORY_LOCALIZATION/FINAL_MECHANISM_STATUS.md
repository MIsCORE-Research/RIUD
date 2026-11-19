# Final mechanism status

## State equation

The independent data-only discovery produced six states (`S0`–`S5`) and 30 directed flow edges. Its executable empirical candidate is:

```text
d pi/du = pi Q
Q_ij = p_ij, i != j
Q_ii = -sum(j != i) Q_ij
logit(p_ij,e) = alpha_ij + beta_RMS (RMS_MEDIAN_e - mean(RMS_MEDIAN))
```

The eventwise leave-one-event-out result was `DELTA_LL_OOF=+111.42793938683462` over 96 events, but gains were positive in 48 and negative in 48 events. It is therefore an empirical heterogeneous-flow association, not a universal law.

## GAP-memory result

Using the frozen R40 progression coordinate `u=GLOBAL_MID_PCT/100` and frozen `GAP_MID_GLOBAL_PCT=41.8624764371929`:

```text
post-minus-pre mean memory = +0.24802386879217775
post-minus-pre median = +0.18107055419088022
positive events = 91/96
bootstrap 95% CI = [+0.21230465, +0.28602148]
```

The corrected result supports a post-GAP memory enhancement. The previously generated native-delay file is withdrawn because `U_SOURCE` is not a latent coordinate.

## Mechanism

The strongest evidence-supported mechanism is:

```text
transient activity
→ GAP-associated progression boundary
→ enhanced post-GAP run/age memory
→ heterogeneous transition propensity
```

This does not identify the microscopic carrier. Radiation, QNM relaxation, horizon shear, and direct GR derivation remain unbound or untested at the required event-row level.

```text
STATE_EQUATION = empirical six-state generator candidate
GAP_MEMORY_ASSOCIATION = supported descriptively
MICROSCOPIC_MECHANISM = unresolved
FUNDAMENTAL_GR_LAW = not established
HOLDOUT30_ACCESSED = false
```
