# RIUD Full Independent Reproduction Package

This package expands the existing integrated authority bundle into an independent reproduction package for a new Ubuntu/WSL reviewer environment.

Scope:
- preserve and verify existing Paper I and Paper II authority outputs
- separate the historically distinct environments into `ENV_A` and `ENV_B`
- fetch public raw data without embedding the 927 local HDF5 files in the ZIP
- run smoke-only checks now
- provide end-to-end wrappers for `QUICK_REPRO` and `FULL_CLEAN_REPRO`

This package does not modify any existing PRISM source tree outputs. Original authority directories and ZIPs remain untouched.

Key boundaries:
- no new authority science is created here
- no existing authority file is overwritten
- exact original versions are only claimed when directly supported by histories, exports, logs, or recorded interpreter paths
- unresolved original-run environment facts are marked `UNKNOWN_AT_ORIGINAL_RUN`

Entry points:
- `07_RUNNERS/RUN_QUICK_REPRO.sh`
- `07_RUNNERS/RUN_FULL_CLEAN_REPRO.sh`
- `09_COMPARISON_AND_VERIFY/VERIFY_PACKAGE.py`

