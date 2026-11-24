# Paper I Verification & Supplementary Replication Suite
## PRISM: Frequency Ridge Locked Validation & Catalog Morphology Controls
### Manuscript Target: *Classical and Quantum Gravity* (CQG)

---

## 1. Executive Summary

This directory (`SEND/PAPER_1_CHECK/`) provides the authoritative numerical replication package and supplementary data for **Paper I** submitted to *Classical and Quantum Gravity* (CQG).

The package covers the two central empirical results of Paper I:
1. **Table 1 (Main Text)**: The 29-event binary black hole (BBH) catalog morphology benchmark across three distinct null and control hypotheses:
   - **Off-source Detector Strain**: 22/29 positive contrast ($p = 0.0081$, Wilcoxon $p = 0.0023$).
   - **Exact GR Waveform Subtraction**: 22/29 positive contrast ($p = 0.0081$, Wilcoxon $p = 0.00067$).
   - **Matched-SNR Waveform Mismatch Bank**: 15/29 positive contrast ($p = 1.0000$, Wilcoxon $p = 0.6239$).
   *Physical conclusion*: The on-source excess vanishes under matched-SNR waveform mismatch, demonstrating that residual excess is governed by template morphology rather than unmodeled detector artifacts.
2. **Table A2 / Section 4.2 (Supplementary Material)**: High-statistics background significance and re-fitting subtraction control across **1,018 disjoint off-source windows** ($4,072$ seconds per event) evaluated on the canonical **87,009-template grid** for four landmark events (`GW190521`, `GW150914`, `GW170104`, `GW170814`).
   - Every event achieves **0 / 1,018 empirical exceedances** ($p < 1/1,019$).

---

## 2. Replication Quick-Start

### Layer 1: Instant Table 1 Verification (< 1 second)

To reproduce the exact numbers, sign tests, Wilcoxon signed-rank tests, and median contrasts for Table 1:

```bash
# From repository root (E:\)
python src/verify_paper1.py

# Or directly within this directory:
python reproduce_table1.py
```

**Expected Console Output:**
```text
================================================================================
MIsCORE-RIUD Paper I — Table 1 Reproduction Suite (29 Events)
Authoritative Manuscript: Classical and Quantum Gravity (CQG)
================================================================================
Loaded 29 binary black hole merger events from PAPER_1_TABLE1_29EVENT_AUDIT.csv

TABLE 1: Event-Level Contrast Statistics Across 29 Evaluated BBH Events
--------------------------------------------------------------------------------
Control Type                           | Positive Events  | Median Contrast  | p (Sign Test)  | p (Wilcoxon)  
--------------------------------------------------------------------------------
Off-source Detector Strain             | 22/29 (75.9%)     |  +0.4435         |    0.00813     |    0.00234    
Exact GR Waveform Subtraction          | 22/29 (75.9%)     |  +0.3733         |    0.00813     |    0.00067    
Matched-SNR Waveform Mismatch Bank     | 15/29 (51.7%)     |  +0.0826         |    1.00000     |    0.62393    
--------------------------------------------------------------------------------

Benchmarking calculated values against frozen PAPER_1_TABLE1_SUMMARY.json:
  [PASS] Off-source Detector Strain: 22/29, median=+0.4435, p_sign=0.00813, p_wilcoxon=0.00234
  [PASS] Exact GR Waveform Subtraction: 22/29, median=+0.3733, p_sign=0.00813, p_wilcoxon=0.00067
  [PASS] Matched-SNR Waveform Mismatch Bank: 15/29, median=+0.0826, p_sign=1.00000, p_wilcoxon=0.62393

ALL PAPER I TABLE 1 BENCHMARKS VERIFIED: 100% MATCH WITH AUTHORITATIVE VALUES.
================================================================================
```

---

### Layer 2: 87,009-Template Background & Refit Subtraction Suite (Table A2)

To re-run the high-statistics 87,009-template background and re-fitting control on continuous 4,096-second GWOSC strain:

```bash
# 1. Canonical Off-source Background Evaluation across 1,018 windows:
python RUN_CANONICAL_87009_GRID_BACKGROUND.py

# 2. Compliant GR Injection + Amplitude/Time Refit + Subtraction Control:
python RUN_GR_INJECTION_REFIT_SUBTRACTION_CONTROL_87009.py
```

*Note*: Full grid evaluation evaluates $1,018 \times 87,009 = 88,575,162$ template correlations per event and takes approximately 1–2 minutes per event with FFT batch vectorization on a modern multi-core workstation. All resulting event-level CSV and Excel files are pre-computed and included in this directory.

---

## 3. High-Statistics Background Results Summary (Table A2)

Evaluated across **1,018 non-overlapping 4.0-second off-source strain windows** per event on the canonical **87,009-point template grid**:

$$\text{Grid: } f_0 \in [30, 250]\,\text{Hz},\quad \tau \in [1, 20]\,\text{ms},\quad \Delta t \in [-10, +10]\,\text{ms},\quad \Delta \phi \in [0, 2\pi]$$

$$\text{Coherent Score Formula: } \text{coh} = \max\left( \frac{|z_H + z_L|}{\sqrt{2}},\, \frac{|z_H - z_L|}{\sqrt{2}} \right)$$

### Canonical Off-Source Background (Raw Detector Noise)

| Event | On-source Score | Null Background Mean $\pm$ Std | Null Background Max | Exceedances |
| :--- | :---: | :---: | :---: | :---: |
| **GW190521** | **22.410994** | $4.380 \pm 0.355$ | 5.868 | **0 / 1,018** |
| **GW150914** | **16.901189** | $2.914 \pm 0.235$ | 3.921 | **0 / 1,018** |
| **GW170104** | **9.805093** | $3.961 \pm 0.299$ | 5.497 | **0 / 1,018** |
| **GW170814** | **20.393390** | $3.822 \pm 0.315$ | 5.360 | **0 / 1,018** |

### Compliant GR Injection + Refit + Subtraction Control (Null Residuals)

| Event | Historical On-source Benchmark | Refit Subtraction Mean $\pm$ Std | Refit Subtraction Max | Exceedances | Empirical $p$-value |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **GW190521** | **22.410994** | $4.379 \pm 0.356$ | 5.868 | **0 / 1,018** | $p < 1/1,019$ |
| **GW150914** | **16.901189** | $2.914 \pm 0.236$ | 3.921 | **0 / 1,018** | $p < 1/1,019$ |
| **GW170104** | **9.805093** | $3.961 \pm 0.299$ | 5.497 | **0 / 1,018** | $p < 1/1,019$ |
| **GW170814** | **20.393390** | $3.822 \pm 0.315$ | 5.360 | **0 / 1,018** | $p < 1/1,019$ |

*Conclusion*: Across all 4,072 independent windows evaluated, no refitted control score approaches the corresponding historical on-source benchmark.

---

## 4. Directory Structure

```text
E:\SEND\PAPER_1_CHECK\
├── README.md                                                        <- This file
├── reproduce_table1.py                                              <- Standalone 1-click Table 1 reproduction script
├── PAPER_1_TABLE1_29EVENT_AUDIT.csv                                 <- Authoritative 29-event event-by-event contrast dataset
├── PAPER_1_TABLE1_SUMMARY.json                                      <- Authoritative benchmark statistics & JSON contract
├── 00_PAPER_1_NUMERICAL_AUDIT_REPORT.md                             <- Full comprehensive numerical audit and methodology report
├── SHA256_MANIFEST.txt                                              <- Authoritative SHA-256 manifest of all files
│
├── RUN_CANONICAL_87009_GRID_BACKGROUND.py                           <- Canonical 87,009-template background evaluation script
├── PAPER_I_SECTION_4_2_CANONICAL_87009_GRID_MASTER.csv              <- Master summary of 87,009-template background runs
├── PAPER_I_SECTION_4_2_CANONICAL_87009_GRID_MASTER.xlsx             <- Excel format of background master
├── GW190521_CANONICAL_87009_GRID_4096S_BACKGROUND.csv               <- Window-by-window scores for GW190521 (1,018 windows)
├── GW150914_CANONICAL_87009_GRID_4096S_BACKGROUND.csv               <- Window-by-window scores for GW150914 (1,018 windows)
├── GW170104_CANONICAL_87009_GRID_4096S_BACKGROUND.csv               <- Window-by-window scores for GW170104 (1,018 windows)
├── GW170814_CANONICAL_87009_GRID_4096S_BACKGROUND.csv               <- Window-by-window scores for GW170814 (1,018 windows)
│
├── RUN_GR_INJECTION_REFIT_SUBTRACTION_CONTROL_87009.py              <- Compliant GR injection, refit, & subtraction script
├── PAPER_I_SECTION_4_2_GR_INJECTION_REFIT_SUBTRACTION_MASTER.csv    <- Master summary of refit subtraction control runs
├── PAPER_I_SECTION_4_2_GR_INJECTION_REFIT_SUBTRACTION_MASTER.xlsx   <- Excel format of refit subtraction master
├── GW190521_GR_INJECTION_REFIT_SUBTRACTION_87009.csv                <- Window-by-window refit scores for GW190521
├── GW150914_GR_INJECTION_REFIT_SUBTRACTION_87009.csv                <- Window-by-window refit scores for GW150914
├── GW170104_GR_INJECTION_REFIT_SUBTRACTION_87009.csv                <- Window-by-window refit scores for GW170104
└── GW170814_GR_INJECTION_REFIT_SUBTRACTION_87009.csv                <- Window-by-window refit scores for GW170814
```

---

## 5. Data Provenance & Integrity

- **Raw Strain Data**: Calibrated 4096 Hz strain data from the Gravitational Wave Open Science Center ([GWOSC](https://gwosc.org/)) for LIGO Hanford (H1) and LIGO Livingston (L1).
- **Event GPS Triggers**:
  - `GW190521`: GPS 1242442967.4
  - `GW150914`: GPS 1126259462.4
  - `GW170104`: GPS 1167559936.6
  - `GW170814`: GPS 1186741861.5
- **Off-source Windows**: Non-overlapping 4.0-second intervals extracted from the continuous 4,096-second strain data, placed safely outside the merger window ($|t - t_{\text{merger}}| > 16.0\,\text{s}$).
- **Integrity**: All files in this package are cryptographically secured. Verify using:
  ```bash
  python -c "import hashlib, sys; [print(f'{p}: PASS' if hashlib.sha256(open(p, 'rb').read()).hexdigest() == h else f'{p}: FAIL') for h, p in [l.strip().split('  ') for l in open('SHA256_MANIFEST.txt') if l.strip()]]"
  ```
