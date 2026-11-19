# Integrated mismatch forensic audit R3

Purpose: reverse-trace only the events where the fixed, leave-one-event-out descriptive branch prediction disagreed with the existing observation.
No new map, path, threshold, fit, imputation, or causal claim was introduced.

## Scope and definitions
- MAG = S rank-bin + frequency-span rank-bin + total-frequency-variation rank-bin; fixed leave-one-out branch prediction.
- SHAPE = f_turns rank-bin + transition-entropy rank-bin + network-z-median rank-bin; fixed leave-one-out branch prediction.
- GAP side/order = existing family branch with ABC where available, with the predeclared family-only fallback where ABC is unavailable.
- `FULL_INPUT_MISMATCH` is the mismatch class. Fallback, missing observation, and unavailable LOO cells are not counted as scientific mismatches.

## Mismatch counts
- MAG: 6 full-input mismatches.
- SHAPE: 30 full-input mismatches.
- GAP_ORDER_MAXFLOW: 3 full-input mismatches.
- GAP_SIDE_T0: 1 full-input mismatch.

## What the reverse trace shows
### Missing variables / axis contrasts
For MAG mismatches, the largest descriptive contrasts are higher f_turns (median 3 versus 1), longer path/transition support (median path_nodes 15.5 versus 10.5), longer time span (0.15 versus 0.10 s), and lower f_directness. These variables were not added to the fixed MAG rule; they are candidates for a missing conditional interaction only.
For SHAPE mismatches, the largest single contrast is weak: f_directness is lower in mismatches (median 0.5357 versus 0.8091), while MAX_FLOW is earlier (0.010 versus 0.020 s) and total variation is somewhat higher (90 versus 70 Hz). The 30 mismatches are not separated by one clean scalar boundary.
For GAP-order mismatches, mismatches have shorter support (median 5 path nodes, 4 transitions, 0.04 s) and later GAP relative to the existing ordering. This is compatible with a short-track/applicability branch, but is not proof of a cause.

### Variable interactions / hidden branches
- SHAPE mismatch rate is elevated in FREQ_MAG_1 (14/33 in the retained interaction cells) and in FREQ_MAG_1 × ABC=A (9/26), but mismatches also occur in FREQ_MAG_2 and across ABC=A/B/C/OTHER. This is a possible interaction pattern, not a stable hidden branch.
- MAG mismatch counts are small and distributed: the largest retained cells are FREQ_SHAPE_2 (3/35) and FREQ_SHAPE_2 × ABC=A (2/27). No single interaction isolates all six MAG mismatches.
- GAP-order mismatches are concentrated in ABC=OTHER (2/7) and ABC=C (1/6), with all three in FREQ_MAG_2. Their support is short, so the result is better treated as a branch/applicability signal than as a new law.
- GAP-side has one full mismatch, in ABC=OTHER and FREQ_MAG_2 (1/7 in that retained cell).

### Out-of-scope / not scorable events
- NO_PATH: GW241230_233618; excluded from path-based scoring.
- S missing: GW150914_095045 and GW231008_142521; MAG uses the predeclared fallback only, not an imputed S.
- GAP/ABC observations missing: GW231008_142521 and GW231206_233901; GAP-side/order cannot be scored as observed classifications.
- SHAPE LOO cell unavailable: GW190728_064510 and GW250118_023225; not counted as failures.
- K1/K2 are absent for most of the 98 path rows (82 each), so they remain an exploratory availability-limited axis and were not treated as complete predictors of the mismatch.

## Interpretation
The main unresolved signal is SHAPE: its fixed two-axis rule does not generalize uniformly, and the mismatch is broad rather than a single obvious missing scalar. MAG has fewer mismatches and shows a descriptive association with richer/longer trajectories, suggesting that support complexity or an interaction with shape may matter. GAP exceptions are few and concentrated in short-track/OTHER-C branches, with two additional cases unscorable because the observed GAP/ABC fields are missing.
These are forensic diagnostics of a fixed exploratory predictor. They do not establish causation, do not select a revised law, and do not change the frozen RIUD map/path or scientific claims.

## Status
- PATH_FOUND=98; NO_PATH=1.
- NEW_MAP=FALSE; NEW_PATH=FALSE; IMPUTATION=FALSE; CAUSAL_CLAIM=FALSE.
- HOLDOUT30_ACCESSED=FALSE.
