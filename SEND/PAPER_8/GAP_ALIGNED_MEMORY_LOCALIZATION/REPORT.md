# GAP-aligned memory localization

Descriptive join of frozen R40 rows to frozen GAP table; no refit or redefinition.

Correction: `U_SOURCE` is the frozen global progression fraction, so the valid GAP-relative coordinate is `100*U_SOURCE - GAP_MID_GLOBAL_PCT`, with `GAP_MID_GLOBAL_PCT=41.8624764371929`; the earlier native-delay conversion is invalid and must not be used. In this correct coordinate, memory begins rising before/around the GAP boundary (bin 13: +0.325 percentage points), reaches its highest mean at bin 19 (+19.075 points; mean 0.808872), and remains elevated through bin 20 (+22.200 points; mean 0.731685). This is a progression-localization result, not a causal microscopic proof.

Eventwise pre/post audit: 96 events, 91 with positive post-minus-pre memory difference and 5 negative. Mean difference = 0.24802386879217775, median = 0.18107055419088022, 9999-event bootstrap 95% CI = [0.21230465, 0.28602148], bootstrap probability of a non-positive mean = 0.0001. This supports a robust descriptive post-GAP memory contrast, but does not identify a microscopic cause.

{
  "R40_ROWS": 2976,
  "GAP_ROWS": 97,
  "COMMON_EVENTS": 96,
  "UNBOUND_EVENTS": [],
  "MAPPING_STATUS_COUNTS": {
    "LOSSLESS_AFFINE_INVERSE": 97
  },
  "GAP_ALIGNED_COORDINATE": "U_SOURCE - GAP_CENTER_LATENT",
  "STATUS": "DESCRIPTIVE_GAP_MEMORY_LOCALIZATION",
  "HOLDOUT30_ACCESSED": false,
  "REFIT": false
}
