# PRISM Internal Full Validation Suite V1

- Started/finished around: 2026-07-07T19:10:53+09:00
- PRISM_ROOT: /mnt/c/Users/민재현/Desktop/prism
- OUTDIR: /mnt/c/Users/민재현/Desktop/prism/PRISM_INTERNAL_FULL_VALIDATION_SUITE_V1_20260707_190939
- PASS: 22
- WARN: 0
- SKIP: 0
- FAIL: 0

## Verdict
PASS/REVIEW: internal full validation suite completed with FAIL=0.

## Meaning

This suite checks package integrity, CLEAN_V4 first-pass validity, EXP17D SHA attachment, PRISM 2.3 frozen-input byte-identical reproduction, PRISM 2.2 locked CSV byte-identical regeneration under original hardcoded HOME path, raw GWOSC smoke access, and self-contained validator kit execution.

## Boundary

This suite does not prove confirmed detection, new physics established, GR falsification, or full raw end-to-end discovery reproduction. It validates the locked internal evidence/reproduction package.

## Key expected anchors

- CLEAN_V4 ZIP integrity OK.
- EXP17D SHA expected: `a1170665a22db0d1ea14034c354b244fdc4a3ab2bfed6320552426cc1db1576f`.
- Full repro V2 expected: PASS=15, WARN=5, SKIP=0, FAIL=0.
- PRISM 2.3 expected: byte-identical=7, different=0.
- PRISM 2.2 expected: HOME CSV byte-identical to locked CSV.
- Raw GWOSC smoke expected: import/event lookup passed.
