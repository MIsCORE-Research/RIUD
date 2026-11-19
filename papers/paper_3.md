# Paper III — Independent Replication Suite & R27 Corroboration Tree

## Summary
Paper III presents a clean-room independent replication of the RIUD detection and statistical pipeline across the development catalog, using the R27 corroboration tree, cold rebuild audit ledgers, and gated numerical releases.

## Repository Assets
- Primary Package: [SEND/PAPER_3/](file:///E:/SEND/PAPER_3)
- Canonical Document: [PAPER_I_III_CANONICAL.pdf](file:///E:/SEND/PAPER_1/SHARED_NUMERICAL_RELEASE_PAPER_I_II/RELEASE_ROOT/00_MANUSCRIPT/PAPER_I_III_CANONICAL.pdf)
- Manifest: `SEND/PAPER_3/SHA256_MANIFEST.txt` (5,792 files, 100% verified)

## Statistical Benchmarks
- Pre-fixed calibrated p-values:
  - H1: $0.005994$ (Replication: $0.009990$)
  - H2: $0.002997$ (Replication: $0.002997$)
  - H3: $0.026973$ (Replication: $0.045954$)
- Final Verdict: `VALIDATED_PARTIALLY_SHARED_DYNAMICS`

## Verification
To run the independent replication verification:
- Windows (1-click): `src\run_paper3.bat`
- Linux / macOS / WSL: `bash src/run_paper3.sh`
- Python: `python src/verify_paper3.py`
Expected output:
```json
{
  "guard_status": "PASS",
  "branch_status_exists": true,
  "independent_replication_status": "PASS",
  "raw_rows": 3,
  "draw_rows": 1000,
  "final_verdict": "VALIDATED_PARTIALLY_SHARED_DYNAMICS",
  "status": "PASS"
}
```
