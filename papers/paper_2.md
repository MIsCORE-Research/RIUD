# Paper II — RIUD: Numerical Relativity SXS Mirror & R26 Permutation Null Companion

## Summary
Paper II introduces the Ringdown-Induced Upstream Dynamics (RIUD) framework, benchmarking detected candidate signatures against numerical relativity simulations from the SXS catalog, surrogate models, and R26 permutation null distributions.

## Repository Assets
- Primary Package: [SEND/PAPER_2/](file:///E:/SEND/PAPER_2)
- Manuscript Draft: [RIUD_PAPERII_MANUSCRIPT_DRAFT_R0.pdf](file:///E:/SEND/PAPER_2/NUMERICAL_SOURCES/paper2_manuscript_package/RIUD_PAPERII_MANUSCRIPT_DRAFT_R0.pdf)
- Manifest: `SEND/PAPER_2/SHA256_MANIFEST.txt` (356 files, 100% verified)

## Key Numerical Quantities
- DEV97 Null Permutation: $p = 0.00019996$, Spearman $\rho = 0.104526$, Rayleigh $p = 0.971843$.
- Authority SHA-256 closure: 340 / 340 entries verified.

## Verification
To run the numerical companion check:
- Windows (1-click): `src\run_paper2.bat`
- Linux / macOS / WSL: `bash src/run_paper2.sh`
- Python: `python src/verify_paper2.py`

Expected output: `NUMERICAL_CHECK=PASS`, `CHECKS=133`, `FAILED=NONE`.
