# Structured anomaly controls

999/9999 is excluded. These controls use the existing 10–80 ms feature grid only; no new node/map/GAP search was performed.

## 1. Fixed gain control

For a fixed multiplicative detector gain, `log10(L1/H1)` changes by a constant offset. Its within-event slope versus width is unchanged. The observed high-band slope is therefore a gain-invariant width effect.

- LOW_20_100: median slope=-0.0021546/ms; negative slopes=52/96; one-sided sign p=0.2376
- MID_100_250: median slope=-0.0011961/ms; negative slopes=59/96; one-sided sign p=0.01577
- HIGH_250_512: median slope=-0.00842472/ms; negative slopes=71/96; one-sided sign p=1.434e-06

## 2. Offset persistence

 WIDTH_MS  N_OFFSETS  PATTERN_OFFSETS  HIGH_NEG_OFFSETS  PATTERN_FRACTION  HIGH_NEG_FRACTION
       10         31                0                 0                 0                  0
       20         31               31                31                 1                  1
       30         31               31                31                 1                  1
       40         31               31                31                 1                  1
       50         31               31                31                 1                  1
       60         31               31                31                 1                  1
       70         31               31                31                 1                  1
       80         31               31                31                 1                  1

At widths 20–80 ms, the population-median high-band sign is negative at all 31 stored offsets, not only at the center bin.

## 3. Same-event pairing control

The cyclic-shift table compares the observed H1/L1 event pairing with all 96 circularly shifted pairings. It tests event matching, not the 999 experiment.

 WIDTH_MS FREQUENCY_BAND  N_EVENTS  REAL_PEARSON  REAL_SPEARMAN  CYCLIC_PEARSON_MEDIAN  CYCLIC_PEARSON_MAX  REAL_PEARSON_RANK  CYCLIC_SPEARMAN_MEDIAN  CYCLIC_SPEARMAN_MAX  REAL_SPEARMAN_RANK
       10     LOW_20_100        96        0.6444         0.6676               -0.02939              0.6444                 97                -0.05107               0.6676                  97
       10    MID_100_250        96        0.6503         0.6867               -0.02338              0.6503                 97                -0.06747               0.6867                  97
       10   HIGH_250_512        96        0.6067          0.643               0.001746              0.6067                 97                 -0.0284                0.643                  97
       20     LOW_20_100        96        0.6504         0.6722               -0.02797              0.6504                 97                -0.05383               0.6722                  97
       20    MID_100_250        96        0.6204         0.6667              -0.009731              0.6204                 97                -0.05444               0.6667                  97
       20   HIGH_250_512        96        0.3049         0.2956               -0.01296              0.3102                 96               -0.005338               0.3168                  92
       30     LOW_20_100        96        0.6567         0.6721               -0.03021              0.6567                 97                -0.05732               0.6721                  97
       30    MID_100_250        96        0.6123         0.6586              -0.002793              0.6123                 97                -0.04719               0.6586                  97
       30   HIGH_250_512        96        0.1823         0.1334               -0.02198              0.3506                 89                -0.01549               0.4063                  77
       40     LOW_20_100        96         0.662         0.6798               -0.03709               0.662                 97                -0.05397               0.6798                  97
       40    MID_100_250        96        0.6216         0.6577               -0.01234              0.6216                 97                -0.05016               0.6577                  97
       40   HIGH_250_512        96       0.08258        0.01776               -0.01375               0.369                 73               -0.006579               0.4506                  54
       50     LOW_20_100        96         0.597         0.6534               -0.01648               0.597                 97                -0.05023               0.6534                  97
       50    MID_100_250        96         0.629         0.6574               -0.01739               0.629                 97                -0.05309               0.6574                  97
       50   HIGH_250_512        96       0.05579       -0.01496              -0.007359              0.3682                 65                 0.00742               0.4514                  41
       60     LOW_20_100        96        0.5983         0.6557               -0.01376              0.5983                 97                -0.05103               0.6557                  97
       60    MID_100_250        96        0.6487         0.6729               -0.01514              0.6487                 97                -0.05589               0.6729                  97
       60   HIGH_250_512        96        0.0254       -0.05269               0.000724              0.3863                 57               0.0002781               0.4424                  33
       70     LOW_20_100        96        0.5996         0.6553               -0.01278              0.5996                 97                -0.05446               0.6553                  97
       70    MID_100_250        96        0.6603         0.6818               -0.02187              0.6603                 97                -0.06215               0.6818                  97
       70   HIGH_250_512        96        0.0167       -0.06815               0.009961              0.3926                 52                0.005629               0.4395                  30
       80     LOW_20_100        96        0.5995         0.6578               -0.01328              0.5995                 97                -0.06158               0.6578                  97
       80    MID_100_250        96        0.6792         0.6856               -0.02863              0.6792                 97                -0.06211               0.6856                  97
       80   HIGH_250_512        96      0.005325       -0.07168               0.005853              0.4001                 49                0.005534               0.4426                  30

## Interpretation

The high-frequency reversal is not explainable by a fixed detector gain and is not confined to one stored offset. The event-pairing control quantifies whether the detector contrast is tied to the same event; it must be read together with the within-event width slope and offset persistence. These controls establish structured representation behavior, not astrophysical origin.
