# Paper VI — Frequency Timing Geometry & Landmark Frequency Freeze

## Summary
Paper VI formalizes the frequency-timing geometry of the post-merger signal, locking 20 primary evidence components and cataloging pre-transition and post-merger transition rates.

## Repository Assets
- Primary Package: [SEND/PAPER_6/](file:///E:/SEND/PAPER_6)
- Master Report: [PAPER_VI_MASTER_REPORT.md](file:///E:/SEND/PAPER_6/PAPER_VI_MASTER_REPORT.md)
- Manifest: `SEND/PAPER_6/SHA256_MANIFEST.txt` (219 files, 100% verified)

## Reference Quantities (from `NUMERICAL_SUMMARY.csv`)
- `FREQ_RATE_P`: $5.131480 \times 10^{-11}$
- `PRETRANSITION_ACC`: $0.395604$
- `POST_G_GAP_P`: $0.009901$
- `GEOMETRY_GLOBAL_PC1_S`: $0.343457$
- H5 Consistency: Magnitude 5/5, Shape 4/4, ABC/GAP 4/4 PASS.

## Verification
- Windows (1-click): `src\run_paper6.bat`
- Linux / macOS / WSL: `bash src/run_paper6.sh`
- Python: `python src/verify_paper6.py`

Expected output: `PAPER_6_VERIFICATION=PASS` (Manifest 219/219 match, numerical summary validated).
