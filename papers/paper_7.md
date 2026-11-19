# Paper VII — Eventwise Observation Layer, C01 Operator & 99 GWOSC Events

## Summary
Paper VII develops the observational data ingestion layer across 99 binary black hole events from the GWOSC catalog (O1, O2, O3, O4). It defines the C01 canonical time-frequency change operator and analyzes changepoint slope dynamics across H1 and L1 strain channels.

## Repository Assets
- Primary Package: [SEND/PAPER_7/](file:///E:/SEND/PAPER_7)
- Methods Specification: [METHODS.md](file:///E:/SEND/PAPER_7/EXPECTED_OUTPUTS/MIsCORE_RAW_EVENTWISE_FULL_TF_CHANGE_R1_20260828/METHODS.md)
- 198 GWOSC Strain Files: `SEND/PAPER_7/STRAIN/<event>/` (99 events × H1/L1)
- Manifest: `SEND/PAPER_7/SHA256_MANIFEST.txt` (286 files, 100% verified)

## Execution & Verification
- Windows (1-click verify): `src\run_paper7.bat`
- Linux / macOS / WSL: `bash src/run_paper7.sh`
- Python: `python src/run_paper7.py --mode verify`
- Full STFT computation across 198 strain files: `python src/run_paper7.py --mode compute`
