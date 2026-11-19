# Paper IV — Holdout5 Exact Replay (public edition package)

Assembled 2026-10-27 (3차). All editing was done on this copy only; the original E: archive and the Drive mirror were used read-only.

## Contents

- `run_holdout5_repro.py` — entry point (no CLI arguments). Loads the frozen engine by importlib and calls its `main()`.
- `FROZEN_ENGINE\` — frozen engine `run_holdout5_r40_exact_replay.py` (SHA-256 `332ae701e2e4c5896d4cf873cb27ef59d496d7d06aec18ad5cc53323c14f6d29`), sibling `run_r39.py` (required import), R6/R8/R9 code (hash-bound only), R40 law/contract/physical-coordinate/support files, bins matrix, memory-conditioned rates.
- `INPUTS\` — `HOLDOUT5_R40_PHYSICAL_BINDING.csv` (SHA-256 prefix `5816ab61`) and per-event `EXPANDED_A2_POSITION_FREE_PATH.csv` (5 events). The binding CSV replaces the engine's heavy default input path (PE posterior HDF5 + HOLDOUT10 event index).
- `CANONICAL_REFERENCE\` — the frozen reference outputs (coverage CSVs, provenance, exact likelihood, README).
- `OUTPUT\` — the **original** outputs of the canonical replay run (from the original replay run folder `RIUD_DEV99_HOLDOUT5_R6_R8_R9_R40_EXACT_REPLAY_R0_20260817`), kept as the expected-value set.
- `SHA256_MANIFEST.txt` — SHA-256 of every file in this package (generated at assembly).
- `SHA256_MANIFEST_SOURCE_OUTPUTS_DRAFT.txt` — the 2026-10-27 draft manifest over the original replay folder's 8 output files (see Exclusions).

## How to run

```
python run_holdout5_repro.py
```
Python 3.12 with pandas, numpy, scipy, h5py. Outputs are written to `OUTPUT\` (R_STATUS line in the provenance JSON).

## Verification evidence (2026-10-27)

- Provenance binding: all **13** `SOURCE_SHA256` entries of `CANONICAL_REFERENCE\HOLDOUT5_R40_REPLAY_PROVENANCE.json` are present in this package by hash (BINS, COVERAGE_REPLAY, NODES, R39_EXACT_ENGINE, R40_ENGINE, R40_LAW, R40_PHYS, R40_SUPPORT, R6_CODE, R8_CODE, R9_CODE, R9_RATES, WINDOWS).
- Expected outputs: 7/7 non-excluded original output files match the draft manifest byte-for-byte, including the exact-likelihood CSV SHA-256 `a983011abdf1c2fe0dc382b3720b986d9fe4da3eba92de58e80ecbe1634830a6` — the same hash cited by the Paper V characterization provenance.
- Clean-room rerun (2차, 2026-10-27): exit 0, R_STATUS=PASS; Δloglik reproduced at full precision — W1 1.1043334444486137 / W2 0.2230157036802467 / W3 1.0415943943363075 / W4 0.1348864350934437; direction True·True·True·False. Likelihood, transition-history, state-age-history and active-fraction files byte-identical. Two value-neutral differences in a rerun: the generated-trajectories CSV differs only in ≤2.2×10⁻¹⁶ (1-ulp) text representation of a few G/TOTAL cells, and the rerun provenance's MAP_SOURCE string points at the rerun location.
- Variant screen: a same-named PUBLIC_R9 set exists (`PAPER_4\RIUD_FAST_TRACK_PUBLIC_R9_20260817`) with different hashes (engine `4a635a74…`). It is **not** used here; the engine in this package is the canonical `332ae701…`.

## Exclusions (trace removal, copy only)

- Two handoff-note files in the source folders (one in `CANONICAL_REFERENCE\`, one among the original outputs) — working notes, excluded from this public copy. Their line remains visible in `SHA256_MANIFEST_SOURCE_OUTPUTS_DRAFT.txt` for the record (hash `aa697f6e…`).
- `__pycache__` from the rerun assembly — build artifact, excluded.

## Frozen constants (engine)

beta2 −0.304588116941319, beta3 −0.0167449766916816, beta4 0.3713520014548632, gamma2 0.1425553247852259, gamma3 −0.3177555096604296, gamma (frozen clock) 0.3162354634393393.
