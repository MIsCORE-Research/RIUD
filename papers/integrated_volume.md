# PRISM / RIUD Integrated Canonical Volume (Papers I & II)

## Summary
The integrated canonical volume synthesizes Paper I (PRISM frequency-ridge locked detection and catalog morphology controls) and Paper II (Ringdown-Induced Upstream Dynamics and numerical relativity comparison) into a single cohesive manuscript and numerical companion.

## Repository Assets
- Manuscript PDF: [RIUD_INTEGRATED_PAPER_I_II_FINAL.pdf](file:///E:/SEND/PAPER_2/SHARED_FROZEN_AUTHORITY_PACKAGE/01_PAPERS/integrated_paper_package/RIUD_INTEGRATED_PAPER_I_II_FINAL.pdf)
- Canonical Paper I–III PDF: [PAPER_I_III_CANONICAL.pdf](file:///E:/SEND/PAPER_1/SHARED_NUMERICAL_RELEASE_PAPER_I_II/RELEASE_ROOT/00_MANUSCRIPT/PAPER_I_III_CANONICAL.pdf)
- Shared Authority Package: `SEND/PAPER_2/SHARED_FROZEN_AUTHORITY_PACKAGE/`

## Verification
- Windows (1-click): `src\run_paper1.bat` and `src\run_paper2.bat`
- Linux / macOS / WSL: `bash src/run_paper1.sh` and `bash src/run_paper2.sh`
- Python: `python src/verify_paper1.py` and `python src/verify_paper2.py`
Both test suites evaluate the shared numerical release package (`SHARED_NUMERICAL_RELEASE_PAPER_I_II`) and assert exact agreement across 133 individual checks.
