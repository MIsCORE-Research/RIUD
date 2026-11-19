# RIUD Paper V reviewer-attack defense matrix

Status: documentation-only supplement to the authoritative R1 freeze.
No scientific calculation, refit, reselection, threshold change, null generation,
or Holdout30 access was performed for this document.

Package root: `E:/RIUD_ACTIVE_20260808/RIUD_PAPER5_AUTHORITATIVE_FREEZE_R1_20260823`

## Frozen denominator and scope

```text
DEV99=99
PATH_FOUND=98
NO_PATH=1                       GW241230_233618
RAW_AVAILABLE=17                existing H1/L1 pairs
RAW_UNAVAILABLE=81              PATH_FOUND events with no existing raw pair
RAW_AUDITED=17
SXS_PANEL=10
HOLDOUT30_ACCESSED=FALSE
```

The 17-event raw denominator is availability-defined, not outcome-defined.
The raw result is a diagnostic subset result, not a 98-event population result.

## Core defense matrix

### 1. “SXS produced no result, so path-only was invented afterward.”

**Answer:** No. The SXS audit consumes `IS_PATH_NODE=1` rows and applies the
frozen R6 state/topology rule to the path-node history. The output records the
original R6 source and SHA; it does not create a new path after observing SXS
results.

**Evidence:**

- `SXS/SXS_EXTENDED_PATH_ONLY_TOPOLOGY_AUDIT.json`
  - `INPUT_MODE=EXTENDED_REPLAY_IS_PATH_NODE_1_ONLY`
  - `STATE_RULE_SOURCE=...RIUD_DEV99_REENTRY_MULTISTATE_STATE_IDENTITY_AUDIT_R6_20260815/RUN.py`
  - `STATE_RULE_SOURCE_SHA256=27173a2806c9afd888f228f2623691058e098e14e23c01207d9eec7f5bc0fd7e`
  - `NEW_STATE_RULE=false`, `NEW_THRESHOLD=false`, `NEW_FIT=false`
- `REVIEWER_DEFENSE/SOURCE_SNAPSHOT_R6_RUN.py` is the byte-preserved R6 source
  snapshot; SHA256=`27173a2806c9afd888f228f2623691058e098e14e23c01207d9eec7f5bc0fd7e`.
- SHA256: `95b0f5261c7128ccd86b0b6afb1d33da5ff423e4af43723f761be2a2d37beb39`

**Claim status:** SUPPORTED for the frozen R6 path-node application.

### 2. “The raw17 denominator is cherry-picked.”

**Answer:** No. The denominator is obtained by joining the 99-event DEV99
ledger to the existence of both original H1 and L1 4-second files. It is fixed
before support scoring; missing inputs are retained as unavailable.

**Evidence:**

- `RAW17/RIUD_DEV99_EXISTING_RAW_INPUT_INVENTORY.csv`
  - `PATH_FOUND=98`, one `NO_PATH`, 17 complete H1/L1 pairs.
- `RAW17/RIUD_RAW_FROZEN_PATH_SUPPORT_AUDIT_R0_20260823_EXISTING17_SUMMARY.csv`
  - 17 rows, including the two exceptions.
- Inventory SHA256: `3ca0dce1f917937f582f92e058ebcb2d350c9d9af156281ee9c12d48c8a21a03`
- Result SHA256: `2273c9a0c31dec9913ce9c79f58bde520236986af3b1d88a4b564011bb10a7d5`

**Claim status:** SUPPORTED with scope limitation: 17 available-input events only.

### 3. “ONPATH/OFFPATH, corridor, or NULL200 was tuned after seeing results.”

**Answer:** The audit uses the same frozen path-support criterion, matched
off-path controls, serialized 200 event-native controls, and frozen rule/lock
hashes for every audited event. No event-wise threshold or corridor retuning is
present in the output contract.

**Evidence:**

- Each `RAW17/EVENTS/*/RAW_FROZEN_PATH_SUPPORT_SUMMARY.json` records:
  `CONTROL_N=200`, `FROZEN_LOCK_SHA256`, `FROZEN_RULE_SHA256`, and
  `RAW_NULL200_FIXED_CORRIDOR_P`.
- The aggregate result records all 17 rows and the two negative cases.

**Claim status:** SUPPORTED as a frozen diagnostic contract.

### 4. “The SXS Panel10 was selected after looking at RIUD results.”

**Answer:** The SXS branch is a predeclared fixed Panel10 source-native
calibration set. The package freezes the panel outputs and adapter contract;
the result is not used to alter the panel or the RIUD rule.

**Evidence:**

- `SXS/SXS_NATIVE_REPLAY_CONTRACT.txt`
  - one common adapter for all 10 events,
  - common peak-origin rule,
  - common grid/width/frequency/null construction.
- `SXS/SXS_NATIVE_REPLAY_SUMMARY.json`
  - `EVENTS=10`, `EXACT_FROZEN_REPLAY=false`, `NEW_NODE_PATH_RULE=false`.
- Contract SHA256: `4f2ac20b4144905c4ff9562719333fde4aa0abdb6873e20e9278849d334650d3`

**Claim status:** SUPPORTED for fixed-panel source-native replay; not a claim of
random or population-representative SXS sampling.

### 5. “The 6/6 G→AR result excludes four failures after the fact.”

**Answer:** No. The four events are separated by the frozen AR-opportunity
rule: their path ended before the AR-eligible region, so they are
`NOT_SCORABLE_INSUFFICIENT_PATH_SUPPORT`, not topology failures.

**Evidence:**

- `SXS/SXS_EXTENDED_AR_OPPORTUNITY_AUDIT_4EVENTS.json`
  - `NOT_SCORABLE_INSUFFICIENT_PATH_SUPPORT_N=4`
  - `TRUE_TOPOLOGY_NONREPRODUCTION_N=0`
  - all new-rule flags false.
- `SXS/SXS_EXTENDED_PATH_ONLY_TOPOLOGY_AUDIT.json`
  - `G_TO_AR_COUNT=6`, `CORE_N0_A1_G_AR_EVENTS=6`, `REENTRY_EVENTS=6`.

**Claim status:** SUPPORTED as `6/6 scorable; 4/10 not scorable`, not as 10/10
full reentry reproduction.

### 6. “Holdout30 is just an arbitrary set of 30 different event IDs.”

**Answer:** Holdout30 is sealed at the stage/claim boundary defined by the
DEV-to-Holdout validation design. This release does not enumerate, inspect,
copy, or evaluate Holdout30. It is not used to enlarge the raw17 or SXS
denominators.

**Evidence:**

- `LINEAGE/PAPER5_COMPLETE_LINEAGE.md`
  - explicit Holdout30 exclusion.
- `REPRODUCTION_PACKAGE/R40/R40_FINAL_101_PROVENANCE.txt`
  - `HOLDOUT30_ACCESSED=FALSE`.
- R40 provenance SHA256: `d69b9027b677d79dfad40d1d33b15dcbb0134cb19da2a1c2eb437a0652e57f48`.

**Claim status:** SUPPORTED as an access/sealing boundary; no broader
Holdout30 claim is made.

### 7. “The representation changed, so the science rule changed.”

```text
NODE_RULE_CHANGED=FALSE
PATH_RULE_CHANGED=FALSE
INPUT_REPRESENTATION_CHANGED=TRUE
NULL_CONSTRUCTION_CHANGED=TRUE
EXACT_FROZEN_REPLAY=FALSE
SXS_NATIVE_REPLAY=TRUE
```

**Answer:** The SXS adapter changes the source-domain representation required by
SXS; it does not claim to be an exact LIGO residual replay. The frozen
structural rule, R40 coordinate, and no-refit boundary remain explicit.

**Evidence:** `SXS/SXS_NATIVE_REPLAY_CONTRACT.txt` and
`SXS/SXS_NATIVE_REPLAY_SUMMARY.json`.

**Claim status:** SUPPORTED as a representation-level cross-check; exact
detector/noise attribution remains UNRESOLVED.

### 8. “The two raw exceptions were hidden.”

**Answer:** They are explicitly retained:

```text
GW240920_124024  ONPATH_MINUS_OFFPATH=-0.0477205201  P=0.0049751244
GW241231_054133  ONPATH_MINUS_OFFPATH=-0.5658695769  P=0.4726368159
```

The first is rare under NULL200 but direction-negative; the second is both
direction-negative and not rare. They remain in the authoritative 17-row table.

**Claim status:** SUPPORTED negative-result accounting.

### 9. “This proves exact residual/model absorption.”

**Answer:** It does not. The raw17 test is pre-subtraction raw path support, and
the SXS branch is source-native. Exact waveform-model absorption and residual
identity are not claimed.

**Claim status:** UNRESOLVED / NOT CLAIMED.

### 10. “This proves RIUD MT=0 is the physical merger time.”

**Answer:** It does not. M-Time remains a reproducible waveform-native landmark
candidate. Physical merger-time identity was not established.

**Claim status:** NOT CLAIMED.

### 11. “SXS proves the complete N0→A1→G↔AR topology.”

**Answer:** Only the following bounded statement is frozen:

```text
N0→A1→G = 10/10
G→AR     = 6/6 scorable
true failure = 0
4 events = not scorable before AR-eligible region
```

**Claim status:** PARTIAL, not full 10/10 topology reproduction.

### 12. “Unexplained portions are evidence for new physics.”

**Answer:** No. Existing GR/waveform-model inputs are partially consistent, but
the tested objects are not directly comparable as the same observable law.
Model absorption and representation incompleteness remain possible.

**Claim status:** NOT CLAIMED / UNRESOLVED.

## Claim-evidence boundary C1–C10

| Claim | Status | Boundary |
|---|---|---|
| C1 LIGO residual RIUD path | SUPPORTED | Frozen DEV/Paper II–IV lineage |
| C2 population intrinsic dynamics | SUPPORTED | Frozen main-domain global replay |
| C3 N0→A1→G↔AR topology | SUPPORTED / PARTIAL | LIGO frozen topology; SXS partial |
| C4 frozen S-dependent clock law | SUPPORTED | R39/R40 frozen law only |
| C5 SXS PATH_FOUND | SUPPORTED | Source-native 10/10 |
| C6 SXS N0→A1→G | SUPPORTED | Source-native 10/10 |
| C7 SXS G↔AR | PARTIAL | 6/6 scorable; 4 not scorable; true failure 0 |
| C8 finite support | SUPPORTED | Search-support audit, no boundary touch |
| C9 prior waveform/model correspondence | PARTIAL | Existing structural correspondence; exact absorption unresolved |
| C10 causal axis separation | PARTIAL / UNRESOLVED | Pure-GR absence not supported; detector/model attribution unresolved |

## Negative-result ledger

| Item | Frozen accounting | Interpretation |
|---|---:|---|
| DEV99 NO_PATH | 1 (`GW241230_233618`) | Separate scientific state; not mixed into PATH_FOUND |
| RAW input unavailable | 81 PATH_FOUND events | No raw score invented or imputed |
| RAW direction exception | 2/17 | Preserved in result table |
| RAW both-criteria support | 15/17 | Available-input diagnostic only |
| SXS AR not scorable | 4/10 | Path ended before AR opportunity |
| SXS true AR failure | 0 | No post hoc exception rule |
| Physical MT identity | unresolved | Not converted into merger-time claim |
| Exact model absorption | unresolved | Not converted into new-physics claim |
| Nonlinear mode-coupling direct test | technical hold | Missing predeclared mode-resolved asset |

## Final defense sentence

The frozen evidence supports the RIUD main-domain structural/clock result and
bounded cross-representation diagnostics, while explicitly preserving missing
inputs, not-scorable cases, technical holds, representation changes, and
unresolved exact model-absorption/physical-merger-time questions.
