# H1/L1 frequency-height and width anomaly audit

Scope: existing 10–80 ms diagnostic features and frozen GAP LEFT/CENTER/RIGHT rows. No node/map/GAP search was run; 999/9999 is excluded.

## Frequency bands by width

The table uses event-level medians before population medians. `L1_OVER_H1_MEDIAN_RATIO` is descriptive only and is not a detector calibration.

```text
 WIDTH_MS FREQUENCY_BAND  N_EVENTS  H1_MEDIAN  L1_MEDIAN  L1_OVER_H1_MEDIAN_RATIO  MEDIAN_LOG10_RATIO  IQR_LOG10_RATIO  FRACTION_L1_GREATER
       10     LOW_20_100        96  1.832e-35  8.636e-35                    6.309                 0.8            1.662               0.6562
       10    MID_100_250        96  2.406e-38  1.411e-37                    4.813              0.6824            1.491               0.7083
       10   HIGH_250_512        96  8.373e-39  1.874e-38                    2.571              0.4101            1.503               0.6562
       40     LOW_20_100        96  5.194e-34  1.706e-33                    4.629              0.6655            1.581               0.6875
       40    MID_100_250        96  5.915e-39  4.435e-38                    4.318              0.6353            1.548               0.6771
       40   HIGH_250_512        96  8.182e-39  5.946e-39                   0.2975             -0.5265            2.067               0.3438
       50     LOW_20_100        96  8.606e-36  5.847e-35                    5.424              0.7343            1.522               0.6875
       50    MID_100_250        96  4.472e-39  3.353e-38                    5.072              0.7052             1.55               0.6979
       50   HIGH_250_512        96  1.094e-38  6.097e-39                   0.2291               -0.64            2.192               0.3438
       80     LOW_20_100        96  8.687e-35  5.621e-34                    5.093              0.7069            1.517               0.6771
       80    MID_100_250        96  2.099e-39  1.223e-38                    3.644              0.5616            1.242               0.7083
       80   HIGH_250_512        96  1.646e-38   4.41e-39                   0.1449              -0.839            2.446               0.3229
```


## Direct result

Across the stored widths, 20–100 Hz and 100–250 Hz remain L1-over-H1 positive in the population median. The 250–512 Hz band is the sharp anomaly: it is L1-over-H1 positive at 10 ms but crosses below one by 20–30 ms and becomes increasingly H1-dominant at 40–80 ms. The detector difference is therefore frequency- and width-dependent, not a single H1/L1 gain factor.

The separate directional width audit shows the complementary pattern: phase-rate, high-frequency power and RMS favor L1(10 ms) → H1(broad), while log-amplitude slope and spectral centroid favor the reverse direction. The phase-rate crossover is near 40–50 ms in the existing diagnostic.

## GAP relation

The final table records CENTER−LEFT and RIGHT−CENTER changes for frozen GAP side rows. It is a side-transition characterization, not a new GAP detector.

## Persistent event subset vs frozen GAP-center geometry

The all-8-width subset contains 7 events, but only 6 have a bindable GAP_CENTER row. The >=6-width subset has 30 events, of which 23 have GAP_CENTER rows. These are exploratory group comparisons, not an independent hypothesis test.

```text
      GROUP            OBSERVABLE  N_GROUP  N_OTHER  GROUP_MEDIAN  OTHER_MEDIAN  GROUP_MINUS_OTHER  MANN_WHITNEY_P
GE_6_WIDTHS H1_SPECTRAL_BANDWIDTH       23       72         91.64         10.98              80.66        0.001248
GE_6_WIDTHS L1_SPECTRAL_BANDWIDTH       23       72         2.407         5.327              -2.92        0.009034
GE_6_WIDTHS  H1_SPECTRAL_CENTROID       23       72         34.91         26.31              8.604          0.0042
GE_6_WIDTHS  L1_SPECTRAL_CENTROID       23       72         25.18         25.66            -0.4839          0.0399
GE_6_WIDTHS       PHASE_COHERENCE       23       72         0.989         0.997          -0.008015        0.006803
```

## Event-level frequency signature

At wider windows, a recurring pattern is L1/H1 > 1 in 20–100 and 100–250 Hz while L1/H1 < 1 in 250–512 Hz. The pattern counts are in `WIDTH_FREQUENCY_SIGNATURE_COUNTS.csv`; this is a detector-representation anomaly, not a physical frequency law.
Across events, the pattern occurs in at least 4 of 8 widths for 39/96 events, at least 6 widths for 30/96, and all 8 widths for 7/96.
