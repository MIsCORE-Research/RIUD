# MIsCORE mechanism synthesis R2

## Evidence chain

Across three independent pure-GR auxiliary simulations (SXS:BBH:0319, 0323, 0320), the same AhC-relative surface behavior is observed:

1. At the AhC boundary, SpinFunction and WeylE_NN angular RMS are elevated and DimlessRicciScalar is elevated through an angular-variance contribution; WeylB_NN shows the opposite early-to-late direction.
2. The surface maxima for SpinFunction, WeylE_NN, and DimlessRicciScalar occur at `tau=0`, so this is a boundary-limited formation transient, not a resolved post-formation peak.
3. The waveform peaks occur later: h22 at 16.87–16.98M and h44 at 17.47–17.68M after AhC.
4. The waveform instantaneous frequencies approach source-native Kerr QNM real frequencies: in the fixed 10–20M window, h22 is about 0.083 below the QNM frequency and h44 about 0.286 below; in the fixed 40–80M window, the differences are approximately 0.001 or less in all three events.

## Surface-field coordination versus waveform amplitude

A prespecified AhC-relative 0–80M, 0.5M-grid correlation audit was added for the three auxiliary simulations. Surface-field co-variation is strong internally (for example, zero-lag SpinFunction–WeylE correlations are 0.886–0.906 and SpinFunction–Ricci correlations are 0.972–0.986), but zero-lag correlations between any surface field and h22 or h44 amplitude are small (absolute values at most about 0.095 across these pairs). The largest absolute correlations in the fixed ±20M descriptive lag scan occur at edge lags (typically −15 to −20M or +20M), so they are not a stable, event-independent response delay. This supports a coherent surface transient without establishing a simple waveform-amplitude coupling law.

## Mechanistic interpretation

The most coherent effective picture is:

`common-horizon formation → boundary-limited angular surface-geometry transient → waveform peak/transition → later Kerr-QNM frequency settling`

The source-native observations are compatible with a short-lived strong-field surface-geometry transient followed by ordinary remnant-mode relaxation. This is more specific than a generic “nonlinear effect” label and is compatible with pure GR in the auxiliary simulations.

## Ten-event scalar-horizon control

The preserved SXS10 `Horizons.h5` files were audited with the same fixed AhC-relative 0–5M versus 25–50M comparison for scalar horizon quantities. ArealMass, DimensionfulInertialSpinMag, and chiMagInertial all increased from the early to late window in all 10/10 events (early-minus-late negative; median differences −0.0249794, −0.0916882, and −0.0486316, respectively). Thus the three-event angular RMS early excess cannot be identified with a generic scalar horizon-size or spin-magnitude transient. The surviving candidate is narrower: an angular/Weyl surface-geometry component superposed on broader scalar remnant relaxation.

## Scalar change versus waveform peak timing

Using the preserved R8 mode time series, the scalar early-minus-late changes were compared with independently measured h22 and h44 amplitude-peak times in a fixed 0–50M AhC-relative window. Across the 10-event panel, Spearman correlations were weak (absolute value at most 0.321); the largest Pearson value was 0.410 for chiMagInertial versus h44 peak time, without a comparably strong rank relation. This does not support a scalar horizon-relaxation variable as a stand-alone determinant of waveform peak timing.

## Scalar relaxation timescale versus QNM damping

For all 10 source-native SXS events, the first crossings of 50% and 90% of the AhC-to-final scalar changes were extracted without fitting. Median crossing times were 0.972M and 4.663M for ArealMass, 0.897M and 5.833M for spin magnitude, and 0.603M and 4.178M for chi magnitude. The corresponding source-native final-spin `(2,2,0)` QNM damping-time median was 11.703M. Scalar horizon evolution therefore occurs predominantly before one QNM damping time, supporting a separation between early horizon/surface reorganization and later QNM settling.

## Source-native event ordering of horizon, waveform, and flux landmarks

The original SXS10 strain files were used to calculate source-native energy-flux and angular-momentum-flux peaks in a fixed 0–50M AhC-relative window. Scalar horizon tau50 preceded the energy-flux peak in 10/10 events and the angular-momentum-flux peak in 10/10 events. Median landmark times were approximately 7.38M for h22 amplitude, 9.49M for h44 amplitude, 11.67M for angular-momentum-flux norm, and 14.12M for energy flux. The energy-flux peak followed both mode peaks in 10/10 events; the angular-momentum-flux peak followed h22 in 10/10 and h44 in 9/10. This separates the source-native landmarks temporally and supports an ordered response sequence, but does not identify any one landmark with the observational GAP, MT, or R40 hazard.

A direct horizon-derivative audit is boundary-limited: the ArealMass derivative maximum is at the AhC boundary in 10/10 events, and the spin-related derivative maxima are at that boundary in 7/10. Thus the apparent derivative-before-flux ordering is not independent causal evidence; it reflects the fact that the horizon series begins at AhC. No absorbed-flux identity is claimed.

As a separate time-series control, native horizon derivatives and radiative fluxes were interpolated onto a fixed 0.1M grid. After excluding the first 5M, zero-lag correlations were moderate to strong (median r about 0.38–0.49 for energy flux and 0.52–0.62 for angular-momentum-flux norm, depending on the horizon scalar). However, the largest absolute correlations commonly occurred at the +20M edge of the prespecified lag scan, indicating broad co-trending rather than a resolved short-lag coupling. This is consistent with a shared later remnant evolution and does not establish an absorbed-flux identity or causal direction.

## Distribution of radiative history

Direct integration of the source-native SXS10 fluxes over 0–50M shows that radiation is distributed mainly after the mode peaks. Median cumulative fractions reached by the h22 peak were 18.2% for energy and 24.0% for J-flux norm; by the h44 peak they were 30.6% and 37.7%. The largest fixed interval share occurred in 10–20M (median 41.9% of energy and 39.9% of J-flux norm), while the 0–5M share was smaller (12.3% and 16.8%). This separates the early surface transient from the later distributed radiative-history layer; it does not establish cumulative radiation as the microscopic origin of RIUD memory.

The same QNM consistency check was extended to the original SXS10 `Strain_N2.h5` files. Median frequency minus the source-native Kerr QNM frequency changed from −0.1055 to −0.00090 M⁻¹ for h22 across the fixed 10–20M to 40–80M windows, and from −0.3027 to +0.00267 M⁻¹ for h44. All 10 events were scorable in each window. This supports a reproducible late-time QNM-frequency settling pattern, while leaving the early surface transient and the RIUD memory mechanism distinct.

## What remains open

The auxiliary surface fields do not provide the missing event-level mapping to the frozen observational GAP/MT/S coordinates, and the R8 source-state additions did not close the RIUD memory likelihood or derive the frozen `S` law. Therefore this synthesis does not establish the microscopic origin of `S`, the R40 hazard, or the observational GAP.

`MECHANISM_STATUS=DESCRIPTIVE_SOURCE_NATIVE_CANDIDATE`

`PURE_GR_COMPATIBILITY=SUPPORTED_DESCRIPTIVELY`

`RIUD_S_MICROSCOPIC_ORIGIN=NOT_ESTABLISHED`

`DIRECT_EINSTEIN_DERIVATION=NOT_ESTABLISHED`

`NEW_PHYSICS=NOT_CLAIMED`
