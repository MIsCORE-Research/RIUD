# Paper VIII — Physical Mechanism Closure, GR Memory & ETK Benchmark

## Summary
Paper VIII investigates the underlying general relativistic mechanism connecting ringdown multipoles to apparent horizon dynamics, evaluating the C01 operator, R8 mechanism closure, R7F3 GR memory conditional closure, and numerical waveform convergence with the Einstein Toolkit (ETK).

## Repository Assets
- Primary Package: [SEND/PAPER_8/](file:///E:/SEND/PAPER_8)
- Candidate Boundary Document: [CANDIDATES_AND_BOUNDARY.md](file:///E:/SEND/PAPER_8/CANDIDATES_AND_BOUNDARY.md)
- ETK Benchmark Package: `SEND/PAPER_8/ETK_EXACT_BENCHMARK/`
- Manifest: `SEND/PAPER_8/SHA256_MANIFEST.txt` (387 files, 100% verified)

## Canonical Operator Hash Binding
- Operator C01: `run_eventwise_full_tf_change_separate.py`
- SHA-256: `26B9F63F55D39C715E6DE907F7759A04C9C7427F7F039FDA9507A4AFBF76EF45`
- Parfile SHA-256: `32AD4496...`

## Verification
- Windows (1-click): `src\run_paper8.bat`
- Linux / macOS / WSL: `bash src/run_paper8.sh`
- Python: `python src/verify_paper8.py`

Expected output: `PAPER_8_VERIFICATION=PASS` (387/387 manifest match, C01 hash confirmed).
