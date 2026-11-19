# Paper IV — Frozen Engine Holdout-5 Exact Replay & Likelihood Benchmark (R40)

## Summary
Paper IV evaluates the autonomous dynamical engine R40 against five strictly excluded holdout events (`GW241114_024711`, `GW240830_211120`, `GW240612_081540`, `GW241130_110422`, `GW250119_190238`) without parameter refitting or threshold alterations.

## Repository Assets
- Primary Package: [SEND/PAPER_4/](file:///E:/SEND/PAPER_4)
- Technical Entrypoint: [ENTRYPOINT.md](file:///E:/SEND/PAPER_4/ENTRYPOINT.md)
- Manifest: `SEND/PAPER_4/SHA256_MANIFEST.txt` (51 files, 100% verified)

## Physical Law Benchmark
- Coupling parameter: $\gamma = 0.3162354634393393$
- Baseline parameters: $\beta_2 = -0.304588$, $\beta_3 = -0.016745$, $\beta_4 = 0.371352$, $\gamma_2 = 0.142555$, $\gamma_3 = -0.317756$
- Delta Log-Likelihoods:
  - W1 (START_TO_PEAK): $+1.104333$ (Direction: True)
  - W2 (PEAK_TO_END): $+0.223016$ (Direction: True)
  - W3 (START_TO_MT): $+1.041594$ (Direction: True)
  - W4 (MT_TO_END): $+0.134886$ (Direction: False)

## 1-Click Reproduction
- Windows (1-click): `fast_track_r40\run_r40.bat` (or `src\run_paper4.bat`)
- Linux / macOS / WSL: `bash fast_track_r40/run_r40.sh` (or `bash src/run_paper4.sh`)
- Python: `python fast_track_r40/reproduce_r40.py`
Runtime: ~5 to 10 seconds.
