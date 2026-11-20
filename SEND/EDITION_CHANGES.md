# EDITION CHANGES — SEND trace/dependency pass (2026-10-29)

This file records every change made inside `E:\SEND` during the trace-removal /
dependency-removal pass of 2026-10-29 (20:05–20:31 KST). Scope was `E:\SEND`
only; the archive and the package working copies were not touched.

## Evidence basis and limits

- Changes were established by SHA-256 comparison of the pre-edit backup
  (`pre_edit_backup.zip`, 98 target files captured before editing) against the
  post-pass state of `E:\SEND`: **55 files changed, 42 files byte-identical,
  1 file removed**.
- The pass's per-action edit log (`edit_log.json`) was not retained in the work
  folder, so no claim is made here beyond what the backup comparison and the
  surviving pass logs (`scan_summary.json`, `edit3_log.json`,
  `manifest_log.json`, `manifest_fix_log.json`, `hits.tsv`, `paths.tsv`)
  directly support.
- Files outside the 98 backup targets have no before/after evidence in the
  pass logs; they are listed under "Unverified scope" below, not claimed as
  unchanged.

## Summary

| Category | Files |
|---|---|
| Document neutralization (docs) | 6 |
| Code path re-binding (absolute path → package-internal) | 40 |
| Manifest regeneration | 9 |
| File removed | 1 |
| **Total changed** | **56** |
| Backup targets verified byte-identical (no change) | 42 |

No scientific data file appears in the changed set. Every content change is in
documentation, code path strings, or manifests, plus the one removal below.

## 1. Document neutralization — 6 files

Wording that described agent/chat handoff processes was rewritten as neutral
technical description; internal absolute paths appearing in prose were removed.

- `PAPER_4/ENTRYPOINT.md` — neutralization only (handoff/agent wording).
- `PAPER_8/ENTRYPOINT.md` — neutralization only (handoff/agent wording).
- `PAPER_5/ENTRYPOINT.md` — mixed: handoff/agent wording (2 lines removed) and
  one internal absolute path (1 line removed).
- `PAPER_7/ENTRYPOINT.md` — mixed: internal absolute paths (4 lines removed)
  and handoff/agent wording (1 line removed).
- `PAPER_8/CANDIDATES_AND_BOUNDARY.md` — mixed: handoff/agent wording
  (5 lines removed) and internal absolute paths (3 lines removed).
- `PAPER_3/KNOWN_GAPS.md` — one internal absolute path removed; no agent
  wording was present in the removed line.

## 2. Code path re-binding — 40 files (all in PAPER_8)

In each file, the only removed lines are lines containing absolute paths
(drive-letter paths); no agent/chat wording was present in any removed line.
Absolute references to the original production folders were re-bound to
package-internal resolution.

- `PAPER_8/GAP_ALIGNED_MEMORY_LOCALIZATION/` (4):
  `RUN_EVENTWISE_ASSOCIATION.py`, `RUN_GAP_MEMORY_AUDIT.py`,
  `RUN_NATIVE_GAP_DIRECTIONAL_TEST.py`, `RUN_ROW_DIRECTIONAL_TEST.py`
- `PAPER_8/MECHANISM_REPLICATION_R1/` (25):
  `build_replication.py`, `cumulative_flux_direction_audit.py`,
  `decompose_0320_components.py`, `decompose_surface_transient.py`,
  `extract_0320_surface.py`, `horizon_flux_timeseries_correlation.py`,
  `horizon_relaxation_qnm_timescale_audit.py`,
  `parent_horizon_asymmetry_audit.py`, `qnm_source_native_audit.py`,
  `s_term_binwise_profile.py`, `s_term_concentration_audit.py`,
  `s_term_event_heterogeneity_audit.py`, `s_term_hazard_decomposition.py`,
  `s_vs_landmark_timing_audit.py`, `scalar_waveform_relation_audit.py`,
  `surface_cross_correlation_audit.py`,
  `surface_waveform_cross_correlation.py`, `sxs10_horizon_flux_order_audit.py`,
  `sxs10_horizon_scalar_transient.py`, `sxs10_qnm_frequency_extension.py`,
  `sxs10_radiative_history_audit.py`, `sxs10_radiative_timing_audit.py`,
  `temporal_order_audit.py`, `waveform_qnm_frequency_audit.py`,
  `weyl_e_b_coupling_audit.py`
- `PAPER_8/R13_SXS_NATIVE_MAP_RELAXATION/` (1): `run_r13.py`
- `PAPER_8/R14_EXTENDED_W0_W5_JOIN/` (1): `join_row_score_interval.py`
- `PAPER_8/R15_EXTENDED_W0_W5_CONDITIONAL/` (1): `build_conditional.py`
- `PAPER_8/R8_PHYSICAL_MECHANISM_CLOSURE/` (8):
  `R8_ACQUIRE_SECONDARY_COHORT.py`, `R8_ACQUIRE_SXS10.py`,
  `R8_FINALIZE_ACTIVE_AUDIT.py`, `R8_MECHANISM_CLOSURE_TEST.py`,
  `R8_MECHANISM_COMPLETION_AUDIT.py`, `R8_RUN_SECONDARY_MECHANISM.py`,
  `R8_SECONDARY_SOURCE_NATIVE_EXTRACTION.py`,
  `R8_SOURCE_NATIVE_MECHANISM_AUDIT.py`

A follow-up fix pass (`edit3_log.json`) recorded **0 replacements**; no further
code change came from it.

## 3. Manifest regeneration — 9 files

Each manifest below was regenerated after the content edits in its tree
(verified changed by backup comparison):

- `PAPER_3/SHA256_MANIFEST.txt`
- `PAPER_4/SHA256_MANIFEST.txt`
- `PAPER_5/SHA256_MANIFEST.txt`
- `PAPER_7/SHA256_MANIFEST.txt`
- `PAPER_8/SHA256_MANIFEST.txt`
- `PAPER_8/GAP_ALIGNED_MEMORY_LOCALIZATION/SHA256_MANIFEST.txt`
- `PAPER_8/MECHANISM_REPLICATION_R1/SHA256_MANIFEST.txt`
- `PAPER_8/R13_SXS_NATIVE_MAP_RELAXATION/SHA256_MANIFEST.txt`
- `PAPER_8/R8_PHYSICAL_MECHANISM_CLOSURE/SHA256_MANIFEST.txt`

A separate manifest fix log (`manifest_fix_log.json`) records 3 PAPER_8
manifests normalized with **0 entries changed** (missing-entry lines kept);
one of them (`R8_SECONDARY_INTERIM_SHA256_MANIFEST.txt`) was not in the backup
target set, so that normalization is log-backed only and is not counted above.

## 4. File removed — 1 file

- `crosscheck.tsv` (SEND root) — the build-phase crosscheck table was removed
  from the SEND root during this pass. SEND file count went from 7,132 to
  7,131. A copy remains in the working records outside SEND.

## 5. Detected during the pass, NOT changed by it

These are recorded detections, not edits:

- `manifest_log.json`: 7,530 manifest entries checked; **17 missing-entry
  detections** across sub-manifests in PAPER_6/7/8 (10 of them `SEND_TO_CHAT.txt`
  lines). These are pre-existing gaps from the build phase's exclusions,
  detected and logged during this pass; the pass did not create or repair them.
- `edit3_log.json` sweep: 2 PAPER_8 code files still contain the original
  production folder name as a string —
  `PAPER_8/R8_PHYSICAL_MECHANISM_CLOSURE/BUILD_R8_AUDIT.py` (file itself
  byte-identical after the pass) and
  `PAPER_8/R8_PHYSICAL_MECHANISM_CLOSURE/R8_FINALIZE_ACTIVE_AUDIT.py`
  (path-re-bound, but the folder-name string remains). Left as recorded
  residuals.
- `scan_summary.json`: 1 binary token hit — the string "Muse" inside
  `PAPER_3/FINAL_REPRO_PACKAGE/vendor/RIUD_R27_MORPHOLOGY_UNIVERSAL_DYNAMICS_LAW_SEARCH_R0_20260802/work/R27B_R3_CONFIRMATORY_1000/full/events/GW240920_124024/raw_checkpoints/control_0993.npz`.
  No log records any treatment of this binary file; it is an unclassified
  residual.

## 6. Unverified scope

- The pre-pass scan (`scan_summary.json`, `hits.tsv`, `paths.tsv`) covered
  5,253 text files and recorded hit lines in 2,320 files (groups include
  absolute paths, user-directory paths, and agent-related tokens). The edits
  verified above cover only the 98 backup targets. Whether any file outside
  the backup targets was altered cannot be established from the surviving
  logs and is **not claimed** either way.
- This file itself (`EDITION_CHANGES.md`) is an addition made after the pass
  to close the record; it is not part of any paper manifest (manifests are
  per-paper, under each `PAPER_n` folder).


## Executability repair pass (2026-10-29, after the trace/dependency pass)

Scope: `E:\SEND` only. Trigger: the isolation test recorded failures for the
Paper I/II companion verifier, the Paper I/II numbers verifier, and the
Paper III package verifier. This section records only what this pass changed.

### Companion cross-reference re-binding - 3 files per paper package

- `PAPER_1/COMPANION_ROOT/CLAIM_EVIDENCE_MATRIX.csv` and
  `PAPER_2/COMPANION_ROOT/CLAIM_EVIDENCE_MATRIX.csv`: the claim-evidence paths
  were written for the original four-paper archive layout (`PAPER_I/...`,
  `PAPER_II/...`, `PAPER_III/...`, `PAPER_IV/...`, resolved relative to the
  companion root). 68 of the 112 reference slots in each copy were re-bound to
  the SEND layout (own package root as `../`, sibling packages as
  `../../PAPER_n/...`, Paper III evidence under
  `../../PAPER_3/CLAIM_EVIDENCE/...`, and two Paper IV primary sources that
  were located by recorded hash in Paper 5's R40 folder, as
  `../../PAPER_5/REPRODUCTION_PACKAGE/R40/...`). A slot was rewritten only
  after the target file's SHA-256 matched the hash recorded in the matrix;
  the hash columns are unchanged.
- `PAPER_1/COMPANION_ROOT/PACKAGE_MANIFEST.csv` and the Paper 2 copy: the
  `CLAIM_EVIDENCE_MATRIX.csv` row's size and SHA-256 were updated to the
  re-bound matrix file.
- `PAPER_1/SHA256_MANIFEST.txt` and `PAPER_2/SHA256_MANIFEST.txt`:
  regenerated (2 entries changed in each) for the two files above.

### Not changed - references left exactly as recorded

44 slots (12 distinct files) point to files that are not in `E:\SEND`, so
their paths were left as recorded: `PAPER_I/VERIFIERS/SHA_VERIFY_FULL.log`
(a hash-identical copy exists in the archive at `PAPER_1/VERIFIERS/`) and
eleven files of the Paper IV `FROZEN_REPRO_PACKAGE`, which exist in neither
SEND nor the archive under their recorded names (a same-name
`VERIFY_PACKAGE.py` in the archive is a different file by hash). Including
any of them is a selection decision, not made here.

The Paper I/II numbers verifier (`verify_numbers.py`) and the Paper III
package verifier (`verify_final_package.py`) were not modified: the inputs
they require (the numerical-release tree `00_MANUSCRIPT` /
`01_NUMERICAL_RESULTS` / `02_FROZEN_CONTRACTS` / `03_PROVENANCE`, and the
`package_path_guard` module) are absent from SEND, so no path re-binding
inside SEND can make them run.

## Recovery inclusion - 2026-10-30

Files that the claim-based crosscheck had identified as missing from SEND
were located in the 5 TB mirror (and, for one log, in the archive) with
SHA-256 identical to the recorded values, and were copied into SEND.
Sources were only read, never modified. Placement logs:
`incl_part1_log.json` and `incl_part2_log.json` in the audit working folder.

- Paper IV `FROZEN_REPRO_PACKAGE` - 11 files placed under
  `PAPER_4/FROZEN_REPRO_PACKAGE/`:
  `01_HANDOFF_BOUNDARY/00_DESIGN_LOCK/FINAL_DEVELOPMENT_TECHNICAL_CENSUS_FREEZE.json`;
  `02_PATH99/01_FREEZE/PATH99_CANONICAL_RESULT_FROZEN.jsonl`;
  `03_DYNAMICS_R5_R10/R9/MEMORY_FLOW_CONTINUOUS_PROFILE.csv`;
  `04_AUTONOMOUS_LAW_R14_R29/RIUD_DEV99_PHYSICS_FREE_AUTONOMOUS_THREE_PHASE_LAW_AUDIT_R29_20260815/R29_MINIMAL_CORE_AUDIT.json`;
  `05_PHYSICAL_CORRESPONDENCE_R30_R38/RIUD_DEV99_KERR_BALANCE_SPIN_ORDINAL_FREEZE_R37_20260815/R37_K1_K6_RANK_AUDIT.csv`;
  `06_PHYSICAL_CLOCK_R39_R41/R39_R40_R41_SOURCE_AUDIT.tsv`;
  `07_FOUR_MAP_AUDIT/RIUD_DEV99_PHYSICAL_CLOCK_4MAP_BIC_AUDIT_R1_20260816/R40_4MAP_BIC_SEMANTICS_AUDIT.txt`;
  `11_GAP_BRANCH/GAP_LOCATION/GAP_NULL99_LOCATION_SUMMARY.txt`;
  `11_GAP_BRANCH/GAP_STRENGTH/GAP_NULL99_SUMMARY.txt`;
  `12_REPRODUCIBILITY/MANIFEST_SHA256.tsv`;
  `12_REPRODUCIBILITY/VERIFY_PACKAGE.py`.
  Three of these are stored in the mirror under different file names
  (`R_STATUS.json` for the census freeze; `SEND_TO_CHAT.txt` for the two
  GAP summaries); the content is byte-identical to the recorded hashes.
- `PAPER_1/VERIFIERS/SHA_VERIFY_FULL.log` - copied from the archive copy.
- `CLAIM_EVIDENCE_MATRIX.csv` (both companion copies): the remaining
  reference slots (12 distinct files, 88 slot references across the two
  copies) were re-bound to the SEND layout under the same rule as before
  (a path is rewritten only after the target file's SHA-256 matches the
  matrix); the `PACKAGE_MANIFEST.csv` rows were updated. A full slot probe
  now reports 0 missing slots.
- Numbers release (Papers I-II shared layer): the complete
  `RIUD_PAPERS_I_IV_NUMERICAL_RELEASE_R1_20260818.zip` (SHA-256
  `51d5724fa22dba246638f78af292828d830ce99945c597bcdd5316e8a863a03c`,
  109 files) was unpacked into both
  `SHARED_NUMERICAL_RELEASE_PAPER_I_II/RELEASE_ROOT` folders
  (`00_MANUSCRIPT`, `01_NUMERICAL_RESULTS`, `02_FROZEN_CONTRACTS`,
  `03_PROVENANCE`, `PACKAGE_SCOPE.txt`, `README.md`, `SHA256SUMS.txt`,
  `verify_numbers.py`). All 102 `ORIGIN_SHA256.tsv` rows verify against
  the unpacked files, and `verify_numbers.py` passes in place for both
  papers (CHECKS=133, FAILED=NONE).
- `PAPER_3/CLAIM_EVIDENCE/VERIFIERS/work/package_path_guard.py` - placed
  where `verify_final_package.py` imports it from (SHA-256
  `0314d50621b5b2485945b434c4c9b174f5aa2e70f3e0bd40f5b71a14d91ac675`).
- Paper VII detector-closure files, placed under `PAPER_7/`:
  `RIUD_R6F12_COHERENCE_EXACT_REPLAY_R1_20260906/FINE_TIME_RAW_FEATURES.csv`
  (8,928 data rows; SHA-256 matches the frozen manifest and the R6F19
  contract);
  `RIUD_R26C30R5B_DETECTOR_RESOLVED_MAP_REGEN_AND_COHERENCE_20260729/output/R_STATUS.json`
  and `R26C30R5B_EVENT_DETECTOR_COHERENCE.csv` (map-regeneration audit
  13/13, coherence failures 0);
  `r26c30r6/output/R26C30R6_EVENT_PATH_DETECTOR_COHERENCE_FDR.csv` and
  `R26C30R6_EVENT_PATH_DETECTOR_COHERENCE.csv`.
- Top-level `SHA256_MANIFEST.txt` regenerated for Papers 1, 2, 3, 4 and 7.
  The eight-paper manifest verification reports 0 mismatch / 0 missing /
  0 extra for every paper. SEND now holds 7,362 files.

## Paper III verifier path closure - 2026-10-30

- `PAPER_3/CLAIM_EVIDENCE/VERIFIERS/verify_final_package.py` (the SEND copy
  only): the script read its independent-replication branch from
  `PACKAGE_ROOT / "03_INDEPENDENT_REPLICATION_R1"`, the branch folder name of
  the original package layout, which does not exist in SEND. The data itself
  is present in SEND at `PAPER_3/CLAIM_EVIDENCE/INDEPENDENT_REPLICATION`
  (`R_STATUS.json`, `PAPERIII_RESULTS.csv`, `PAPERIII_DRAW_TABLE.csv`), so the
  one branch line was re-bound to
  `PACKAGE_ROOT.parent / "INDEPENDENT_REPLICATION"` - the same sibling-folder
  relationship, in SEND layout terms. No folder was duplicated. SHA-256
  `c8b814f6832eaca11c22531babd02c10da02c349b136d38ddafc6b668c33835b` ->
  `a92cd1ca7363361025db13b4ff4ee4a1c95450e6875f00e7e3b2213115ff0a6f`;
  the `PAPER_3/SHA256_MANIFEST.txt` entry for this file was updated to match.
  The original script in the mirror/archive is untouched.
- Not changed: `work/package_path_guard.py` - its
  `03_INDEPENDENT_REPLICATION_R1` entries are informational runtime targets
  that tolerate absence, and the guard already returned PASS. Frozen records
  quoting the original branch name (`CLAIM_EVIDENCE/MANIFESTS/
  E_CRITICAL_SHA256SUMS.txt`, `E_PACKAGE_DIRECTORY_INVENTORY.csv`, the
  `CANONICAL` comparison design lock, `VERIFIERS/R_STATUS.json`) were left
  exactly as recorded: they are provenance of the original package layout,
  not runtime paths.
- Verification, in a fresh isolation copy of SEND (7,362 files copied,
  counts equal): before the fix the verifier exited 1 with
  guard_status=PASS, branch_status_exists=false, raw_rows=-1, draw_rows=-1,
  status=FAIL. After the fix it exits 0 with status=PASS:
  independent_replication_status=PASS, raw_rows=3, draw_rows=1000,
  final_verdict=VALIDATED_PARTIALLY_SHARED_DYNAMICS.
- Regression in the same isolation copy: Paper IV holdout5 replay exit 0,
  R_STATUS=PASS, likelihood CSV SHA-256
  `a983011abdf1c2fe0dc382b3720b986d9fe4da3eba92de58e80ecbe1634830a6`
  (identical to the SEND copy, as in previous runs); Paper VII stage 1 and
  stage 2 exit 0 with the same output profile as the previous isolation run
  (data files identical; the generated `ERRORS.csv` is extra and the
  generated folder's own `SHA256_MANIFEST.txt` differs, as before); Paper V
  `VERIFY_PAPER5_FREEZE` = PASS. Final eight-paper manifest verification
  after this change: 0 mismatch / 0 missing / 0 extra for every paper.


## Paper VII closure layer (2026-10-30)

Final closure pass for the Paper VII detector-closure layers named in the
manuscript section 7 release list. Additions were copied from the read-only
Drive mirror; the mirror and `E:\ARCHIVE` were not modified.

### 1. Directionality audit (manuscript sections 3.3-3.4) - ADDED

- Added `PAPER_7\EXT_DETECTOR_REPRESENTATION_AUDIT_R1\` - 18 files, copied
  from the mirror copy at `RIUD_ACTIVE_20260808\UNCLASSIFIED_REVIEW\
  EXTERNAL_VALIDATION\EXT_DETECTOR_REPRESENTATION_AUDIT_R1`. Every file
  SHA-256-verified against the mirror source: 0 mismatches.
- Contents check: 96 events, 57,696 directional rows (window -300..300 ms,
  width 10 ms); final null 9,999 draws, exceedances 0, empirical p
  (plus-one) 0.0001, status PASS; directional medians H1_TO_L1
  -0.20440297970384336 and L1_TO_H1 +0.6496645696751138, matching the
  manuscript. Key file hashes (prefixes; full hashes in the regenerated
  PAPER_7 manifest): `04_DIRECTIONAL_RESULTS.csv` E65D5EC3B6DF,
  `05_NULL_FINAL9999.csv` 4A439AAF99CD,
  `SUMMARY_FINAL9999_L1_TO_H1.json` 5B5D54A6CF3D, `run_audit.py`
  1B24F65A367E.

### 2. Width diagnostic, 10-80 ms (manuscript sections 3.5, 4.3) - ADDED, one sub-item open

- Added `PAPER_7\WINDOW_10_80_EXTENDED_DIAGNOSTIC\` - 38 files, copied from
  the mirror copy at `PAPER_6\MIsCORE_MT_RAW_FROM_SOURCE_R2_20260829\
  RAW_FRONTEND\WINDOW_10_80_EXTENDED_DIAGNOSTIC`. Every file SHA-256-verified
  against the mirror source: 0 mismatches (3 files whose mirror paths exceed
  the Windows path limit were copied and verified via long-path calls).
  Features table `FINE_TIME_RAW_FEATURES_10_80_EXTENDED.csv` SHA-256
  9AC2BF7B1BF256ECBBB4CE38ED56E3207B64983EEA2DFC91EAF376759E914684
  (2,976 rows = 96 events x 31 offsets, -15..+15 ms).
- Added `PAPER_7\WINDOW_10_80_PRODUCERS\` - the 6 original producer and
  analysis scripts from the Codex 2026-08-29 goal folder (hash-verified),
  plus `verify_width_series.py`, the verification script written for this
  pass (2026-10-30, new file, not an original).
- Verification: the manuscript's T0 baseline series reproduces exactly from
  the included features table at all five printed widths - computed
  +0.3932 / -0.0812 / -0.5265 / -0.7485 / -0.8511 vs printed +0.393 / -0.081 /
  -0.527 / -0.749 / -0.851 (median log10 L1/H1, 250-512 Hz band, offsets 0).
  This confirms the included layer is the section 4.3 source data.
- NOT located: the manuscript's NODE-conditioned series (+0.4373 at 10 ms to
  -0.7916 at 80 ms) as a standalone result file, and the exact 273-row
  conditioning set behind it. Conditioning on the frozen GAP
  LEFT/CENTER/RIGHT rows (285 rows in this 96-event cohort) does NOT
  reproduce the printed values (computed +0.4014 / -0.0978 / -0.5698 /
  -0.7824 / -0.8229). The printed NODE-conditioned series therefore remains
  supported by the manuscript text; the features needed to recompute it,
  once the conditioning set is identified, are now included above.

### 3. Threshold-robustness lineage (manuscript sections 3.7, 4.5) - NOT included, NOT recomputed

- The lineage does not exist as a file (deep-search conclusion, reconfirmed
  in this pass). A recompute from surviving records is not possible; the
  missing basis is: (i) no per-NODE ROBUST_NETWORK_Z table survives - the
  global NODE atlas run's OUTPUT folder holds maps and one continuity audit
  only; (ii) the frozen PATH's NODE membership was not located; (iii) no
  recorded definition of PATH persistence under the sweep was located.
  Section 4.5 prints no numbers, so no printed target exists to validate a
  reconstruction against. No sweep table was fabricated.

### 4. Manifest

- `PAPER_7\SHA256_MANIFEST.txt` regenerated over the final PAPER_7 folder
  (all files except the manifest itself).

## Final rulings on the two open Paper VII items (2026-10-30, published-text verification)

Both items were re-checked against the published final text (Zenodo
combined record and the Paper VII record). The rulings below supersede the
framing in items 2 and 3 of the Paper VII closure layer section above.

### 1. Width diagnostic, NODE-conditioned series - published result; reproduction material lost

- Final ruling: the NODE-conditioned series (+0.4373 at 10 ms to -0.7916
  at 80 ms) IS a result printed in the published paper. What is lost is
  only the reproduction material - the record of the exact 273-row
  conditioning set behind the printed values. The gap recorded in item 2
  above is a lost selection record, not an unpublished or unsupported
  number.

### 2. Threshold-robustness sweep - narrative only in the paper; no data products exist

- Final ruling: the sweep exists in the published paper only as
  narrative, without numbers (the section 3.7 statement; section 4.5
  prints no values), and no data products of the sweep exist anywhere
  searched. It is therefore not a missing numeric result and not a
  recompute target: there is no printed number to reproduce. The
  robustness files located during the searches belong to the earlier
  PRISM-stage work, a different lineage from this sweep. The
  "missing basis" framing in item 3 above is superseded by this ruling.
