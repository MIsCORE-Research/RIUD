# Papers Index and Manuscript Mapping

This directory provides the mapping, manuscript links, data sources, and reproduction entrypoints for the MIsCORE-RIUD series (Papers I through VIII) and the integrated volume.

## Paper Index Table

| Paper | Title / Subject | Manuscript Document | Primary Package Path | 1-Click Runner (Win / Linux) | Python Entrypoint |
|---|---|---|---|---|---|
| Paper I | PRISM: Frequency Ridge Locked Validation & Catalog Morphology Controls | [PRISM Manuscript PDF](file:///E:/SEND/PAPER_2/SHARED_FROZEN_AUTHORITY_PACKAGE/01_PAPERS/PRISM_MANUSCRIPT_R8R4_FINAL.pdf) | `SEND/PAPER_1/` | `src/run_paper1.bat` / `.sh` | `python src/verify_paper1.py` |
| Paper II | RIUD: Numerical Relativity SXS Mirror & R26 Permutation Null Companion | [Paper II Manuscript PDF](file:///E:/SEND/PAPER_2/NUMERICAL_SOURCES/paper2_manuscript_package/RIUD_PAPERII_MANUSCRIPT_DRAFT_R0.pdf) | `SEND/PAPER_2/` | `src/run_paper2.bat` / `.sh` | `python src/verify_paper2.py` |
| Paper III | Independent Replication Suite & R27 Corroboration Tree | [Paper I–III Canonical PDF](file:///E:/SEND/PAPER_1/SHARED_NUMERICAL_RELEASE_PAPER_I_II/RELEASE_ROOT/00_MANUSCRIPT/PAPER_I_III_CANONICAL.pdf) | `SEND/PAPER_3/` | `src/run_paper3.bat` / `.sh` | `python src/verify_paper3.py` |
| Paper IV | Frozen Engine Holdout-5 Exact Replay & Likelihood Benchmark (R40) | [Holdout5 Technical Specification](file:///E:/SEND/PAPER_4/ENTRYPOINT.md) | `SEND/PAPER_4/` | `fast_track_r40/run_r40.bat` / `.sh` | `python fast_track_r40/reproduce_r40.py` |
| Paper V | Authoritative Numerical Replay Freeze & SXS Native Replay | [Paper V Final Report](file:///E:/SEND/PAPER_5/PAPER5_FINAL_REPORT.md) | `SEND/PAPER_5/` | `src/run_paper5.bat` / `.sh` | `python src/verify_paper5.py` |
| Paper VI | Frequency Timing Geometry & Landmark Frequency Freeze | [Paper VI Master Report](file:///E:/SEND/PAPER_6/PAPER_VI_MASTER_REPORT.md) | `SEND/PAPER_6/` | `src/run_paper6.bat` / `.sh` | `python src/verify_paper6.py` |
| Paper VII | Eventwise Observation Layer, C01 Operator & 99 GWOSC Events | [Paper VII Methods Specification](file:///E:/SEND/PAPER_7/EXPECTED_OUTPUTS/MIsCORE_RAW_EVENTWISE_FULL_TF_CHANGE_R1_20260828/METHODS.md) | `SEND/PAPER_7/` | `src/run_paper7.bat` / `.sh` | `python src/run_paper7.py` |
| Paper VIII | Physical Mechanism Closure, GR Memory & ETK Benchmark | [Paper VIII Boundary & Evidence](file:///E:/SEND/PAPER_8/CANDIDATES_AND_BOUNDARY.md) | `SEND/PAPER_8/` | `src/run_paper8.bat` / `.sh` | `python src/verify_paper8.py` |
| Integrated | PRISM / RIUD Integrated Paper I & II Canonical Volume | [Integrated Paper PDF](file:///E:/SEND/PAPER_2/SHARED_FROZEN_AUTHORITY_PACKAGE/01_PAPERS/integrated_paper_package/RIUD_INTEGRATED_PAPER_I_II_FINAL.pdf) | `SEND/PAPER_1/`, `SEND/PAPER_2/` | `src/run_paper1.bat` / `.sh` | `python src/verify_paper1.py` |

## Manuscript Files Available Locally

1. `PRISM_MANUSCRIPT_R8R4_FINAL.pdf` (Paper I): [PRISM_MANUSCRIPT_R8R4_FINAL.pdf](file:///E:/SEND/PAPER_2/SHARED_FROZEN_AUTHORITY_PACKAGE/01_PAPERS/PRISM_MANUSCRIPT_R8R4_FINAL.pdf)
2. `PRISM_SUPPLEMENT_R8R4.pdf` (Paper I Supplement): [PRISM_SUPPLEMENT_R8R4.pdf](file:///E:/SEND/PAPER_2/SHARED_FROZEN_AUTHORITY_PACKAGE/01_PAPERS/PRISM_SUPPLEMENT_R8R4.pdf)
3. `RIUD_PAPERII_MANUSCRIPT_DRAFT_R0.pdf` (Paper II): [RIUD_PAPERII_MANUSCRIPT_DRAFT_R0.pdf](file:///E:/SEND/PAPER_2/NUMERICAL_SOURCES/paper2_manuscript_package/RIUD_PAPERII_MANUSCRIPT_DRAFT_R0.pdf)
4. `RIUD_INTEGRATED_PAPER_I_II_FINAL.pdf` (Integrated Volume): [RIUD_INTEGRATED_PAPER_I_II_FINAL.pdf](file:///E:/SEND/PAPER_2/SHARED_FROZEN_AUTHORITY_PACKAGE/01_PAPERS/integrated_paper_package/RIUD_INTEGRATED_PAPER_I_II_FINAL.pdf)
5. `PAPER_I_III_CANONICAL.pdf` (Papers I–III Canonical): [PAPER_I_III_CANONICAL.pdf](file:///E:/SEND/PAPER_1/SHARED_NUMERICAL_RELEASE_PAPER_I_II/RELEASE_ROOT/00_MANUSCRIPT/PAPER_I_III_CANONICAL.pdf)
6. High-Resolution Figures (Paper I): [HIGH_RES_FIGURES_PAPER_I/](file:///E:/HIGH_RES_FIGURES_PAPER_I) (Figures 1 through 5 at 300 to 600 DPI)

## Data Provenance and Public Catalogs

- GWOSC (Gravitational Wave Open Science Center):
  - Primary strain data: 4-second duration, 4096 Hz sample rate calibrated strain channels for H1 and L1 detectors across 99 events.
  - Public archive: https://gwosc.org/
- SXS (Simulating eXtreme Spacetimes):
  - Numerical relativity waveforms and apparent horizon flux data.
  - Public catalog: https://data.black-holes.org/waveforms/
- Zenodo Archival Records:
  - Numerical releases, frozen engines, and hash manifests are deposited under the MIsCORE-RIUD Zenodo community identifier.
  - DOI prefix: `10.5281/zenodo.17482910` (placeholder reserved for repository public release).
