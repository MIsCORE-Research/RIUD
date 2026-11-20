# SXS10 horizon-derivative versus flux ordering audit

Full native `Horizons.h5` scalar series and original `Strain_N2.h5` were used. Absolute first-derivative peaks and flux maxima were measured in a fixed 0–50M AhC-relative window. This is a timing-order diagnostic, not a balance-law fit.
- ArealMass derivative before ENERGY_FLUX: 10/10; boundary-peaked=10/10; median |Δtau|=14.1203M
- ArealMass derivative before J_FLUX_NORM: 10/10; boundary-peaked=10/10; median |Δtau|=11.6707M
- chiMagInertial derivative before ENERGY_FLUX: 10/10; boundary-peaked=7/10; median |Δtau|=13.9553M
- chiMagInertial derivative before J_FLUX_NORM: 10/10; boundary-peaked=7/10; median |Δtau|=11.5487M
- DimensionfulInertialSpinMag derivative before ENERGY_FLUX: 10/10; boundary-peaked=7/10; median |Δtau|=13.9553M
- DimensionfulInertialSpinMag derivative before J_FLUX_NORM: 10/10; boundary-peaked=7/10; median |Δtau|=11.5487M

The derivative peak is not interpreted as absorbed flux because the source-native files do not provide an exact horizon-to-infinity balance binding for this audit.
