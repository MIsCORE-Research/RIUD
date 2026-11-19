# MIsCORE mechanism campaign — consolidated evidence matrix

This document consolidates the frozen upstream R8/R11/R40 evidence and the deterministic source-native audits in this branch. It is an evidence ledger, not a new fitted model.

## Candidate-mechanism status

| Candidate / layer | Evidence | Status | Boundary |
|---|---|---|---|
| Pure-GR internal source structure (R8 frozen path/topology replay) | Prior frozen R8 path/topology result: PATH_FOUND=10/10; N0→A1→G=10/10; G↔AR=6/6 AR-scorable; true failure=0 | SUPPORTED_SOURCE_NATIVELY_WITH_SCOPE | This is the R8 frozen path/topology scope, not the later strict R13 native-map support audit |
| Strict SXS native-map transition support (R13) | N0→A1=0/10 in physical support; A1→G=8/10; G→AR=6/6; AR→G=0/6; AR source support missing=6 | TECHNICAL_HOLD_NATIVE_POST_REENTRY_SUPPORT_MISSING | Do not promote R8 topology counts to an R13 full native-map result |
| S_A as a direct merger timestamp | In the frozen A-only physical cohort (N=73), Spearman(S_A, GAP)=0.106, MT=0.109, MAX_FLOW=0.029; the largest landmark association is with PEAK, 0.372 | NOT_SUPPORTED_AS_TIMESTAMP | S_A is a rate/state coordinate; this audit does not define a time conversion or establish causality |
| Frozen S term inside the R40 hazard | Across 2,976 frozen rows, removing/restoring S algebraically changes cumulative row log-probability by +5.693923102455701; median γS=-0.00412, IQR=-0.07087 to +0.07983 | SUPPORTED_AS_RATE_MODULATOR | This isolates the role of S within R40 and is not a microscopic-origin test or timestamp identity |
| Where the frozen S contribution acts | S-only ΔLL by source state: N0=-1.4128, A1=+3.1858, G=+1.1487, AR=+2.7722; observed-transition rows +12.0858 versus no-transition rows -6.3918 | ACTIVE-TRANSITION-ENRICHED_RATE_EFFECT | This is an algebraic decomposition of the frozen operator, not a source-level causal attribution; signed contributions are not disjoint evidence fractions |
| Event-level heterogeneity of S contribution | ABC=A: +6.09276 over 73 S-available events; B: +0.20030 over 5; C: -0.46231 over 10; MAX_FLOW<t0: -0.40762 over 16 versus +5.89726 over the other 79 | DESCRIPTIVE_REGIME_HETEROGENEITY | Existing labels were joined after the frozen decomposition; no regime-specific refit or causal claim |
| Binwise distribution of S contribution | Across the 31 frozen bins, S-only ΔLL changes sign across bins; cumulative contribution dips early and recovers to +5.693923102455685 at the final bin | DISTRIBUTED_MEMORY_RATE_MODULATION | No single timestamp or impulse localization is established; bin profile is an algebraic frozen-operator diagnostic |
| Source-history discriminator (completed R0 LOSO) | Ten-event source-state baseline: cumulative flux increment +9.687599929348; instantaneous flux −7.399301550260; source-time −21.124032735212; reversed cumulative-flux control +6.006398176390 | CUMULATIVE_RADIATIVE_HISTORY_INFORMATION_SUPPORTED | The reverse-time control prevents a causal direction claim; this does not close the RIUD memory mechanism |
| Forward versus reversed cumulative-flux ordering | Forward cumulative flux beats reversed cumulative flux in 8/10 events; median paired ΔLL=+1.16001; exact sign p=0.05469; Wilcoxon one-sided p=0.06543; whole-model increment difference=+3.68120 | WEAK_DIRECTIONAL_CANDIDATE | Direction is suggestive but not conventionally decisive at this small N; no causal claim |
| Direct GR versus RIUD memory (R6P9/R7F2) | Direct instantaneous GR ΔLL vs P0=+0.22433543998687; frozen RIUD ΔLL=+5.3369505049687; recovered GR-history ΔLL=-2.58632683864383; GR-memory-kernel ΔLL=-4.25942481822468 | RIUD_MEMORY_NOT_EXPLAINED_BY_TESTED_GR_HISTORY | R7F2 is the valid contract-recovered branch; the earlier contract-mismatched R7 output is not used |
| Common-horizon angular/Weyl transient | 0319/0323/0320: 4/4 fields repeat the same early-to-late directional change | PARTIAL_SOURCE_NATIVE | Surface maxima are AhC-boundary limited; only three events have these angular fields |
| Generic scalar horizon-size/spin relaxation as the trigger | SXS10 ArealMass, spin magnitude, and chi magnitude all have early−late<0 in 10/10 | NOT_SUPPORTED_AS_STANDALONE_TRIGGER | Scalar evolution is broader than the angular transient |
| Scalar horizon change as waveform-peak clock | Maximum event-level Spearman absolute correlation 0.321; maximum Pearson 0.410 | NOT_SUPPORTED_AS_STANDALONE_CLOCK | Descriptive N=10 association only |
| Source-native radiative ordering | Median h22≈7.38M, h44≈9.49M, J-flux≈11.67M, E-flux≈14.12M after AhC | SUPPORTED_ORDERING | Does not identify an observational GAP/MT |
| Direct horizon derivative→flux causation | Derivative maxima commonly at AhC boundary; later derivative/flux co-trend peaks at lag-scan edge | NOT_ESTABLISHED | No exact absorbed-flux balance binding |
| Distributed radiative history | Largest fixed 0–50M share occurs at 10–20M: E≈41.9%, J-norm≈39.9% | DESCRIPTIVE_SUPPORT | Not proof of RIUD memory origin |
| Horizon–flux time-series co-trend | In the 5–50M control, zero-lag median r≈0.38–0.49 for energy and 0.52–0.62 for J-flux norm | DESCRIPTIVE_SUPPORT | Maxima often at +20M lag boundary; no short-lag causal identity |
| Kerr QNM late settling | SXS10 h22 Δf(QNM): −0.1055→−0.00090 M⁻¹; h44: −0.3027→+0.00267 M⁻¹ | SUPPORTED_LATE_SETTLING | Does not identify early transient as QNM excitation |
| Fixed quadratic QNM mode coupling | Frozen R8 diagnostic not stable cohort-wide | NOT_SUPPORTED_UNDER_FIXED_DIAGNOSTIC | No coefficient fitted |
| Non-normal/transient-amplification operator | Required source-native operator/pseudospectrum absent | NOT_TESTABLE_WITH_ACQUIRED_DATA | No surrogate substituted |
| Frozen R40 memory/S microscopic origin | R8 richer source-state additions and R11 horizon-relaxation branch did not close it | NOT_ESTABLISHED | R40 remains valid within its frozen observational domain |
| Orbital/separation/component-spin mechanism (R10) | 32 transition rows; separation available 10/32, component-spin orientation 10/32, h22 orbital frequency 24/32, remnant orientation 18/32; complete mechanism test not established | NOT_ESTABLISHED | Source support is incomplete across the topology; no uniform orbital direction |
| G↔AR phase/hazard relation (R12) | 10 source-supported G/AR rows; four events with both directions; median paired phase separation 2.1216436214719776; derivative opposition 2/4 | CORRELATE_ONLY | Neither relaxation phase nor RIUD memory gained established incremental closure |
| Strict native-map support (R13) | N0→A1=0/10 in physical support; A1→G=8/10; G→AR=6/6; AR→G=0/6; six AR→G rows lacked post-reentry source support | TECHNICAL_HOLD | Does not invalidate the separate R8 fixed-grid replay; full native-map topology is not established |

## Frozen R8 source-state likelihood boundary

The existing R8 source-state comparison must be kept separate from the new source-native timing audits. Relative to the memory-only source-state baseline, a flux-only extension improved the held-out likelihood by `+9.377255076976752`, whereas a horizon-plus-flux extension changed it by `−42.963721545587646` and the full source-state extension by `−38.66994508480133`. Thus radiative variables contain some incremental information in that frozen comparison, but adding all available source observables does not reproduce the R40 memory law. These values were read from the authoritative R8 summary; no refit was run here.

## Surviving source-native sequence

```text
common-horizon formation
→ early angular/Weyl surface-geometry transient
→ scalar horizon reorganization
→ h22/h44 mode response
→ distributed 10–20M radiative history
→ energy/J-flux maxima
→ late Kerr-QNM frequency settling
```

The sequence is compatible with pure GR in the acquired source-native simulations. It is not an equation-level derivation of the frozen RIUD hazard, S, GAP, or MT.

## Strongest current interpretation

The data favor a layered source-native response rather than one universal instantaneous merger clock. The early component is angular/Weyl and boundary-localized; scalar horizon variables evolve on a somewhat broader early-to-late relaxation; radiation is distributed later; and the remnant frequency approaches Kerr QNM values at late times. The angular component is therefore the most specific surviving mechanism candidate, while the physical origin of the observational semi-Markov memory remains unresolved.

## Explicit non-claims

`DIRECT_EINSTEIN_DERIVATION=NOT_ESTABLISHED`

`RIUD_S_MICROSCOPIC_ORIGIN=NOT_ESTABLISHED`

`HORIZON_ABSORBED_FLUX_IDENTITY=NOT_ESTABLISHED`

`OBSERVATIONAL_GAP_NATIVE_SXS_IDENTITY=NOT_ESTABLISHED`

`NEW_PHYSICS=NOT_CLAIMED`

## Remaining decisive evidence gaps

1. A source-native event-level registration between the observational GAP/MT/S coordinates and the SXS horizon/radiative variables.
2. Full horizon absorption and infinity-flux balance data on a common coordinate and normalization.
3. Angular/Weyl surface observables for a larger SXS cohort under the same fixed extraction contract.
4. A predeclared, independent test linking the layered source-native sequence to the frozen R40 age/memory operator without refitting R40.

No one of these gaps is silently replaced by a surrogate in this campaign.

`CAMPAIGN_STATUS=SOURCE_NATIVE_DESCRIPTIVE_MECHANISM_CANDIDATE`
`PURE_GR_COMPATIBILITY=SUPPORTED_DESCRIPTIVELY`
`MICROSCOPIC_CLOSURE=NOT_ESTABLISHED`
