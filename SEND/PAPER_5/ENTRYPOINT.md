# Paper V — Authoritative Freeze R1 (public edition package)

Assembled 2026-10-27 (3차) from the surviving freeze folder plus hash-verified restoration of components that the 2026-10-27 duplicate cleanup had removed from the freeze folder. All editing was done on this copy only; originals were used read-only. Restoration sources are recorded per file in the build record (deletion log of 2026-10-27: each restored file's canonical surviving copy, matched by SHA-256).

## What this package is

A **frozen numerical replay / evidence package** — not a raw-to-final recomputation archive (per its own `REPRODUCTION_PACKAGE\REPRODUCTION_SCOPE.md`). Excluded by the freeze's own scope: the missing raw sources for PATH_FOUND 81 events, DEV99 NO_PATH 1 event, Holdout30.

## Verification entry point

```
powershell -File REPRODUCTION_PACKAGE\VERIFY_PAPER5_FREEZE.ps1 -Package <this package root>
```
The script checks every line of `SHA256_MANIFEST.txt` (hash + existence); PASS prints `VERIFY_PAPER5_FREEZE=PASS` and exits 0.

**Result on this copy (2026-10-27): `VERIFY_PAPER5_FREEZE=PASS`, exit 0.**

## Assembly accounting (against the original 147-entry freeze manifest)

- Present in the freeze folder and copied: 29
- Restored from canonical surviving copies (SHA-256 matched): 97 (93 via copies deleted in the cleanup, 4 via already-gone entries)
- Excluded as working handoff notes: 21 (see below)
- Unrecovered: **0**

`SHA256_MANIFEST_ORIGINAL.txt` preserves the freeze's original 147-line manifest. The working `SHA256_MANIFEST.txt` in this copy is the same manifest minus the 21 excluded lines, so the freeze's own verifier passes on the public copy.

## Exclusions (trace removal, copy only)

21 handoff-note files (working artifacts): 17 under `RAW17\EVENTS\…\` (one per audited event) and 4 under `SXS\`. Their names and hashes remain listed in `SHA256_MANIFEST_ORIGINAL.txt`. All result records — including the boundary results (location p = 0.01 vs gap-strength p = 0.99; surrogate recovery 82.6449%; no stable replacement) — are retained.

## Production entry points (for reference; not re-run in this round)

- SXS native replay: `PRODUCTION_CODE\run_sxs_native_replay.py` (copy of the production run's `run_sxs_native_replay.py`, SHA-256 `d23b28af2887fc2dbbab66b4870bdc6d445a419f469cc277f0dbdc996c37e36f`; needs the `sxs` library). Its frozen outputs are in `SXS\`.
- R40 final 101-event characterization: results + provenance in `REPRODUCTION_PACKAGE\R40\`. The producing script itself is not present in the result folder (hash-bound inputs only) and remains unidentified — recorded as an open defect.
- RAW17 path-support audits: per-event folders under `RAW17\EVENTS\` (17 events).
