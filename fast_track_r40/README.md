# R40 Holdout-5 Reproduction Guide

## Overview

This package provides a standalone, one-command reproduction suite for the R40 physical law benchmark established in Paper IV and referenced across Papers V through VIII. The evaluation computes likelihood trajectories and active fraction predictions under two competing hypotheses:

1. Null Hypothesis ($P_0$): Baseline transition rate model conditioned on prior run states and age.
2. Physical Law Hypothesis ($P_1$): Dynamic linear coupling of the physical coordinate $S$ with coupling constant $\gamma = 0.3162354634393393$.

## Physical Coordinate Formulation

The coordinate $S$ is evaluated from pre-merger and remnant physical observables:

$$R = \frac{M_{\mathrm{irr,final}}}{M_{\mathrm{irr,1}} + M_{\mathrm{irr,2}}}$$

$$\chi_{A,\mathrm{norm}} = \frac{\chi_{1z} - \chi_{2z}}{|\chi_{1z}| + |\chi_{2z}|}$$

$$S = 0.22030031492055946 \cdot z(R) + 0.3457660274266933 \cdot z(\chi_{A,\mathrm{norm}})$$

where $z(\cdot)$ denotes the standard score transformation across the developmental catalog.

Hazard rates are parameterized as:

$$\eta_0(u) = \text{base\_log\_rate}_j(u) - 0.304588 \cdot I(\text{run}=2) - 0.016745 \cdot I(\text{run}=3) + 0.371352 \cdot I(\text{run}\ge 4) + 0.142555 \cdot I(\text{state}\ne N_0, \text{age}=2) - 0.317756 \cdot I(\text{state}\ne N_0, \text{age}\ge 3)$$

$$\eta_{P_1}(u) = \eta_0(u) + \gamma \cdot S$$

$$\lambda(u) = \exp(\eta(u)), \quad p = 1 - \exp(-\lambda(u) \cdot \Delta u)$$

with frozen step size $\Delta u = 0.03125$.

## Reproduction Command

From the repository root:

```bash
python fast_track_r40/reproduce_r40.py
```

Or on Windows:

```cmd
fast_track_r40\run_r40.bat
```

Or on Linux / macOS / WSL:

```bash
bash fast_track_r40/run_r40.sh
```

Execution runtime is typically under 10 seconds on standard x86_64 hardware.

## Canonical Reference Benchmarks

The 5 holdout events evaluated are `GW241114_024711`, `GW240830_211120`, `GW240612_081540`, `GW241130_110422`, and `GW250119_190238`.

Expected Delta log-likelihoods ($\Delta \ln \mathcal{L} = \ln \mathcal{L}_{P_1} - \ln \mathcal{L}_{P_0}$):

| Window | Definition | Delta Log-Likelihood | Direction Agreement |
|---|---|---|---|
| W1 | START_TO_PEAK | +1.104333 | True |
| W2 | PEAK_TO_END | +0.223016 | True |
| W3 | START_TO_MT | +1.041594 | True |
| W4 | MT_TO_END | +0.134886 | False |

The script compares generated values against `SEND/PAPER_4/CANONICAL_REFERENCE/HOLDOUT5_R40_W1_W4_EXACT_LIKELIHOOD.csv` and asserts numerical consistency within $10^{-5}$ relative tolerance.
