# Paper V — Authoritative Numerical Replay Freeze & SXS Native Replay

## Summary
Paper V establishes the authoritative numerical replay freeze (R1) encompassing 101 event characterizations, SXS native replay tests, and reviewer defense matrices across the complete development catalog.

## Repository Assets
- Primary Package: [SEND/PAPER_5/](file:///E:/SEND/PAPER_5)
- Final Report: [PAPER5_FINAL_REPORT.md](file:///E:/SEND/PAPER_5/PAPER5_FINAL_REPORT.md)
- Full Audit: [PAPER5_FULL_EXPERIMENT_AUDIT.md](file:///E:/SEND/PAPER_5/PAPER5_FULL_EXPERIMENT_AUDIT.md)
- Manifest: `SEND/PAPER_5/SHA256_MANIFEST.txt` (128 files, 100% verified)

## Verification
- Windows (1-click): `src\run_paper5.bat`
- Linux / macOS / WSL: `bash src/run_paper5.sh`
- Python: `python src/verify_paper5.py`
- PowerShell: `powershell -File SEND\PAPER_5\REPRODUCTION_PACKAGE\VERIFY_PAPER5_FREEZE.ps1 -Package SEND\PAPER_5`

Expected output: `VERIFY_PAPER5_FREEZE=PASS`.
