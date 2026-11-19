# RIUD Paper V — Complete Master Record

**Revision:** R4, 2026-08-24  
**Purpose:** One readable master record combining the Paper5 lineage, frozen scientific results, diagnostics, claim boundaries, archive audit, and the 2026-08-24 final append.

Earlier result folders and the R1 authority release are preserved unchanged. This document is a synthesis and index; it does not replace the underlying CSV, JSON, manifest, or source files.

## 1. Final status

```text
R_STATUS=PAPER5_COMPLETE_MASTER_AUDIT_PASS
PAPER5_STAGE_COUNT=62
PAPER5_MAIN=18
PAPER5_DIAGNOSTIC=30
PAPER5_SUPERSEDED=11
STAGE_CLASS_TECHNICAL_HOLD=3
ACTIVE_TECHNICAL_HOLDS=0
CLOSED_TECHNICAL_BOUNDARIES=3
TODAY_CANONICAL_APPEND_BRANCHES=4
SCIENCE_RESULT_MISSING=FALSE
HOLDOUT30_ACCESSED=FALSE
CANONICAL_GLOBAL_MAP_REWRITTEN=FALSE
CANONICAL_R40_S_REFIT=FALSE
CANONICAL_GAMMA_REFIT=FALSE
CANONICAL_THRESHOLD_CHANGED=FALSE
CANONICAL_NULL_CHANGED=FALSE
APPEND_BRANCH_LOCAL_MAPS_BUILT=TRUE
APPEND_BRANCH_LOCAL_EXPLORATORY_S_DISCOVERY=TRUE
R40_REFIT=FALSE
```

The authoritative source TSV was re-read directly. It contains 62 rows, with class counts MAIN=18, DIAGNOSTIC=30, SUPERSEDED=11, and TECHNICAL_HOLD=3. The four 2026-08-24 append branches are separately indexed and are not included in this base lineage count.

## 2. Executive scientific result

Paper V is a continuation of the frozen Paper IV RIUD object, not one new experiment. Its main evidence chain is:

```text
frozen DEV/PATH object
→ two-anchor map extension
→ persistent color-free depletion gap
→ corrected W1/W2/W3/W4 scope
→ frozen physical-S transition-rate law
→ raw17 availability-defined support audit
→ source-native pure-GR SXS structural replay
→ explicit physical/source interpretation limits
```

The defensible overall claim is:

> A frozen RIUD structural transition object persists under the two-anchor extension and shows partial source-native correspondence in pure-GR SXS. Its exact detector/source identity, physical merger-time identity, common physical-law identity across representations, and causal interpretation remain unresolved.

No GR-violation or new-physics claim is established.

## 3. Frozen Paper IV objects inherited by Paper V

```text
GLOBAL_MAP_ROWS=1077
GLOBAL_MAP_EVENTS=97
PHYSICAL_S_SUPPORT=96
GAP_LEFT_LATENT=0.0182607298884202
GAP_RIGHT_LATENT=0.0198413898273119
GAP_CENTER_LATENT=0.01905105985786605
S=0.22030031492055946*z(R)+0.3457660274266933*z(CHI_A_NORMALIZED)
GAMMA=0.3162354634393393
STATE_GRAPH=N0→A1→G→AR with G↔AR re-entry
```

The inherited R40 law and coefficients are not refit in the Paper5 main branch.

## 4. Main Paper5 lineage

### 4.1 Two-anchor extension and gap persistence

Canonical anchors:

```text
GW240601_061200
GW231221_135041
```

The extended search support was approximately `-1.00..+1.00 s`. The two-anchor path ranges were approximately:

```text
GW240601: -0.04..+0.28 s
GW231221: -0.11..+0.20 s
```

The Figure-6 color-free gap survived both extensions. No new node entered the frozen gap. The minimal extended anchor map contains 5 events and 75 rows. The canonical 97-event map was not rewritten.

The extension-specific W0/W5 readout is sparse and event-specific:

```text
GW240601: W0 transitions=0, W5 transitions=4
GW231221: W0 transitions=2, W5 transitions=0
```

Therefore W0/W5 are not established as a universal population law.

### 4.2 Gap, t0 and M-Time boundary

The gap is an independently discovered color-free latent depletion, not a red-dot or AT_ZERO definition. Nominal waveform `t=0`, GAP, MT, PEAK, and MAX_FLOW remain distinct landmarks.

The M-Time object is reproducible as a waveform-native temporal candidate. It is not confirmed as first common apparent-horizon formation or as a unique physical merger time.

Two-anchor native gap-midpoint offsets were approximately:

```text
GW240601: -6.910111 ms relative to t0
GW231221: -2.091138 ms relative to t0
```

The blind gap/time audit did not support a common GAP midpoint identity with MT/t0.

### 4.3 Corrected W-window terminology

```text
W0   = sparse extension-only preparation/diagnostic prefix
W1   = canonical primary start-to-peak scope
W2   = peak-to-end
W3   = event-specific pre-MT/start-to-MT structural phase
W4   = event-specific MT-to-end phase
W5   = extension-only post-support diagnostic where present
```

W1-0 is preparation, not the canonical primary W1 law domain. The corrected W1 primary start is the frozen L1-start rule. W3 post-gap behavior is recorded as a local structural interruption/breakdown, not as proof that W3 is merger time.

### 4.4 Frozen physical-S law

```text
S = 0.22030031492055946*z(R)
  + 0.3457660274266933*z(CHI_A_NORMALIZED)

gamma = 0.3162354634393393
lambda = exp(eta)
p = 1-exp(-lambda*du)
```

The frozen law supports the main W1/W2/W3-pre-gap/W4 domain. W0 has only sparse activation evidence. The direct nonlinear mode-coupling stage is a closed unresolved technical boundary because the required predeclared mode-resolved asset was unavailable.

## 5. Raw and known-physics diagnostics

The raw sequence was described as:

```text
oscillation/zero-crossing activity
→ frequency relaxation
→ envelope/amplitude rise
→ frozen downstream progression
```

This remains a descriptive trigger candidate, not a universal causal trigger. Existing known-physics audits did not identify a unique cause. QNM-scale testing was insufficient to explain the raw sequence/S relation. Unexplained does not equal new physics.

The residual-to-S source identity was not established from the frozen assets. Component and multi-law audits support a descriptive relational state/clock/boundary decomposition, not a fundamental GR law.

## 6. Cross-domain frozen diagnostics

### 6.1 RAW17 availability-defined audit

```text
DEV99=99
PATH_FOUND=98
NO_PATH=1
RAW_H1/L1_PAIRS_AVAILABLE=17
PATH_FOUND_WITHOUT_EXISTING_RAW_PAIR=81
ONPATH>OFFPATH=15/17
NULL200_RARE=16/17
BOTH=15/17
```

This is an availability-defined 17-event diagnostic, not a 98-event raw population claim. The NO_PATH event is kept separate.

### 6.2 Pure-GR SXS source-native replay

SXS lacks the exact detector-realized LIGO noise/model-subtraction frontend. The earlier 10-event test is a source-native structural replay under frozen structural rules, whereas the 2026-08-24 matched GR16 append is a separate low-strain residual representation. Neither is an exact replication of the detector residual frontend.

```text
PATH_FOUND=10/10
N0→A1→G=10/10
G→AR=6/6 AR-scorable
TRUE_TOPOLOGY_NONREPRODUCTION=0
AR_NOT_SCORABLE=4
```

This supports cross-representation structural correspondence, but not exact detector/noise attribution and not exact LIGO residual R40 replay.

## 7. 2026-08-24 final append

### 7.1 Observation-only integrated frequency families

The exact PATH × A2 intersection was classified before attaching physical variables. Inputs included frequency magnitude, frequency shape, GAP, native t0, MT, PEAK, MAX_FLOW, available W/support fields, and A2 descriptors. ABC, frozen S, gamma, legacy H labels, width, transition, node count, and source path were not family inputs.

```text
INT_1=63
INT_2=33
```

This is an observational morphology/frequency partition, not a new physical law.

### 7.2 Frozen physical append

After the labels were frozen, R40 `S_KERR_ORDINAL` and frozen gamma were attached descriptively.

| Quantity | INT_1 | INT_2 |
|---|---:|---:|
| Events | 63 | 33 |
| Frozen S mean | 0.0258324 | -0.0372166 |
| Frozen S median | -0.0073735 | -0.0485431 |
| gamma*S mean | 0.0081691 | -0.0117692 |
| gamma*S up/down | 31/32 | 16/16 |
| R mean | 0.916309 | 0.911358 |
| CHI_A mean | 0.189911 | 0.166732 |
| A2 score mean | 3.08301 | 2.85863 |
| MAX_FLOW mean | 18.49 ms | 21.29 ms |
| GAP mean | -3.526 ms | -3.428 ms |
| PEAK mean | 57.81 ms | 61.48 ms |

`GW150914_095045` belongs to INT_2 but has no matching frozen R40 S row. Thus the S comparison is 63 versus 32 available rows. The S effect is Cohen's d=0.158, with substantial overlap. This is weak descriptive separation, not evidence for two distinct physical populations. No family-specific rate fit was performed.

### 7.3 A2 / ABC / H-family pairwise audit

```text
A2×ABC=96
A2×H-family=13
ABC×H-family=12
A2×ABC×H-family=12
```

Pairwise joins are not replaced by the triple intersection. Native t0 is the reference baseline. A2 remains a descriptive bank and does not define a new canonical time or classifier.

### 7.4 Early-MAX_FLOW16 matched Pure-GR branch

```text
MATCHED_SOURCE_INPUTS=16/16
GR16_PATH_FOUND=16/16
GR16_NODE_ROWS=136
OBS16_MAP_NODES=196
GR16_MAP_NODES=136
OBS16_DIRECTED_EDGES=240/240
GR16_DIRECTED_EDGES=240/240
```

Independent branch-local exploratory S discovery selected different axes:

```text
OBS16=M_DET+MC_DET
GR16=CHI_P
S_EVENT_PEARSON=0.517259957841
SAME_AXIS_SELECTED=FALSE
```

The branch therefore does not establish a common physical S axis or exact R40 rate-law reproduction. Its final status is `TECHNICALLY_INCONCLUSIVE_SOURCE_MATCH` for common physical-law validation.

### 7.5 A-only branch status

The A-only branch is a separate append-branch exploratory discovery, not a rewrite of the canonical 97-event global map or the canonical R40 law.

```text
A_ONLY_BRANCH_STATUS=APPEND_BRANCH_LOCAL_EXPLORATORY
A_ONLY_GEOMETRY_COHORT=74
A_ONLY_PHYSICAL_COHORT=73
A_ONLY_S_DISCOVERY=TRUE
A_ONLY_S_VARIABLES=R|CHI_A
A_ONLY_GAMMA_REFIT=TRUE
A_ONLY_BASE_RATE_REBUILT=TRUE
A_ONLY_DEV_W1_W2_W3_W4_DIRECTION=4/4_POSITIVE
A_ONLY_SXS_REPLAY=SOURCE_NATIVE_COMPLETED_WITH_EXISTING_SCOPE_LIMITS
A_ONLY_AUTHORITY=E:/RIUD_ACTIVE_20260808/RIUD_A_ONLY_TRUE_PHYSICAL_S_DISCOVERY_RATE_REBUILD_R0_20260824
```

This branch-local S and rate law are reported for provenance and exploratory comparison only. They do not replace frozen global `S`, gamma, map, or R40 results.

## 8. Claim/evidence matrix

| Claim | Status | Boundary |
|---|---|---|
| Frozen RIUD structure exists in DEV lineage | SUPPORTED | Paper IV frozen population/path assets |
| Two-anchor extension preserves structural gap | SUPPORTED | Figure-6 extension audit |
| W0/W5 are a universal population law | NOT CLAIMED | Sparse event-specific extension readout |
| Frozen S remains main W1-W4 descriptor | SUPPORTED | Frozen global replay |
| W3 post-gap is a physical merger-time identity | NOT CLAIMED | Local structural breakdown only |
| M-Time is reproducible waveform-native object | SUPPORTED | Frozen independent derivation |
| M-Time equals physical merger time | UNRESOLVED | Closed unresolved source-side bridge boundary |
| SXS reproduces path and early topology | PARTIAL/SUPPORTED | Source-native 10/10 path, 10/10 early topology |
| SXS is exact LIGO residual replication | NOT CLAIMED | Frontend representation differs |
| Raw support is positive in available inputs | SUPPORTED WITH SCOPE | 15/17 and 16/17 only |
| Detector/noise causality isolated | UNRESOLVED | Source-native SXS frontend |
| Existing GR/model failure implies new physics | NOT CLAIMED | Not the same observable/law |
| INT_1/INT_2 observed structural split | SUPPORTED | Frozen observation-only 63/33 census |
| INT_1/INT_2 are distinct physical populations | NOT ESTABLISHED | Weak S contrast, overlapping direction counts |
| Same S axis is recovered in GR16 | NOT ESTABLISHED | Branch-local selected variables differ |

## 9. Main, diagnostic, superseded and technical-hold separation

```text
MAIN=18
DIAGNOSTIC=30
SUPERSEDED=11
STAGE_CLASS_TECHNICAL_HOLD=3
ACTIVE_TECHNICAL_HOLDS=0
CLOSED_TECHNICAL_BOUNDARIES=3
TOTAL_BASE_LINEAGE=62
```

Superseded attempts remain archived and are not used as authority: early anchor retries, pre-correction phase partitions, early cross-event W0 framing, raw trigger R3, thermodynamic R0, and earlier final-comparison R0.

Three historical stage entries retain the `TECHNICAL_HOLD` lineage class. All three are operationally closed as explicit unresolved evidence boundaries. They are not active experiments and are not scientifically resolved.

## 10. Completeness and integrity audit

```text
CATALOG_STAGE_DIRECTORIES=62/62
AUTHORITY_INDEX_ROWS=179
AUTHORITY_FILES_PRESENT=179/179
AUTHORITY_SHA_MATCH=179/179
R1_FREEZE_MANIFEST=PASS
RAW17_MANIFESTS=PASS
R2_APPEND_MANIFEST=PASS
STAGE_COUNT_SOURCE_RECHECK=PASS
CLASS_COUNT_SUM=62
```

The four 2026-08-24 append branches are recorded in `PAPER5_STAGE_CATALOG_APPEND_20260824.tsv`. Detailed evidence remains in the original source folders and is indexed by `PAPER5_TODAY_SOURCE_INDEX.tsv`.

## 11. Reproduction and scope invariants

```text
CANONICAL_R40_S_REFIT=FALSE
CANONICAL_GAMMA_REFIT=FALSE
CANONICAL_GLOBAL_MAP_REWRITTEN=FALSE
CANONICAL_THRESHOLD_CHANGED=FALSE
CANONICAL_NULL_CHANGED=FALSE
APPEND_BRANCH_LOCAL_MAPS_BUILT=TRUE
APPEND_BRANCH_LOCAL_EXPLORATORY_S_DISCOVERY=TRUE
R40_REFIT=FALSE
HOLDOUT30_ACCESSED=FALSE
```

The Paper5 master is ready for manuscript/report use with the above claim boundaries. It must not be used to claim exact SXS R40 replay, physical M-Time equality, a universal W0 trigger, GR violation, or new physics.

## 12. Source-of-truth files

- Prior Paper5 lineage: `RIUD_PAPER5_COMPLETE_LINEAGE_SUMMARY_R1_20260822/PAPER5_COMPLETE_LINEAGE.md`
- Prior authoritative freeze: `RIUD_PAPER5_AUTHORITATIVE_FREEZE_R1_20260823/PAPER5_FINAL_REPORT.md`
- Full experiment audit: `RIUD_PAPER5_AUTHORITATIVE_FREEZE_R1_20260823/PAPER5_FULL_EXPERIMENT_AUDIT.md`
- Existing stage catalog: `RIUD_PAPER5_COMPLETE_LINEAGE_SUMMARY_R1_20260822/PAPER5_STAGE_CATALOG.tsv`
- Existing authority index: `RIUD_PAPER5_COMPLETE_LINEAGE_SUMMARY_R1_20260822/PAPER5_AUTHORITY_FILE_INDEX.tsv`
- 2026-08-24 stage append: `PAPER5_STAGE_CATALOG_APPEND_20260824.tsv`
- 2026-08-24 source index: `PAPER5_TODAY_SOURCE_INDEX.tsv`
- 2026-08-24 documentation audit: `PAPER5_DOCUMENTATION_AUDIT.md`

## 13. Technical-hold closure (2026-08-24)

The three technical-hold branches were re-audited against the later frozen and SXS assets. They are now closed as explicit unresolved evidence boundaries; none was upgraded to a scientific positive or negative result.

| Hold | Closure status | What is established | What remains unavailable | Claim boundary |
|---|---|---|---|---|
| Pre-W0 model absorption | `CLOSED_UNRESOLVED_EXACT_MODEL_LAYER_MISSING` | Frozen residual readout retains phase-coherence and zero-crossing structures; audit code and residual provenance are present | Standalone deterministic model waveform and exact paired source raw input | No exact model-absorption or residual-disappearance claim |
| Direct nonlinear mode coupling | `CLOSED_UNRESOLVED_MODE_DECOMPOSITION_MISSING` | 96-event schema audit and later fixed Kerr/QNM scale crosswalk exist; QNM crosswalk is descriptive only | Event-level parent/child frequencies, amplitudes and phases | No direct 2f1/2f2/f1+f2/|f1-f2|, quadratic/product, or phase-combination claim |
| Physical M-Time confirmation | `CLOSED_UNRESOLVED_OFFICIAL_TRANSFER_INPUTS_MISSING` | Official SXS u(T) formula and AhC horizon diagnostics are documented; horizon HDF5 files contain horizon mass/spin/center products | Event-matched finite-radius r_j(T), g_TT,j(T), and M_ADM transfer inputs; exact SXS R40 history contract | No physical equality between M-Time and first common-horizon time |

The later SXS R40 audit independently preserves the same boundary: `R40_COMPATIBLE_MT0=NOT_RESOLVED`, `R8_HISTORY=PARTIAL_NOT_EXACT`, `R9_HISTORY=PARTIAL_NOT_EXACT`, and `EXACT_W1_W4_SCORING=NOT_RUN`. Its reconstructed W1-W4 likelihood is retained as reconstructed aggregate direction only, not as exact R40 validation.

Closure ledger: `E:/RIUD_ACTIVE_20260808/RIUD_PAPER5_TECHNICAL_HOLD_CLOSURE_R0_20260824/`.

```text
TECHNICAL_HOLDS_CLOSED=3
TECHNICAL_HOLDS_SCIENTIFICALLY_RESOLVED=0
SCIENCE_RERUN=FALSE
CANONICAL_R40_S_REFIT=FALSE
CANONICAL_GAMMA_REFIT=FALSE
CANONICAL_GLOBAL_MAP_REWRITTEN=FALSE
CANONICAL_THRESHOLD_CHANGED=FALSE
CANONICAL_NULL_CHANGED=FALSE
APPEND_BRANCH_LOCAL_MAPS_BUILT=TRUE
APPEND_BRANCH_LOCAL_EXPLORATORY_S_DISCOVERY=TRUE
HOLDOUT30_ACCESSED=FALSE
```
