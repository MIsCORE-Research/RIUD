# Paper VII — Eventwise Observation Layer (public edition package)

Assembled 2026-10-27 (3차). All path repairs were made **in this copy only**; the original scripts and run folders were used read-only.

## Contents and layout

The package root plays the role of the original archive root:

- `run_eventwise_full_tf_change_separate.py` — stage 1 (the C01 canonical operator; original SHA-256 `26B9F63F55D39C715E6DE907F7759A04C9C7427F7F039FDA9507A4AFBF76EF45`).
- `run_eventwise_c_slope_changepoint.py` — stage 2 (original SHA-256 `b343e6538529…`).
- `MIsCORE_FULL99_RAW_SOURCE_BINDING_AUDIT_R0_20260828\FULL99_RAW_SOURCE_BINDING.csv` — rebound binding table (see Repairs); `FULL99_RAW_SOURCE_BINDING_ORIGINAL.csv` is the untouched original.
- `STRAIN\<event>\` — the 198 GWOSC 4-second strain slices (99 events × H1/L1), each SHA-256-verified against the binding table's recorded H1_SHA256/L1_SHA256.
- `RIUD_GAP_RAW_POSITION_FULL_CORRECTED_TIME_AUDIT_R2_20260821\GAP_RAW_POSITION_FULL_CORRECTED_TIME_EVENT_TABLE.csv` — corrected GAP table, SHA-256 `d5a348252d9e30295329bd2df3f55d4e526aa6ba3ee6f8592d4a8670825ca619`.
- `EXPECTED_OUTPUTS\` — the original outputs of both stages (the comparison set, including each stage's own SHA256_MANIFEST.txt).
- `SHA256_MANIFEST.txt` — SHA-256 of every file in this package.

## How to run

```
python run_eventwise_full_tf_change_separate.py
python run_eventwise_c_slope_changepoint.py
```
No arguments. Python 3.12 with numpy, scipy, h5py. Stage 1 writes `MIsCORE_RAW_EVENTWISE_FULL_TF_CHANGE_R1_20260828\` at the package root; stage 2 reads its `EVENTWISE_C_CURVES.csv` and writes `MIsCORE_RAW_EVENTWISE_C_SLOPE_CHANGEPOINT_R0_20260828\`. Selection reads no GAP/MT/t0/population statistics (frozen before the GAP join); HOLDOUT30 is not accessed.

## Repairs made in this copy (originals untouched)

1. Both scripts hardcoded `ROOT` to the original archive root while the input/output folders now live under `PAPER_7\`. In the copies, ROOT resolves to the script's own directory (`Path(__file__).resolve().parent`), restoring the original relative layout.
2. The binding table pointed at a backup tree that no longer exists at its recorded path. Each of the 198 slices was located among the surviving copies on E: and verified by SHA-256 against the binding table (198/198 matched; 33 files had multiple same-name candidates — the recorded hash decided). The copies live under `STRAIN\`, and the rebound binding table references them by package-relative path; stage 1's copy resolves relative strain paths against the package root.
3. GAP table: only one copy survives (under `PAPER_8\`); the `PAPER_5\` audit-bundle copy was removed by the duplicate cleanup with this survivor recorded as its canonical copy (deletion log, SHA-256 `d5a34825…`). That survivor is the one included here.

## Clean-room reproduction (2026-10-27, this package copied to a fresh folder)

- Stage 1: exit 0, 48.4 s. **All output files byte-identical** to `EXPECTED_OUTPUTS` (landmarks, curves, GAP timing evaluation, METHODS, SUMMARY). 99 events in, 594 event-detector rows, 0 errors, GAP join 576.
- Stage 2: exit 0, 1.1 s. All data files byte-identical (slope changepoints, curves, GAP evaluation, ERRORS, METHODS). `SUMMARY.json` differs in exactly one field, `INPUT_CURVE` — a path string naming the run location (value-neutral); all counts (104,940 curve rows, 594 groups, 0 errors, 576 evaluation rows) and every median/MAE statistic identical.
- Expected headline values: stage 1 median absolute timing error 41.4–54.4 ms (H1/L1 across 5/10/20 ms widths); stage 2, 42.2–49.3 ms.
- Note: the original stage-1 folder no longer contains `ERRORS.csv` (a header-only file, removed as an exact duplicate in the cleanup); a rerun regenerates it with 0 error rows, consistent with `N_ERRORS = 0` in the frozen SUMMARY.
