# S_A versus landmark timing audit

Input rows: 96
S_A available rows: 73
Input SHA256: c4cf1e1303d70d6bcab088e16c57faefdb7c717ee11a16abc56c11c08d701f03

No refit, no new time reference, and no landmark re-selection were used. T0 is constant in this table and is therefore not a correlation target. S_A is available only for the A-only physical cohort represented in this ledger.

The audit tests whether S_A is itself a timestamp. Correlation with landmarks is descriptive and does not establish causality or a time conversion.
- GAP_TIME: N=73, Spearman=0.10573244477354068, Pearson=0.09940663589504628, status=COMPUTED_FROZEN_EVENT_TABLE
- MT: N=73, Spearman=0.1094518331423363, Pearson=0.152148608636872, status=COMPUTED_FROZEN_EVENT_TABLE
- MAX_FLOW: N=73, Spearman=0.028998301575768645, Pearson=0.059912847963738226, status=COMPUTED_FROZEN_EVENT_TABLE
- PEAK: N=73, Spearman=0.37171417993335804, Pearson=0.26161050962640936, status=COMPUTED_FROZEN_EVENT_TABLE
- W1_START_NATIVE: N=73, Spearman=-0.3806306306306307, Pearson=-0.2567471508031488, status=COMPUTED_FROZEN_EVENT_TABLE
- W2_START_NATIVE: N=70, Spearman=0.37580264193858803, Pearson=0.26979688939844, status=COMPUTED_FROZEN_EVENT_TABLE
- W3_START_NATIVE: N=73, Spearman=-0.3806306306306307, Pearson=-0.2567471508031488, status=COMPUTED_FROZEN_EVENT_TABLE
- W4_START_NATIVE: N=68, Spearman=0.3490094285605222, Pearson=0.2716344967026687, status=COMPUTED_FROZEN_EVENT_TABLE
- W1_END_NATIVE: N=73, Spearman=0.369122547204739, Pearson=0.26097296383817065, status=COMPUTED_FROZEN_EVENT_TABLE
- W2_END_NATIVE: N=70, Spearman=0.3761875601434695, Pearson=0.24551515527458173, status=COMPUTED_FROZEN_EVENT_TABLE
- W3_END_NATIVE: N=73, Spearman=0.3543749228680736, Pearson=0.2395271709759968, status=COMPUTED_FROZEN_EVENT_TABLE
- W4_END_NATIVE: N=68, Spearman=0.36878268504027173, Pearson=0.24456916682475244, status=COMPUTED_FROZEN_EVENT_TABLE
