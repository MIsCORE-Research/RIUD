# Scientific Analysis and Verification Interface

This directory provides a unified, 1-click execution and verification interface for evaluating the numerical claims, replication suites, and observational analyses across Papers I through VIII.

## Scripts Overview

| Paper | Python Target | Windows 1-Click | Linux / macOS / WSL | Description |
|---|---|---|---|---|
| Paper I | `verify_paper1.py` | `run_paper1.bat` | `run_paper1.sh` | Numerical companion release checks (133 tests) |
| Paper II | `verify_paper2.py` | `run_paper2.bat` | `run_paper2.sh` | SXS numerical companion checks (133 tests) |
| Paper III | `verify_paper3.py` | `run_paper3.bat` | `run_paper3.sh` | Independent replication suite (R27 tree) |
| Paper IV | `reproduce_paper4.py` | `run_paper4.bat` | `run_paper4.sh` | R40 Holdout-5 forward likelihood benchmark |
| Paper V | `verify_paper5.py` | `run_paper5.bat` | `run_paper5.sh` | Authoritative numerical freeze check (128 files) |
| Paper VI | `verify_paper6.py` | `run_paper6.bat` | `run_paper6.sh` | Frequency timing geometry and census check |
| Paper VII | `run_paper7.py` | `run_paper7.bat` | `run_paper7.sh` | Eventwise observation layer and C01 operator |
| Paper VIII | `verify_paper8.py` | `run_paper8.bat` | `run_paper8.sh` | Mechanism evidence and ETK benchmark closure |
| Master | `run_all_verifications.py` | `run_all.bat` | `run_all.sh` | Orchestrates sequential verification across all 8 papers |

## Quick Usage

Run all 8 papers in sequence:
- Windows (CMD/PowerShell/Explorer): `src\run_all.bat` (or root `run_all_papers.bat`)
- Linux / macOS / WSL: `bash src/run_all.sh` (or root `bash run_all_papers.sh`)
- Python: `python src/run_all_verifications.py`

Run an individual paper:
- Windows: `src\run_paper1.bat`
- Linux / macOS / WSL: `bash src/run_paper1.sh`
- Python: `python src/verify_paper1.py`
