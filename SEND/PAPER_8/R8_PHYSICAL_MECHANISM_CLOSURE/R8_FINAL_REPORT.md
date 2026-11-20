# MIsCORE R8 Physical Mechanism Closure

R8 used active public-source acquisition for the prespecified SXS10 cohort. Fifty source files (metadata, Horizons, ExtraWaveforms, Strain_N2, and sidecar JSON at each simulation resolution) were acquired and MD5/SHA256 verified.

## Scope

The observational RIUD law, R40 coefficients, state definitions, and prior branches were not modified. SXS data were analyzed source-natively. No Holdout30 access, refit, new threshold, or detector-residual identity claim was made.

## Numerical tests

- AhC horizon state, areal/irreducible-mass, Christodoulou-mass, spin and geometry series: 10/10.
- Horizon derivatives and J/chi derivative proxies: 10/10. They are explicitly horizon-balance proxies, not absorbed flux.
- Standard `sxs.waveforms.energy_flux` and `angular_momentum_flux` routines were applied to all 10 strain-mode files; direct stored flux was false, waveform-derived infinity flux was true.
- Remnant mass/spin metadata and late relaxation diagnostics: 10/10.
- h22 and h44 source-native modes: 10/10. The fixed cohort-wide 2:1 frequency-locking and phase diagnostic did not yield stable nonlinear-QNM support; no coefficient was fitted.
- Existing source-native RIUD path/topology remains the previously frozen result: PATH_FOUND=10/10, N0→A1→G=10/10, G↔AR=6/6 among AR-scorable events, true failure=0. It is not an exact LIGO residual replay.
- Non-normality was not claimed: a source-native perturbation operator or pseudospectral object was not present, and generic transient amplification was not substituted.

## Verdict

`GR_INTERNAL_SOURCE_STATE_OBSERVED=SUPPORTED`
`HORIZON_STATE_AND_REMNANT_RELAXATION=SUPPORTED_AS_SOURCE_NATIVE_OBSERVABLES`
`HORIZON_BALANCE_PROXY=SUPPORTED_AS_DERIVED_PROXY`
`INFINITY_FLUX=SUPPORTED_AS_WAVEFORM_DERIVATION`
`NONLINEAR_MODE_COUPLING=NOT_SUPPORTED_UNDER_FIXED_DIAGNOSTIC`
`R40_MEMORY_REDUCTION_BY_SOURCE_STATE=NOT_ESTABLISHED`
`NONNORMAL_OPERATOR=NOT_TESTABLE_WITH_ACQUIRED_DATA`
`MICROSCOPIC_ORIGIN=UNRESOLVED`
`DIRECT_GR_DERIVATION=NOT_ESTABLISHED`
`NEW_PHYSICS=NOT_CLAIMED`

The active acquisition requirement and all currently testable SXS10 mechanism tests are complete. The microscopic origin of the effective semi-Markov memory is not closed by these source-native observables.

## Final status block

R8_OVERALL_STATUS=PASS_ACTIVE_MECHANISM_CAMPAIGN
TESTED_MECHANISM_COUNT=6
SUPPORTED_MECHANISM_COUNT=0
PARTIAL_MECHANISM_COUNT=6
DISFAVORED_MECHANISM_COUNT=1
RULED_OUT_MECHANISM_COUNT=0
UNTESTABLE_MECHANISM_COUNT=1
BEST_GR_INTERNAL_MECHANISM=SOURCE_NATIVE_HORIZON_STATE_AND_REMNANT_EVOLUTION
SECOND_BEST_GR_INTERNAL_MECHANISM=SOURCE_NATIVE_WAVEFORM_INFINITY_FLUX
BEST_MECHANISM_EXPLAINS_TOPOLOGY=PARTIAL_SOURCE_NATIVE
BEST_MECHANISM_EXPLAINS_MEMORY=NOT_ESTABLISHED
BEST_MECHANISM_EXPLAINS_TIME_LAW=NOT_ESTABLISHED
BEST_MECHANISM_EXPLAINS_S=NOT_ESTABLISHED
BEST_MECHANISM_EXPLAINS_GAP=NOT_ESTABLISHED
BEST_MECHANISM_EXPLAINS_MT=NOT_ESTABLISHED
BEST_MECHANISM_EXPLAINS_EVENT_VARIATION=PARTIAL_SOURCE_NATIVE
RIUD_MEMORY_CLOSED_BY_RICHER_GR_STATE=NOT_ESTABLISHED
MICROSCOPIC_MECHANISM_VERDICT=E_AVAILABLE_DATA_INSUFFICIENT_FOR_MICROSCOPIC_CLOSURE
FULL_EINSTEIN_EQUATION_DERIVATION=NOT_ESTABLISHED
GR_FALSIFICATION=NOT_CLAIMED
BEYOND_GR=NOT_CLAIMED
HOLDOUT30_ACCESSED=FALSE
REMAINING_UNKNOWN=Exact source-to-RIUD mechanism binding, horizon absorption, non-normal operator, and microscopic generator origin
NEXT=STOP_AND_FREEZE_RIUD_PHYSICAL_MECHANISM_CAMPAIGN
