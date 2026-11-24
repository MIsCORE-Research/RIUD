#!/usr/bin/env python3
"""
Paper I Table 1 Reproducibility Runner: 29-Event Catalog Morphological Controls
================================================================================
Reproduces Table 1 and all statistical tests from the authoritative event-by-event
contrast records (PAPER_1_TABLE1_29EVENT_AUDIT.csv) for Classical and Quantum Gravity (CQG).

Comparators evaluated:
  1. Off-source detector noise: 22/29 positive (p_sign = 0.0081, p_wilcoxon = 0.0023)
  2. Exact GR waveform subtraction: 22/29 positive (p_sign = 0.0081, p_wilcoxon = 0.00067)
  3. Matched-SNR waveform mismatch bank: 15/29 positive (p_sign = 1.0000, p_wilcoxon = 0.6239)

Usage:
  python reproduce_table1.py
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    csv_path = script_dir / "PAPER_1_TABLE1_29EVENT_AUDIT.csv"
    summary_path = script_dir / "PAPER_1_TABLE1_SUMMARY.json"

    if not csv_path.exists():
        print(f"ERROR: Audit CSV not found at {csv_path}", file=sys.stderr)
        return 1

    df = pd.read_csv(csv_path)
    n_events = len(df)

    print("=" * 80)
    print("MIsCORE-RIUD Paper I — Table 1 Reproduction Suite (29 Events)")
    print("Authoritative Manuscript: Classical and Quantum Gravity (CQG)")
    print("=" * 80)
    print(f"Loaded {n_events} binary black hole merger events from {csv_path.name}")
    print()

    comparators = [
        ("Off-source Detector Strain", "OFFSOURCE_CONTRAST", "OFFSOURCE_POSITIVE"),
        ("Exact GR Waveform Subtraction", "EXACT_SUBTRACTION_CONTRAST", "EXACT_SUBTRACTION_POSITIVE"),
        ("Matched-SNR Waveform Mismatch Bank", "MISMATCH_BANK_CONTRAST", "MISMATCH_BANK_POSITIVE"),
    ]

    results = {}

    for name, col_contrast, col_pos in comparators:
        contrasts = df[col_contrast].values.astype(float)
        n_pos = int(np.sum(contrasts > 0))
        n_total = len(contrasts)
        frac_pos = n_pos / n_total

        median_val = float(np.median(contrasts))
        mean_val = float(np.mean(contrasts))
        std_val = float(np.std(contrasts, ddof=1))

        # Two-sided exact binomial sign test (null: p = 0.5)
        # scipy.stats.binomtest in modern scipy, or scipy.stats.binom_test
        if hasattr(stats, "binomtest"):
            res_binom = stats.binomtest(k=n_pos, n=n_total, p=0.5, alternative="two-sided")
            p_sign = float(res_binom.pvalue)
        else:
            p_sign = float(stats.binom_test(x=n_pos, n=n_total, p=0.5, alternative="two-sided"))

        # Two-sided Wilcoxon signed-rank test against 0
        w_res = stats.wilcoxon(contrasts, alternative="two-sided")
        p_wilcoxon = float(w_res.pvalue)

        results[col_contrast] = {
            "name": name,
            "n_pos": n_pos,
            "n_total": n_total,
            "frac_pos": frac_pos,
            "median": median_val,
            "mean": mean_val,
            "std": std_val,
            "p_sign": p_sign,
            "p_wilcoxon": p_wilcoxon,
        }

    # Print Table 1 Formatted
    print("TABLE 1: Event-Level Contrast Statistics Across 29 Evaluated BBH Events")
    print("-" * 80)
    header = f"{'Control Type':<38} | {'Positive Events':<16} | {'Median Contrast':<16} | {'p (Sign Test)':<14} | {'p (Wilcoxon)':<14}"
    print(header)
    print("-" * 80)
    for k, v in results.items():
        row = (
            f"{v['name']:<38} | "
            f"{v['n_pos']}/{v['n_total']} ({v['frac_pos']*100:.1f}%)"
            f"{'':<4} | "
            f"{v['median']:>+8.4f}{'':<8} | "
            f"{v['p_sign']:>10.5f}{'':<4} | "
            f"{v['p_wilcoxon']:>10.5f}{'':<4}"
        )
        print(row)
    print("-" * 80)
    print()

    # Verify against frozen JSON benchmark if available
    if summary_path.exists():
        with open(summary_path, "r", encoding="utf-8") as f:
            summary_ref = json.load(f)

        ref_comp = summary_ref.get("comparators", {})
        mapping = {
            "OFFSOURCE_CONTRAST": "off_source_strain",
            "EXACT_SUBTRACTION_CONTRAST": "exact_waveform_subtraction",
            "MISMATCH_BANK_CONTRAST": "matched_snr_mismatch_bank",
        }

        all_passed = True
        print("Benchmarking calculated values against frozen PAPER_1_TABLE1_SUMMARY.json:")
        for col_contrast, ref_key in mapping.items():
            if ref_key in ref_comp:
                ref = ref_comp[ref_key]
                calc = results[col_contrast]

                ref_pos = ref["positive_events"]
                calc_pos = f"{calc['n_pos']}/{calc['n_total']}"
                assert calc_pos == ref_pos, f"Positive count mismatch: {calc_pos} vs {ref_pos}"

                assert math.isclose(calc["median"], ref["median_contrast"], rel_tol=1e-5), \
                    f"Median mismatch: {calc['median']} vs {ref['median_contrast']}"

                assert math.isclose(calc["p_sign"], ref["sign_p_twosided"], rel_tol=1e-4), \
                    f"Sign p mismatch: {calc['p_sign']} vs {ref['sign_p_twosided']}"

                assert math.isclose(calc["p_wilcoxon"], ref["wilcoxon_p_twosided"], rel_tol=1e-4), \
                    f"Wilcoxon p mismatch: {calc['p_wilcoxon']} vs {ref['wilcoxon_p_twosided']}"

                print(f"  [PASS] {calc['name']}: {calc_pos}, median={calc['median']:+.4f}, p_sign={calc['p_sign']:.5f}, p_wilcoxon={calc['p_wilcoxon']:.5f}")

        print()
        print("ALL PAPER I TABLE 1 BENCHMARKS VERIFIED: 100% MATCH WITH AUTHORITATIVE VALUES.")
    else:
        print("[WARNING] Frozen summary JSON not found, skipping comparison benchmark.")

    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
