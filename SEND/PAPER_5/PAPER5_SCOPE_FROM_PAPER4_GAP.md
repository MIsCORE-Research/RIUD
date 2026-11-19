# RIUD Paper V scope extracted from the Paper IV boundary

## Purpose

This document defines what Paper V can add beyond Paper IV using the already
frozen RIUD outputs. It is a scope and manuscript-planning document; it does
not introduce a new score, fit, threshold, null, map, state rule, or physical
law.

## Paper IV already established

Paper IV established the DEV99/PATH99 population, the endogenous state/history
lineage, the autonomous transition structure, the physical coordinate, the
frozen physical score and the R39/R40 clock law. The frozen main-domain law is:

```text
S = 0.22030031492055946*z(R)
  + 0.3457660274266933*z(CHI_A_NORMALIZED)
gamma = 0.3162354634393393
```

Paper IV also contains the four-map replay, W4 power audit, gap-strength and
gap-location analyses, and the Combined101 characterization. Paper V must not
present any of these as newly discovered or refitted.

## The Paper V question

Paper V should ask whether the frozen RIUD structural object survives a change
of representation and what its physical interpretation can, and cannot, be.
The central object is therefore:

```text
frozen node/path structure
    -> intrinsic progression/topology
    -> cross-representation audit
    -> explicit physical claim boundary
```

This is a cross-representation and scope paper, not a new-law paper.

## Paper V contributions beyond Paper IV

### 1. Source-native pure-GR cross-representation replay

The SXS branch applies the frozen structural detector to a deterministic
source-native representation because SXS has no LIGO detector-residual
frontend. The adapter uses the SXS native quadrature representation specified
in the frozen SXS contract; it does not claim exact LIGO residual replay.

Frozen results:

```text
PATH_FOUND                         10/10
N0->A1->G                          10/10
G->AR                              6/6 AR-scorable
TRUE_TOPOLOGY_NONREPRODUCTION     0
AR-not-scorable events             4
finite-support behavior            supported in the audited window
```

The correct claim is partial source-native structural correspondence. The
four non-scorable events remain in the denominator and are not converted into
topology successes.

### 2. Availability-defined raw support audit

Paper V adds an explicit raw-input availability and denominator audit. Among
the 98 DEV99 events with a frozen path, 17 had existing original H1/L1 raw
pairs in the searched local stores. All 17 were audited under one frozen
ONPATH/OFFPATH support criterion with fixed NULL200 controls:

```text
ONPATH > OFFPATH                  15/17
NULL200 fixed-corridor rare       16/17
both criteria                     15/17
```

The one DEV99 NO_PATH event, `GW241230_233618`, is kept separate. The remaining
81 PATH_FOUND events are unavailable-input cases, not negative raw-support
results. The raw17 result is therefore an availability-defined diagnostic
subset and must not be expanded to a 98-event population claim.

### 3. Representation and causality boundary

Paper V makes explicit what the SXS result does and does not resolve:

```text
LIGO residual structure                  supported in the DEV lineage
source-native pure-GR structural replay  supported as partial correspondence
exact detector/noise attribution          unresolved
exact residual-to-source identity         unresolved
exact M-Time = physical merger time      unresolved
GR falsification                         not claimed
new physics                              not established
```

This distinction is a contribution because it prevents a source-native replay
from being misreported as an exact detector-residual reproduction.

### 4. Frozen negative-result and scorability accounting

The paper must preserve the two raw17 exceptions, the 81 unavailable raw
inputs, the one DEV99 NO_PATH event, and the four SXS AR-not-scorable events.
These are part of the evidence, not cleanup exclusions. This accounting is
the defensible answer to the reviewer question “what did not reproduce, and
could it actually be tested?”

## Proposed Paper V title

**Cross-representation validation and physical scope of a frozen transition
structure in binary-black-hole merger data**

Alternative short title: **The physical scope of a frozen RIUD transition
structure**.

## Recommended manuscript structure

1. **Introduction** — Paper IV froze the transition object; Paper V tests
   representation portability and claim limits.
2. **Frozen RIUD object** — reproduce the Paper IV contract without refitting
   `S`, `gamma`, map, topology, or thresholds.
3. **Cross-representation protocol** — LIGO residual lineage versus the
   source-native SXS adapter; define exact-replay and native-replay boundaries.
4. **SXS source-native results** — path existence, early topology, AR
   scorability, reentry, and finite support.
5. **DEV raw-support diagnostic** — availability-defined raw17 accounting,
   fixed criterion, NULL200 reference, and exceptions.
6. **Physical interpretation** — detector artifact, pure-GR absence,
   waveform-model incompleteness, and analysis/representation incompleteness.
7. **Limitations and claim matrix** — unresolved exact frontend, M-Time
   identity, and population coverage.
8. **Conclusion** — the structural object transfers partially across
   representations; the stronger causal and exact-time claims remain open.

## Paper V claim boundary

### Supported

- A frozen RIUD path object is present in all 10 audited source-native SXS
  cases.
- The early `N0->A1->G` progression is present in all 10.
- `G->AR` is reproduced in all 6 cases with an actual AR opportunity.
- The audited SXS paths terminate before the extended right search boundary,
  supporting finite support for this panel and window.
- Frozen raw support is positive in the availability-defined 17-event audit
  under the stated criterion, with exceptions preserved.

### Partial or unresolved

- Full `N0->A1->G<->AR` topology is only partially observable in SXS because
  four events do not reach the AR-eligible region.
- Exact equivalence between LIGO residual and SXS source-native frontend is
  not established.
- Detector noise/response cannot be separated from representation effects by
  the source-native SXS replay alone.
- M-Time is a reproducible waveform-native landmark/candidate, not a proven
  physical merger-time identity.

### Not claimed

- No exact LIGO-residual replay in SXS.
- No GR falsification.
- No confirmed new physics.
- No 98-event or 97-event raw-support population result from the 17 available
  raw pairs.
- No new physical law beyond the frozen Paper IV `S` and `gamma` law.

## Evidence anchors

The source of truth is the authoritative Paper V freeze directory and its
included lineage, raw17, SXS, R40, claim-matrix, reviewer-defense, and
verification files. The relevant frozen outputs are not modified by this
document.

```text
PAPER5_FINAL_REPORT.md
LINEAGE/PAPER5_FINAL_LINEAGE_FREEZE.md
LINEAGE/PAPER5_COMPLETE_LINEAGE.md
RAW17/RIUD_RAW_FROZEN_PATH_SUPPORT_AUDIT_R0_20260823_EXISTING17_SUMMARY.csv
SXS/SXS_NATIVE_REPLAY_SUMMARY.json
SXS/SXS_EXTENDED_PATH_ONLY_TOPOLOGY_AUDIT.json
SXS/SXS_EXTENDED_SEARCH_SUPPORT_AUDIT_SUMMARY.json
SXS/SXS_NATIVE_REPLAY_CONTRACT.txt
CLAIM_EVIDENCE_MATRIX_UPDATED.csv
REVIEWER_DEFENSE/REVIEWER_ATTACK_DEFENSE_MATRIX.md
```

`HOLDOUT30_ACCESSED=FALSE` remains a release invariant.
