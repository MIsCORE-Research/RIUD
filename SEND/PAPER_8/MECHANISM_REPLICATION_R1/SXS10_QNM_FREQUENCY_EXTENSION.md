# SXS10 source-native QNM frequency extension

Corrected audit: reads original `Strain_N2.h5` directly, not downsampled summary history. Fixed AhC-relative windows 10–20M, 20–40M, and 40–80M. Frequency is from unwrapped native phase; QNM frequency uses qnm 0.4.4 with preserved final spin and mass ratio. No fit or timing adjustment.
- (2,2,0) AHC_10_20M: 10/10 scorable; median frequency-minus-QNM=-0.10546102 M^-1
- (2,2,0) AHC_20_40M: 10/10 scorable; median frequency-minus-QNM=-0.013002834 M^-1
- (2,2,0) AHC_40_80M: 10/10 scorable; median frequency-minus-QNM=-0.00089984213 M^-1
- (4,4,0) AHC_10_20M: 10/10 scorable; median frequency-minus-QNM=-0.30265852 M^-1
- (4,4,0) AHC_20_40M: 10/10 scorable; median frequency-minus-QNM=-0.059007833 M^-1
- (4,4,0) AHC_40_80M: 10/10 scorable; median frequency-minus-QNM=0.0026735569 M^-1

Ringdown consistency only; not a microscopic RIUD mechanism identification.
