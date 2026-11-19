RIUD_R26C42G_EXACT_SELECTOR_AWARE_COMPLEX_PHASE_NULL_R8_EVENTWISE_TAU_FRAME_EQUIVALENCE_20260801

R8 eventwise tau-frame equivalence
----------------------------------
Observed failures in R6 were not morphology changes:

GW240919: selected tau = frozen tau +0.008 s
GW200224: selected tau = frozen tau -0.002 s
GW200129: selected tau = frozen tau -0.024 s

For each, frequency, width, node count, node ordering, and node-to-node spacing
were identical. This demonstrates event-specific coordinate-origin differences
between frozen path tables and the canonical engine axes.

R8 accepts an observed replay only when:
- node count is identical;
- every frequency is identical;
- every width is identical;
- order is identical;
- inter-node tau spacing is identical;
- all tau differences equal one event-level constant to 5e-10 s.

Any morphology change or nonconstant timing deformation remains a hard failure.
Every event's shift and maximum residual from a constant shift are recorded.

Visible 1/200 through 200/200 progress, ten-control checkpoints, all-event
preflight, null definitions, 100,000 draws, and scientific verdict thresholds
remain unchanged.
