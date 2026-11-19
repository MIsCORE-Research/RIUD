# R8 secondary cohort interim mechanism audit

This is an interim, separate audit. It does not modify the frozen SXS10 branch,
R0/R1/R2/R3/R40, or Holdout30. The 16-event panel was selected from metadata
and source availability before replay, using one lexicographically first event
per occupied mass-ratio/final-spin coverage cell; outcomes were not used.

## Coverage

- Events: 16
- Source files: 80/80, SHA pass 80/80
- PATH_FOUND: 15/16
- NO_PATH: 1/16 (`0054`)
- Mechanism row master: 960 rows
- Transition audit: 30 rows
- Source-native physical summary: 16/16 events
- Frozen path-only topology: `N0->A1=16/16`, `A1->G=16/16`, `G->AR=0/16`, `AR->G=0/16`, illegal transitions 0

The absence of `G->AR` in this secondary panel is retained as an observed
negative result; it is not converted into a scorable reentry claim.

## Mechanism model summary

The same LOSO mechanism blocks were applied. The baseline is `BM`.

| model | total log-likelihood | delta vs BM |
|---|---:|---:|
| B0 | -112.648091293362 | +19.568598896609 |
| BM | -132.216690189971 | 0 |
| BH | -132.073755391423 | +0.142934798548 |
| BR | -125.004121354533 | +7.212568835438 |
| BF | -106.993038699595 | +25.223651490377 |
| BHF | -203.987139779971 | -71.7704495899997 |
| BFS | -294.046776690203 | -161.830086500231 |
| BMODE | -97.582045388734 | +34.634644801238 |
| BM+H | -384.840796045816 | -252.624105855844 |
| BM+R | -149.276756856485 | -17.060066666514 |
| BM+F | -181.397016396650 | -49.180326206679 |
| BM+HF | -911.201582293368 | -778.984892103396 |
| BM+FS | -992.695816906996 | -860.479126717025 |

Sequential memory increments relative to the corresponding non-memory block:

- after horizon: `BM+H - BH = -252.767040654392`
- after remnant: `BM+R - BR = -24.2726355019521`
- after flux: `BM+F - BF = -74.4039776970550`
- after horizon+flux: `BM+HF - BHF = -707.214442513396`
- after full source: `BM+FS - BFS = -698.649040216793`

These are not evidence that the source variables are absent; they show that
the tested combined mechanism blocks do not improve this secondary cohort
under the current LOSO surrogate contract. No coefficient or rule refit was
performed for this audit.

## Temporal and S diagnostics

Across the 30 audited transition-variable pairs, the fraction whose variable
change preceded the transition was:

- area, mass, chi, angular momentum and most distance/rate variables: 12/30
- cumulative-energy / cumulative-Jz / flux and derivative variants: 13--14/30
- relaxation-rate area: 11/30

The common deterministic changepoint audit produced 320 event-variable rows;
median distance to the nearest observed transition was `50.75636165771455 M`.
No sharp, reproducible pre-transition alignment was established.

Using frozen `S_FROZEN` and the same event-level source summary contract, the
secondary diagnostic correlations were: areal-mass delta Pearson `+0.4483`
(Spearman `+0.5000`), Christodoulou-mass delta `+0.2692` (`+0.1941`), chi
delta `+0.3026` (`+0.4324`), J-magnitude delta `-0.6205` (`-0.5647`),
energy flux `-0.5645` (`-0.7059`), Jz flux `-0.6139` (`-0.7088`), and local
relaxation proxy `-0.0641` (`-0.6382`). All used N=16. These mixed signs do
not constitute stable gamma-positive mechanism support; they are secondary
diagnostics only.

## Interim boundary

`SECONDARY_MECHANISM_TEST_STATUS=COMPLETED_NO_CLOSURE`

The secondary panel does not close a single physical mechanism for the
memory-bearing transition-time behavior. It also does not justify pooling its
different topology/support behavior with the frozen SXS10 result. A final R8
freeze/report remains pending until the requested cross-cohort synthesis is
explicitly completed.
