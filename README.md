# MIsCORE-RIUD

## Overview

This repository provides numerical pipelines, frozen execution engines, replication suites, and observational data bindings for the MIsCORE-RIUD gravitational wave memory and ringdown dynamics analysis series (Papers I through VIII). All physical equations, coordinates, and statistical models are frozen and verified against authoritative SHA-256 manifests.

## Quick Reproduction

```bash
python fast_track_r40/reproduce_r40.py
```
Evaluates the frozen R40 forward likelihood engine across the five holdout events (GW241114_024711, GW240830_211120, GW240612_081540, GW241130_110422, GW250119_190238) across windows W1–W4 in under 10 seconds.

To verify all 8 papers in sequence:
- Windows: `run_all_papers.bat`
- Linux / macOS / WSL: `bash run_all_papers.sh`
- Python: `python src/run_all_verifications.py`

## Repository Layout

- `fast_track_r40/`: Standalone 1-click reproduction runner and verification guide for the R40 physical law benchmark.
- `papers/`: Mapping table, manuscript documents, figure indices, and data source links for Papers I–VIII.
- `src/`: Unified Python verification runners for individual papers (`verify_paper1.py` .. `verify_paper8.py`) and master suite (`run_all_verifications.py`).
- `SEND/`: Authoritative frozen packages for Papers I through VIII, including input datasets, reference outputs, and SHA-256 manifests.
- `archive/`: Master archive holding historical exploratory runs, intermediate calculation logs, and legacy packages.
- `ENVIRONMENT.md`: Specification of computational environment, Python dependencies, and platform compatibility.
- `requirements.txt`: Minimal pinned Python dependencies (numpy, scipy, pandas, h5py).

## Paper I–VIII Index

| Paper | Title / Subject | Code & Data Path | Primary Verification Command |
|---|---|---|---|
| Paper I | PRISM: Frequency Ridge Locked Validation & Catalog Morphology Controls | `SEND/PAPER_1/` | `python src/verify_paper1.py` |
| Paper II | RIUD: Numerical Relativity SXS Mirror & R26 Permutation Null Companion | `SEND/PAPER_2/` | `python src/verify_paper2.py` |
| Paper III | Independent Replication Suite & R27 Corroboration Tree | `SEND/PAPER_3/` | `python src/verify_paper3.py` |
| Paper IV | Frozen Engine Holdout-5 Exact Replay & Likelihood Benchmark (R40) | `SEND/PAPER_4/` | `python fast_track_r40/reproduce_r40.py` |
| Paper V | Authoritative Numerical Replay Freeze & SXS Native Replay | `SEND/PAPER_5/` | `python src/verify_paper5.py` |
| Paper VI | Frequency Timing Geometry & Landmark Frequency Freeze | `SEND/PAPER_6/` | `python src/verify_paper6.py` |
| Paper VII | Eventwise Observation Layer, C01 Operator & 99 GWOSC Events | `SEND/PAPER_7/` | `python src/run_paper7.py --mode verify` |
| Paper VIII | Physical Mechanism Closure, GR Memory & ETK Benchmark | `SEND/PAPER_8/` | `python src/verify_paper8.py` |
| Integrated | PRISM / RIUD Integrated Paper I & II Canonical Volume | `SEND/PAPER_1/`, `SEND/PAPER_2/` | `python src/verify_paper1.py` |

## Data & Provenance

- Gravitational Wave Open Science Center (GWOSC): 4-second calibrated strain timeseries (4096 Hz, H1 and L1 detectors) across 99 binary black hole merger events analyzed in Paper VII (`SEND/PAPER_7/STRAIN/`).
- Simulating eXtreme Spacetimes (SXS): Numerical relativity waveforms and apparent horizon flux data benchmarked in Papers V and VIII (`SEND/PAPER_5/SXS/`, `SEND/PAPER_8/MECHANISM_REPLICATION_R1/`, `SEND/PAPER_8/R13_SXS_NATIVE_MAP_RELAXATION/`).
- Integrity Verification: Every package in `SEND/PAPER_1` through `SEND/PAPER_8` contains an authoritative `SHA256_MANIFEST.txt` recording full SHA-256 digests for all files. All 7,416 files match with zero mismatches.
