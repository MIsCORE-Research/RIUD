# R13 design lock

Use the existing SXS-native extended R6 history as the sole state-map input.
Derive state-change timestamps from adjacent native history rows. Bind only
when the timestamp lies inside the existing source-native waveform and AhC
support. No endpoint clamp, map refit, new threshold, or DEV transition-time
projection is allowed. R8/R10/R11 remain read-only. Holdout30 is untouched.
