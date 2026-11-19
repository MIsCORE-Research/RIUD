# RIUD Paper V full experiment audit

## Audit status

This is a read-only synthesis of the frozen Paper V lineage. It does not rerun
science, change a result, refit `S`, refit `gamma`, rebuild a map, create a
threshold, or open Holdout30.

Primary source of truth:

```text
LINEAGE/PAPER5_STAGE_CATALOG.tsv
LINEAGE/PAPER5_AUTHORITY_FILE_INDEX.tsv
PAPER5_FINAL_REPORT.md
CLAIM_EVIDENCE_MATRIX_UPDATED.csv
```

The stage catalog contains 62 recorded Paper V follow-up stages. The exact
stage folder, class, status, verdict, next action, selected authority count,
and absolute path remain in the TSV; this document groups those records for
human reporting.

## Executive result

Paper V is not one new experiment. It is a chain with four layers:

1. **Map-extension layer** — two-anchor support extension and gap survival.
2. **Frozen-law scope layer** — W0/W5 readout, W1-0 correction, W1-W4 global
   projection, and gap/M-Time terminology boundary.
3. **Physical/representation diagnostic layer** — raw trigger and known-
   physics audits, raw17 support, and source-native SXS replay.
4. **Claim-closure layer** — exact replay limits, model-comparison limits,
   exception accounting, and reviewer defense.

The Paper V main claim is therefore:

> A frozen RIUD structural transition object persists under the two-anchor
> extension and shows partial source-native correspondence in pure-GR SXS;
> its exact detector/source identity, physical merger-time identity, and causal
> interpretation remain unresolved.

## A. Canonical MAIN lineage

### A1. Two-anchor extension and gap

| Order | Stage | Frozen result | Paper V role |
|---:|---|---|---|
| 6 | `RIUD_PAPER5_MAP_ANCHOR_EXTENSION_PM1S_R5_SCORE_CHECKPOINT_WORKERS22_20260820` | PASS | Canonical expanded-anchor execution source |
| 7 | `RIUD_PAPER5_FIG6_FROZEN_DEPLETION_TWO_ANCHOR_R0_20260820` | Gap survives two-anchor extension | Structural gap persistence |
| 8 | `RIUD_PAPER5_TWO_ANCHOR_BLIND_GAP_DUAL_TIME_R0_20260820` | Gap midpoint is not supported as an MT/t0 identity by this audit | Keeps gap and time-origin claims separate |
| 9 | `RIUD_PAPER5_EXTENDED_PATH_R40_FROZEN_REPLAY_R0_20260820` | Frozen R40 replay on extended support | Checks law readout beyond local window |
| 10 | `RIUD_PAPER5_TWO_ANCHOR_EXTENDED_R40_REPLAY_R0_20260820` | W0/W5 readout on two anchors | Adds sparse extension behavior |
| 11 | `RIUD_PAPER5_GW231221_W1_FRONT_BOUNDARY_SCAN_R0_20260820` | W1 extends to the audited front limit | Boundary/support audit |

Authoritative extension facts:

```text
anchors = GW240601_061200, GW231221_135041
search support = -1.00 .. +1.00 s
path ranges = -0.04 .. +0.28 s; -0.11 .. +0.20 s
minimal extended atlas = 5 events, 75 rows
canonical 97-event map modified = FALSE
```

W0/W5 are not universal new windows:

```text
GW240601: W0 transitions=0, W5 transitions=4
GW231221: W0 transitions=2, W5 transitions=0
```

Correct report: event-specific extended readout, insufficient for a separate
W0/W5 population law.

### A2. Gap, M-Time and phase scope

| Order | Stage | Frozen verdict | Paper V role |
|---:|---|---|---|
| 12 | `RIUD_PAPER5_SUPPORT_GAP_MIDPOINT_MT_R0_20260820` | Strong waveform MT candidate | Historical candidate generation |
| 13 | `RIUD_PAPER5_SUPPORT_GAP_INDEPENDENT_DERIVATION_R1_20260820` | Reproducible waveform-native candidate; physical time unconfirmed | Independent provenance |
| 14 | `RIUD_PAPER5_FINAL_TWO_ANCHOR_GAP_MT_20260820` | Gap survives; t0 localization not supported | Final gap/time boundary |
| 15 | `RIUD_PAPER5_M_TIME_FINAL_EVIDENCE_FREEZE_20260820` | Reproducible M-Time object; physical identity open | Terminology freeze |
| 16 | `RIUD_PAPER5_PHASE_TERMINOLOGY_CORRECTION_FREEZE_R1_20260820` | W3 post-gap negative contribution is local, not an MT claim | Corrected phase language |
| 18 | `RIUD_PAPER5_PHYSICAL_S_PHASE_PARTITION_AUDIT_CORRECTION_R1_20260820` | W1-0 is preparation; primary W1 starts at frozen L1 bin | Corrected law scope |

Two-anchor native candidate positions:

```text
GW240601: gap midpoint -6.910111 ms relative to t0
GW231221: gap midpoint -2.091138 ms relative to t0
```

These values do not establish `M-Time = physical merger time`.

W1 scope correction:

```text
W1-0: U_PCT < 10.9375, pre-L1 preparation
W1:   10.9375 <= U_PCT < 45.3125, L1-to-peak primary scope
```

### A3. Global law readout

| Order | Stage | Frozen verdict | Paper V role |
|---:|---|---|---|
| 19 | `RIUD_PAPER5_GLOBAL_LAW_FULL_PHASE_MONTAGE_AUDIT_R0_20260821` | W1-W4 survive with W0 sparse and W3 post-gap local mismatch | Full-map law scope |
| 20 | `RIUD_PAPER5_GLOBAL_MAP_LAW_MONTAGE_CORRECTION_R0_20260821` | One global law projected to full map and W0 extension; W0 not separate law | Prevents W0 overclaim |
| 21 | `RIUD_PAPER5_STRUCTURE_ONLY_PHYSICAL_S_LAW_AUDIT_R0_20260821` | Frozen S structurally compatible with W1-W4; W0 sparse diagnostic | Law interpretation |
| 56 | `RIUD_PAPER5_FINAL_PHYSICAL_LAW_DERIVATION_R2_20260821` | Main S domain supported; W3 post-gap local breakdown; no new physics | Internal final derivation |
| 57 | `RIUD_PAPER5_FINAL_RIUD_LAW_VS_GR_MODEL_COMPARISON_R1_20260821` | Existing physics shares inputs but not the same RIUD observable | External comparison |
| 58 | `RIUD_PAPER5_EXISTING_PHYSICS_FINAL_COMPARISON_R2_20260821` | Unexplained is not equivalent to new physics | Final claim boundary |

Frozen law:

```text
S = 0.22030031492055946*z(R)
  + 0.3457660274266933*z(CHI_A_NORMALIZED)
gamma = 0.3162354634393393
```

Paper V does not refit either quantity.

## B. Post-freeze diagnostics

These are retained as supporting/limitation evidence, not as new universal
laws.

### B1. W0/raw/known-physics diagnostics

| Stage family | What was tested | Final use |
|---|---|---|
| `W0_CAUSAL_HYPOTHESIS`, `W0_SINGLE_EVENT_TRIGGER` | Sparse/event-specific W0 activation and raw trigger candidate | Single-event candidate only; no universal trigger claim |
| `W0_T0_PROVENANCE_TRANSITION_ORDER` | Transition ordering relative to t0 provenance | Overlay only; cross-event order unresolved |
| `W0_RAW_CAUSE_*`, `W0_TRIGGER_TO_FROZEN_S` | Raw behavior before downstream progression | Descriptive; causality unresolved |
| `PRE_W0_RAW_TRIGGER_MODEL` | Candidate raw features and model-absorption question | Model absorption unresolved |
| `PRE_W0_MODEL_ABSORPTION_RESIDUAL` | Direct three-layer model/residual comparison | Technical hold; not comparable from frozen assets |
| `RAW_SUBSTRUCTURE_PHYSICAL_LAW`, `RAW_TRIGGER_LONG_DEV97` | Expanded raw sequence and possible activation candidate | Availability/cohort-limited descriptive evidence |
| `THERMODYNAMIC_RAW_ACTIVATION`, `ALL_KNOWN_PHYSICS_RAW_ACTIVATION` | Existing known-physics variable families | Diagnostic only; no unique cause established |
| `KNOWN_PHYSICS_RAW_SEQUENCE_QNM` | QNM-scale crosswalk | QNM scale insufficient; not a new-physics result |
| `NONLINEAR_MODE_COUPLING_DIRECT_TEST` | Direct mode-combination test | Technical hold; required predeclared mode asset unavailable |

### B2. Multi-physics and source interpretation

| Stage | Frozen result | Reporting role |
|---|---|---|
| `MERGER_RESIDUAL_PHYSICAL_S` | Residual-to-S source identity not established | Explicit unresolved limitation |
| `FULL_BINARY_COMPONENT_MULTI_PHYSICS` | Relational state + clock system supported | Descriptive decomposition |
| `MULTI_LAW_DECOMPOSITION` | Four-component role decomposition supported | Do not call fundamental GR law |
| `FIVE_PANEL_S_NODE_LAW` | Frozen S/node relation recovered without trigger | Supporting structural audit |
| `ALL_PHYSICS_ASSET_RECOVERY`, `EXPANDED_PHYSICS_ASSET`, `SELECTED_PE_SCHEMA`, `EXTENDED_SELECTED_PHYSICS` | Existing physical metadata inventory | Provenance and limitation support |

## C. Cross-domain results added to the final freeze

### C1. SXS source-native replay

```text
PATH_FOUND = 10/10
N0->A1->G = 10/10
G->AR = 6/6 AR-scorable
TRUE_TOPOLOGY_NONREPRODUCTION = 0
AR-not-scorable = 4
```

This is not exact LIGO residual replay because SXS has no LIGO residual
frontend. It is source-native representation correspondence under frozen
structural rules.

### C2. RAW17 availability-defined support

```text
DEV99 = 99
PATH_FOUND = 98
NO_PATH = 1
raw H1/L1 pairs available = 17
PATH_FOUND with no existing raw pair = 81
ONPATH > OFFPATH = 15/17
NULL200 rare = 16/17
both = 15/17
```

This is not a 98-event raw population result. The exceptions remain reported.

## D. Superseded and technical-hold ledger

### Superseded execution attempts

The following are preserved for audit but are not Paper V authority:

- anchor extension R0/R1/R2/R3/R4 attempts;
- original physical-S phase partition before R1 correction;
- cross-event W0 trigger search R5;
- raw trigger long audit R3;
- thermodynamic activation R0;
- raw-trigger-to-frozen-transition R0;
- final physical-law comparison R0.

### Technical holds that remain honest boundaries

- direct pre-W0 model-absorption/residual comparison;
- direct nonlinear mode-coupling test;
- physical M-Time confirmation against a source-side merger marker.

No technical hold is silently converted into a positive result.

## E. Paper V reportable claim matrix

| Claim | Status | Why |
|---|---|---|
| Frozen RIUD structure exists in DEV lineage | SUPPORTED | Paper IV frozen population/path assets |
| Two-anchor extension preserves the structural gap | SUPPORTED | Frozen Fig-6 extension audit |
| W0/W5 are a new universal population law | NOT CLAIMED | Only sparse two-anchor readout |
| Frozen S law remains the main W1-W4 descriptor | SUPPORTED | Full-map frozen replay |
| W3 post-gap is a separate physical merger time | NOT CLAIMED | Local structural breakdown only |
| M-Time is a reproducible waveform-native object | SUPPORTED | Independent frozen derivation |
| M-Time equals physical merger time | UNRESOLVED | Physical bridge technical hold |
| SXS reproduces path and early topology | PARTIAL/SUPPORTED | Source-native: 10/10 path, 10/10 early topology |
| SXS is exact LIGO residual replication | NOT CLAIMED | Frontend differs |
| Raw support is positive in available inputs | SUPPORTED WITH SCOPE | 15/17 and 16/17 in raw17 |
| Detector/noise causality is isolated | UNRESOLVED | SXS frontend is source-native |
| Existing GR/model failure implies new physics | NOT CLAIMED | Model comparison not same observable |

## F. Recommended paper narrative

The clean narrative is:

```text
Paper IV froze the RIUD object.
Paper V extends the map in two anchors, tests gap persistence,
re-reads W0/W5 without fitting a new law, corrects the W1/W3 scope,
audits raw support and source-native SXS correspondence,
then states exactly which physical interpretations remain open.
```

This lets the author report the full experimental history without mixing
canonical results, diagnostics, superseded runs, and technical holds.

## G. No-new-science invariants

```text
NEW_S_FIT=FALSE
NEW_GAMMA_FIT=FALSE
NEW_MAP=FALSE
NEW_THRESHOLD=FALSE
NEW_NULL=FALSE
R40_REFIT=FALSE
HOLDOUT30_ACCESSED=FALSE
```
