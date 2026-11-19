# RIUD Full Integrated Authority Repro Package

## Scope

This package is a frozen integration bundle assembled on 2026-08-01 from existing authoritative files already present under the PRISM root.

It includes:

- Paper I final manuscript and submission assets.
- Paper I 374-event B7B1 population authority.
- Paper I original A2 scorer runner used as methodology source.
- Paper I 927 event-detector external-data lock manifest with SHA256.
- Paper II manuscript package and final submission ZIP.
- Paper II fixed-path raw-strain authority from `R26C37`.
- Paper II selector-aware complex-phase authority from `R26C42G` and `R26C42H`.
- Integrated Paper I and Paper II package assets.
- Authority manifests, handoff records, and package-level verification assets.

It does not include:

- Any new scientific recomputation.
- Any rerun of PRISM, RIUD, calibration, selector, or phase-null jobs.
- Any duplicated copy of the 927 external Paper I HDF5 files.

## Boundary Rules

- `PRISM_2P5B7B1_EVENT_LEVEL_BEST_SUMMARY.csv` is the Paper I 374-event population authority.
- `B7B1_LOCKED_EVENT_DETECTOR_PATHS.csv` and `EXTERNAL_DATA_FILE_MANIFEST.csv` lock the 927 Paper I event-detector paths without bundling those HDF5 files.
- `PRISM_2P5A2_SELECTED29_4S_PRISM_SMOKE_RESULTS.csv` is not promoted here as final coherent scope authority. Its runner is included only as methodology source code.
- `PRISM_2P5B7C81C_FULL29_DQ_FINAL_LOCK_20260710` is preserved as a separate downstream FULL29 DQ branch and must not be described as a direct subset lock of SELECTED29.
- Paper II phase-null significance and Paper II raw fixed-path significance answer different null questions and are not combined.

## External Data

Paper I external data:

- Locked in `02_paper1_population_authority/EXTERNAL_DATA_FILE_MANIFEST.csv`
- Relative paths point into `_GWOSC_BULK_ANYDET_4S_4096HZ_380_20260705/01_hdf5_4s/...`
- Not copied into this package

Paper II raw fixed-path data:

- Included from the frozen `R26C37` evidence subtree
- Limited to the 13-event fixed-path authority used by the frozen Paper II evidence package

## Scientific Status

- Scientific recomputation performed: `False`
- Files moved or deleted from source tree: `False`
