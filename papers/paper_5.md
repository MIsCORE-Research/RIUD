# Paper V — Authoritative Numerical Replay Freeze & SXS Native Replay

## Summary
Paper V establishes the authoritative numerical replay freeze (R1) encompassing 101 event characterizations, SXS native replay tests, and reviewer defense matrices across the complete development catalog.

## Repository Assets
- Primary Package: [SEND/PAPER_5/](file:///E:/SEND/PAPER_5)
- Final Report: [PAPER5_FINAL_REPORT.md](file:///E:/SEND/PAPER_5/PAPER5_FINAL_REPORT.md)
- Full Audit: [PAPER5_FULL_EXPERIMENT_AUDIT.md](file:///E:/SEND/PAPER_5/PAPER5_FULL_EXPERIMENT_AUDIT.md)
- Manifest: `SEND/PAPER_5/SHA256_MANIFEST.txt` (128 files, 100% verified)
- Companion Numerical Verification Package: [SEND/PAPER_5_CHECK/](file:///E:/SEND/PAPER_5_CHECK/)
  - Short-Track Statistics & Exact Tests: [GAP_POST_T0_SHORT_TRACK_STATS.csv](file:///E:/SEND/PAPER_5_CHECK/GAP_POST_T0_SHORT_TRACK_STATS.csv) ($p_{\text{Fisher}} = 8.3898 \times 10^{-11}$, $p_{\text{perm}} = 1.0 \times 10^{-5}$, spin median $0.4582$)
  - Short-Track 2×2 Contingency Table: [GAP_POST_T0_SHORT_TRACK_2X2.csv](file:///E:/SEND/PAPER_5_CHECK/GAP_POST_T0_SHORT_TRACK_2X2.csv) (7/0 vs 0/89, total 96)
  - Full Audit Report: [00_PAPER_5_NUMERICAL_AUDIT_REPORT.md](file:///E:/SEND/PAPER_5_CHECK/00_PAPER_5_NUMERICAL_AUDIT_REPORT.md)
  - Companion Manifest: `SEND/PAPER_5_CHECK/SHA256_MANIFEST.txt` (3 files, 100% verified)

## Verification
- Windows (1-click): `src\run_paper5.bat`
- Linux / macOS / WSL: `bash src/run_paper5.sh`
- Python: `python src/verify_paper5.py`
- PowerShell: `powershell -File SEND\PAPER_5\REPRODUCTION_PACKAGE\VERIFY_PAPER5_FREEZE.ps1 -Package SEND\PAPER_5`

Expected output: `VERIFY_PAPER5_FREEZE=PASS`.
