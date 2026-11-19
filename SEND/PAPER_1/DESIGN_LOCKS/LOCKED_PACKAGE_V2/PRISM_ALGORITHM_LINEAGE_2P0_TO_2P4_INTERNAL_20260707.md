# PRISM Algorithm Lineage 2.0 to 2.4
Date: 2026-07-07
Status: Internal algorithm-lineage document
Scope: PRISM 2.0 / 2.1 / 2.2 / 2.3 / planned 2.4 cleanup-hardening

---

## 0. Purpose

This document records the algorithmic evolution of PRISM from early residual-morphology exploration to the locked PRISM 2.2/2.3 validation package and the planned PRISM 2.4 cleanup/hardening stage.

This is not a discovery-claim document.

The purpose is to preserve:

1. what question each version asked,
2. what input class it used,
3. what transformation or rule was introduced,
4. what output was produced,
5. what limitation remained,
6. why the next version became necessary.

---

## 1. Global Claim Boundary

This lineage document does not claim:

- confirmed detection
- new physics established
- GR falsification
- LVK/LIGO error
- formal waveform-family robustness closure
- full raw end-to-end discovery reproduction

Current safe status:

PRISM 2.2/2.3 is a locked, background-calibrated residual-morphology candidate package with successful internal validation and external-style cleanroom reproduction anchors, intended for independent technical review.

---

## 2. High-Level Version Map

| Version | Core Question | Algorithmic Role | Current Status |
|---|---|---|---|
| PRISM 2.0 | Can meaningful post-GR residual structure be examined morphologically? | Residual-morphology exploration begins | Exploratory foundation |
| PRISM 2.1 | Do repeated residual structures appear across candidate events? | Candidate grouping and anomaly pattern exploration | Transitional exploratory stage |
| PRISM 2.2 | Can residual-ridge candidates be locked and validated against background? | Locked residual-ridge candidate validation | Locked candidate package |
| PRISM 2.3 | Can a quiet-to-burst rule be frozen and reproduced on holdout targets? | QTB R1 frozen-input holdout validation | Byte-identical reproduction achieved |
| PRISM 2.4 | Can external reproducibility be cleaned and hardened further? | Path cleanup, sidecar cleanup, warning reduction | Planned / optional hardening |

---

## 3. One-Line Algorithm Evolution

PRISM evolved from an exploratory residual-morphology search into a locked, background-calibrated candidate-validation workflow, culminating in a frozen-input PRISM 2.3 reproduction path and an external-style cleanroom validator package.

Korean summary:

PRISM은 초기 residual-morphology 탐색에서 출발해, 2.2에서 locked residual-ridge 후보 검증 구조로 고정되었고, 2.3에서 frozen-input QTB holdout 재현 경로와 외부형 cleanroom validator package로 정리되었다.

---

## 4. PRISM 2.0: Residual-Morphology Exploration

### 4.1 Core Question

After subtracting or accounting for standard GR waveform structure, can the remaining residual data be examined as a morphology problem rather than as ordinary noise?

### 4.2 Algorithmic Idea

PRISM 2.0 introduced the working viewpoint:

- look at post-GR residual behavior,
- search for structured morphology rather than only scalar excess,
- treat detector-paired residual shape as potentially informative,
- avoid claiming discovery from a single event or single statistic.

### 4.3 Input Class

General input class:

- public gravitational-wave event strain data,
- GR waveform-subtracted or GR-referenced residual products,
- event-centered residual windows,
- detector-pair information, mainly H1/L1.

### 4.4 Processing Logic

PRISM 2.0 was not yet a locked validation protocol.

It functioned as an exploration layer:

1. obtain event-centered residual representation,
2. inspect residual morphology,
3. compare H1/L1 behavior,
4. identify possible coherent structures,
5. record whether residual structures are event-specific noise or repeated candidate patterns.

### 4.5 Output

Output type:

- exploratory residual-morphology observations,
- early candidate structures,
- informal signal-shape impressions,
- basis for later rule design.

### 4.6 Limitation

Main limitations:

- exploratory,
- no locked rule,
- no clean background-calibrated candidate package,
- vulnerable to look-elsewhere criticism,
- not independently reproducible as a frozen protocol.

### 4.7 Why Move to 2.1

2.0 showed that residual-morphology inspection was worth pursuing, but it needed candidate grouping and repeated-structure checks.

Therefore PRISM moved toward a more organized candidate-pattern exploration stage.

---

## 5. PRISM 2.1: Candidate Structure and Pattern Exploration

### 5.1 Core Question

Do similar residual structures appear across multiple events, and can they be grouped into candidate morphology classes?

### 5.2 Algorithmic Idea

PRISM 2.1 shifted from single-event inspection to repeated candidate structure.

The algorithmic focus became:

- compare residual structures across events,
- group similar morphology,
- look for recurring frequency/time/lag behavior,
- separate isolated anomalies from repeated residual fingerprints.

### 5.3 Input Class

Input class:

- candidate event residual windows,
- H1/L1 residual morphology,
- frequency-window or time-window diagnostics,
- preliminary event grouping outputs from 2.0-style exploration.

### 5.4 Processing Logic

General processing:

1. collect residual morphology candidates,
2. compare candidate windows across events,
3. search for repeated patterns,
4. test whether structures are detector-paired or single-detector artifacts,
5. identify whether a candidate structure deserves locking.

### 5.5 Output

Output type:

- candidate groupings,
- anomaly classes,
- preliminary repeat-pattern evidence,
- candidate rules for possible locking.

### 5.6 Limitation

Main limitations:

- still exploratory,
- rule selection not yet frozen,
- background calibration not yet the central structure,
- vulnerable to “candidate chosen after looking” criticism.

### 5.7 Why Move to 2.2

2.1 created candidate structures, but the project needed a locked validation object.

Therefore PRISM moved to 2.2: lock a residual-ridge candidate rule and test it against background.

---

## 6. PRISM 2.2: Locked Residual-Ridge Candidate Validation

### 6.1 Core Question

Can a residual-ridge morphology candidate be locked and validated as a background-calibrated candidate package?

### 6.2 Algorithmic Idea

PRISM 2.2 converted exploration into a locked candidate-validation workflow.

Core shift:

- from “searching for interesting residual structure”
- to “testing a locked residual-ridge candidate against background.”

### 6.3 Input Class

Input class:

- locked event/candidate set,
- locked residual-ridge windows,
- H1/L1 residual morphology products,
- background or time-slide comparison outputs,
- locked CSV/summary validation outputs.

### 6.4 Processing Logic

General processing:

1. use locked candidate windows,
2. compute residual-ridge morphology score,
3. compare candidate score against background,
4. record exceedance count,
5. preserve locked output table,
6. produce locked CSV/summary evidence.

### 6.5 Key Current Anchors

Current locked validation/reproduction status includes:

- PRISM 2.2 locked CSV byte-identical reproduction: PASS
- PRISM 2.2 HOME CSV byte-identical to locked CSV: PASS
- PRISM 2.2 remains a locked residual-ridge candidate package, not a confirmed detection claim.

### 6.6 Known Packaging Limitation

The legacy PRISM 2.2 script still has external-packaging issues:

- hardcoded HOME/output paths,
- possible GR-parameter sidecar dependency,
- script-level isolated cleanroom behavior not fully cleaned.

These are packaging/reproducibility hardening issues, not current evidence-anchor failures.

### 6.7 Output

Output type:

- locked residual-ridge CSV,
- locked summary,
- candidate-background comparison,
- byte-identical locked CSV reproduction anchor.

### 6.8 Limitation

Main limitations:

- legacy path assumptions,
- sidecar dependency cleanup still useful,
- not yet a polished external script-level package,
- still candidate status.

### 6.9 Why Move to 2.3

2.2 established a locked residual-ridge candidate structure, but a stronger holdout-style frozen-input rule was needed.

Therefore PRISM moved to 2.3: QTB rule, holdout evaluation, and frozen-input reproduction.

---

## 7. PRISM 2.3: QTB Frozen-Input Holdout Validation

### 7.1 Core Question

Can a quiet-to-burst morphology rule be frozen and reproduced on holdout targets?

### 7.2 Algorithmic Idea

PRISM 2.3 introduced the R1 QTB rule.

QTB means quiet-to-burst morphology:

- quiet background behavior before/around candidate region,
- coherent burst-like behavior in target window,
- detector-paired H1/L1 residual contrast,
- rule evaluated against valid-slide background.

### 7.3 Core Rule Concept

The internal rule concept:

- quiet gate: based on valid slide-background max quiet RMS distribution,
- burst gate: requires sufficiently strong H1/L1 burst structure,
- contrast gate: requires sufficiently strong H1/L1 quiet-to-burst contrast,
- score: coherent burst multiplied by minimum contrast and quiet-depth factor,
- background: empirical valid-slide calibration.

### 7.4 Primary Holdout Boundary

Primary PRISM 2.3 holdout events:

- GW150914
- GW170104

Diagnostic/reference event:

- GW190521_074359

Catalog-extension candidate:

- GW170814

Important boundary:

GW190521_074359 is not used as the primary claim target for the 2.3 holdout rule because it contributed to diagnostic/rule-development context.

### 7.5 Frozen-Input Reproduction

Current PRISM 2.3 external-style reproduction anchor:

- EXP15 frozen-input reproduction: PASS
- output comparison: byte-identical=7, different=0
- locked anchor produced: PASS

### 7.6 Output

Output type:

- frozen-input holdout output,
- valid-slide empirical result,
- locked anchor output,
- byte-identical reproduction evidence.

### 7.7 Limitation

Main limitations:

- still a candidate package,
- not independent external validation yet,
- not confirmed detection,
- not proof of new physics,
- full raw end-to-end discovery reproduction not claimed.

### 7.8 Why Move to External Validator Packaging

2.3 produced a stronger locked/frozen result, but reviewability required external-style packaging.

Therefore CLEAN_V4, the minimal external input bundle, and V3 external validator kit were created.

---

## 8. EXP17D Supporting Addendum

### 8.1 Role

EXP17D is a supporting waveform-family sensitivity addendum.

It is not the main locked PRISM 2.2/2.3 result.

### 8.2 What It Supports

EXP17D supports the idea that the residual-morphology candidate structure is not trivially removed by several Phenom-family waveform substitutions.

It is best described as:

- positive informal waveform-family sensitivity result,
- supporting systematic diagnostic,
- not formal waveform-family robustness closure.

### 8.3 Boundary

EXP17D does not prove:

- waveform robustness,
- SEOBNR confirmation,
- confirmed detection,
- new physics,
- GR falsification.

---

## 9. External-Style Validation Packaging

### 9.1 Created Packages

Current external/reviewer package state:

1. `PRISM_VALIDATION_CLEAN_V4_WITH_EXP17D_20260707.zip`
2. `PRISM_MINIMAL_EXTERNAL_REPRO_INPUT_BUNDLE_V1_20260707.zip`
3. `PRISM_VALIDATOR_REPRO_KIT_V3_EXTERNAL_20260707.zip`
4. `PRISM_EXTERNAL_REVIEWER_SENDKIT_V1_20260707.zip`
5. `PRISM_FULL_LOCKED_PACKAGE_V1_20260707.zip`

### 9.2 Final SHA Records

Reviewer sendkit:

`PRISM_EXTERNAL_REVIEWER_SENDKIT_V1_20260707.zip`

SHA256:

`801b812d3aece72893baa119f0ab5bc25cd84b29ff3438235e8142ca872db496`

Internal full locked package:

`PRISM_FULL_LOCKED_PACKAGE_V1_20260707.zip`

SHA256:

`9c76a7d36e8ead05b4ec5d524856d395c12ae35ffb41e4c86e19260e512bc979`

Core package SHA records:

`PRISM_VALIDATION_CLEAN_V4_WITH_EXP17D_20260707.zip`

SHA256:

`01664685820f8d7dc53b4d93e6380c71101700de0335f95b05025c1cb24b7704`

`PRISM_MINIMAL_EXTERNAL_REPRO_INPUT_BUNDLE_V1_20260707.zip`

SHA256:

`2f1a9e664cd9b3b3003d4798fa5522072d3dbd40bd46819a0edc06da635d57ac`

`PRISM_VALIDATOR_REPRO_KIT_V3_EXTERNAL_20260707.zip`

SHA256:

`3f5861bca078bbb8092145665f674309ba62c091897ddd25697c81a7c513f457`

### 9.3 V3 External Cleanroom Simulation

Final V3 external-style cleanroom simulation status:

- PASS: 8
- WARN: 0
- FAIL: 0

Core anchors:

- PRISM 2.3 EXP15 byte-identical reproduction: PASS
- PRISM 2.3 locked anchor produced: PASS
- PRISM 2.2 locked CSV byte-identical: PASS
- Raw GWOSC smoke PASS: PASS
- CLEAN_V4 first-pass FAIL=0: PASS

---

## 10. Planned PRISM 2.4: Cleanup and Reproducibility Hardening

### 10.1 Status

PRISM 2.4 is not yet completed.

It is a planned cleanup/hardening layer, not a required condition for the current 2.2/2.3 reviewer package.

### 10.2 Core Question

Can the external reproducibility path be made cleaner, with fewer warnings and fewer legacy assumptions?

### 10.3 Planned Work

Potential 2.4 tasks:

1. remove PRISM 2.2 hardcoded HOME/output path assumptions,
2. package or eliminate PRISM 2.2 GR-parameter sidecar dependency,
3. reduce validator warnings,
4. make PRISM 2.2 isolated script-level cleanroom reproduction cleaner,
5. improve external reviewer UX,
6. preserve the existing 2.2/2.3 locked anchors without changing the locked results.

### 10.4 Boundary

PRISM 2.4 must not silently change the locked PRISM 2.2/2.3 results.

If 2.4 changes scripts, it must preserve:

- PRISM 2.3 byte-identical reproduction,
- PRISM 2.3 locked anchor production,
- PRISM 2.2 locked CSV identity,
- CLEAN_V4 package integrity,
- V3 external-style cleanroom validation behavior or a clearly documented successor.

### 10.5 Why 2.4 Is Optional

The current 2.2/2.3 reviewer package already passes the external-style cleanroom validator.

Therefore 2.4 is a cleanup/hardening phase, not a rescue phase.

---

## 11. Frozen vs Exploratory Separation

### 11.1 Frozen / Locked

Frozen or locked items:

- PRISM 2.2 locked residual-ridge CSV/summary outputs,
- PRISM 2.3 EXP15 frozen-input reproduction path,
- QTB R1 holdout rule boundary,
- CLEAN_V4 validation package,
- V3 external-style validator package,
- SHA-locked reviewer sendkit and full locked package.

### 11.2 Exploratory / Historical

Exploratory or historical items:

- early PRISM 2.0 residual inspections,
- PRISM 2.1 candidate grouping,
- abandoned rules,
- failed branches,
- A7/Core3/PRISM-Core branches,
- informal search history,
- raw full engine/data.

### 11.3 Separation Rule

Exploratory history may explain the algorithmic lineage, but it must not be mixed into the locked 2.2/2.3 claim boundary.

---

## 12. Algorithm Flow Diagram

```text
PRISM 2.0
Residual-morphology exploration
        |
        v
PRISM 2.1
Repeated candidate structure / anomaly grouping
        |
        v
PRISM 2.2
Locked residual-ridge candidate validation
        |
        v
PRISM 2.3
QTB R1 frozen-input holdout reproduction
        |
        v
CLEAN_V4 + EXP17D + V3 External Validator
External-style cleanroom validation anchors PASS
        |
        v
PRISM 2.4 planned
Cleanup / hardening / warning reduction
```

---

## 13. Safe External Description

A safe external description:

PRISM 2.2/2.3 is a locked, background-calibrated residual-morphology candidate package. It includes a PRISM 2.3 frozen-input reproduction path and an external-style validator kit that reproduced the core locked anchors in a cleanroom simulation with FAIL=0. The package is intended for independent technical review and does not claim confirmed detection, new physics established, GR falsification, or full raw end-to-end discovery reproduction.

---

## 14. Current Final Status

As of 2026-07-07:

- PRISM 2.2/2.3 validation/reviewer package phase: DONE
- External-style cleanroom validation: PASS
- Reviewer sendkit: CREATED
- Internal full locked package: CREATED
- PRISM 2.4 cleanup/hardening: OPTIONAL / LATER
- Raw full cold backup: NOT REQUIRED BEFORE 2.4

