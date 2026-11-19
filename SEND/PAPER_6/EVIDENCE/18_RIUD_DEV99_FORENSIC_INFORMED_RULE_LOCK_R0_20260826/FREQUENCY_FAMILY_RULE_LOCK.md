# Frequency family rule lock

The frozen DEV99 frequency family definitions are retained exactly as
provided by the source freeze:

* FREQ_MAG: K=2, using only the four frozen frequency-variation fields
  `frequency_span_hz`, `frequency_total_variation_hz`, `abs_net_change_hz`,
  and `rate_mad_hz_per_s`.
* FREQ_SHAPE: K=2, using only the within-event normalized profile fields
  `f_shape_00` through `f_shape_31`.

Node count, width, transition fingerprint, ABC, A2, S, and legacy H labels
were not used to define these frozen frequency-only families. The original
assignment table and inputs are copied beside this lock. No K selection,
family refit, or Holdout5 fitting is performed here.
