# RIUD frequency-family × K-axis × ABC × geometry exploration

## Scope

This assembled release preserves the completed exploratory audits as-is. The
free exploration is the primary result; the axis cross-audit is retained as a
separate supporting branch. No new scientific calculation, map/path rebuild,
score averaging, refit, null, or Holdout30 access occurred during assembly.

The event-level table uses the existing exact joins and preserves missingness.
K1/K2 are branch-local 16-event axes, K5 is the existing global R40 axis, and
the A-only K5 view is retained only as an existing diagnostic subset.

## Frozen source definitions represented here

- K1 / GR16: `0.22727260016061515*z_BRANCH(CHI_P)`; branch-local N=16.
- K2 / OBS16: `2.2539666336842394*z_BRANCH(M_DET) - 1.9356907205819978*z_BRANCH(MC_DET)`; branch-local N=16.
- K5 / global: `0.22030031492055946*z(R) + 0.3457660274266933*z(CHI_A_NORMALIZED)`; N=96.
- K5 / A-only diagnostic: `0.26368072470484993*z_A(R) + 0.19053949293019626*z_A(CHI_A_NORMALIZED)`; N=73.

## Key numerical readout

- Free exploration event rows: 98
- Stored S axis rows: 96; S is retained independently from K5-labelled score fields.
- Four-way/common-16 combination rows: 378
- Frequency-family plots: 17 SVG files
- K5 R40 vs R39 max absolute score difference: `2.220446049250313e-16`.
- K5 vs observed active-fraction target: Spearman `-0.436902694303`, Pearson `-0.381984809031`.
- K1 branch target: Spearman `0.453274589233`, Pearson `0.387741875741`.
- K2 branch target: Spearman `0.554213047587`, Pearson `0.640285120373`.
- Common-16 K1×K2: Spearman `0.582352941176`, p=`0.017932734131`, N=16.
- Common-16 K1×K5: Spearman `0.452941176471`, p=`0.0780987414167`, N=16.
- Common-16 K2×K5: Spearman `0.414705882353`, p=`0.110229403918`, N=16.
- Frequency MAG vs CHI_A: Kruskal H=`10.980300759109817`, p=`0.0009208548426330285`.
- Frequency SHAPE vs CHI_A: H=`0.4191`, p=`0.51737`.

## Interpretation boundary

These are descriptive and exploratory comparisons, not a selected integrated
regression or a new physical law. K1 and K2 have exact branch-local N=16
coverage and are not population-wide independent axes. The MAG/CHI_A result
is an association in the existing data; it is not causal evidence. Small-cell
ABC/family/geometry contrasts are preserved in the tables without being
promoted to claims.

## Source summaries

### Free exploration branch
R_STATUS=PASS_FREE_EXPLORATORY_CROSS_AUDIT
MODE=FREE_EXPLORATION_NO_INTEGRATED_REGRESSION
N_EVENT_ROWS=98
N_FREQUENCY_ROWS=98
N_ABC_ROWS=96
N_K5_GLOBAL=96
N_K5_A_ONLY=73
N_K1_GR16=16
N_K2_OBS16=16
RAW_PHYSICAL_COVERAGE=R/CHI_A on 96-event K5 source; M_DET/MC_DET/Q/ETA/CHI_EFF/CHI_P/SPIN1Z/SPIN2Z on exact 16-event K1/K2 source
SCORE_AVERAGING=FALSE
NEW_MAP=FALSE
NEW_PATH=FALSE
NEW_K_LAW=FALSE
CAUSAL_CLAIM=FALSE
HOLDOUT30_ACCESSED=FALSE
NOTE=Contrasts and plots are discovery-oriented descriptions; no p-value or regression is promoted as a law
PLOTS=SVG standard-library plots in plots/; no matplotlib dependency
RANK_BINS=Exploratory within-axis rank terciles only; not scientific thresholds
COUNTS_FREQ_MAG_FAMILY={'FREQ_MAG_2': 64, 'FREQ_MAG_1': 34}
COUNTS_FREQ_SHAPE_FAMILY={'FREQ_SHAPE_1': 63, 'FREQ_SHAPE_2': 35}
COUNTS_ABC_CLASS={'A': 74, 'C': 10, 'OTHER': 7, 'B': 5, nan: 2}
K1_X_K2_COMMON16_SPEARMAN_RHO=0.582352941176|p=0.017932734131|N=16
K1_X_K5_COMMON16_SPEARMAN_RHO=0.452941176471|p=0.0780987414167|N=16
K2_X_K5_COMMON16_SPEARMAN_RHO=0.414705882353|p=0.110229403918|N=16
DERIVED_AXIS_WARNING=K1 is frozen linear CHI_P branch score; K5 includes frozen R and CHI_A; these constructional correlations are not independent discoveries
COMMON16_ABC_SCOPE=K1/K2 common branch contains B=5,C=10,OTHER=1 and no A events


### Axis cross-audit branch
R_STATUS=PASS_EXPLORATORY_CROSS_AUDIT
PURPOSE=Frequency family x K1/K2/K5 x ABC x geometry; axes kept separate
NO_SCORE_AVERAGING=TRUE
NO_MAP_OR_PATH_REBUILD=TRUE
K1_SCOPE=GR16 branch-local, N=16
K2_SCOPE=OBS16 branch-local, N=16
K5_SCOPE=global R40/R39 P1, N=96
K5_R40_R39_MAX_ABS_SCORE_DIFF=2.220446049250313e-16
K5_GLOBAL_N_SCORE=96
K1_GR16_N_SCORE=16
K2_OBS16_N_SCORE=16
K5_A_ONLY_N_SCORE=73
K5_GLOBAL_SCORE_TARGET_SPEARMAN=-0.436902694303
K5_GLOBAL_SCORE_TARGET_PEARSON=-0.381984809031
K1_GR16_SCORE_TARGET_SPEARMAN=0.453274589233
K1_GR16_SCORE_TARGET_PEARSON=0.387741875741
K2_OBS16_SCORE_TARGET_SPEARMAN=0.554213047587
K2_OBS16_SCORE_TARGET_PEARSON=0.640285120373
K5_GLOBAL_INCREMENTAL_DELTA_R2=2.28695969573e-05
K5_GLOBAL_INCREMENTAL_DELTA_BIC=4.46460946347
K1_GR16_INCREMENTAL_DELTA_R2=0.388629317279
K1_GR16_INCREMENTAL_DELTA_BIC=-9.125672155
K2_OBS16_INCREMENTAL_DELTA_R2=0.016046293618
K2_OBS16_INCREMENTAL_DELTA_BIC=-0.0903689328991
FAMILY_PHYSICAL_TEST=FREQ_MAG_FAMILY|CHI_A|N=96|Kruskal_H=10.980300759109817|p=0.0009208548426330285
FAMILY_PHYSICAL_TEST=FREQ_SHAPE_FAMILY|CHI_A|N=96|Kruskal_H=0.4191364495718935|p=0.5173682539122169
FAMILY_PHYSICAL_TEST=FREQ_MAG_FAMILY|R|N=96|Kruskal_H=0.9918034390344133|p=0.31930199736385195
FAMILY_PHYSICAL_TEST=FREQ_SHAPE_FAMILY|R|N=96|Kruskal_H=0.0678417026937268|p=0.7945055739633357
FAMILY_PHYSICAL_TEST=FREQ_MAG_FAMILY|M_DET|N=16|Kruskal_H=0.4235294117647044|p=0.515181169612164
FAMILY_PHYSICAL_TEST=FREQ_SHAPE_FAMILY|M_DET|N=16|Kruskal_H=1.9882352941176507|p=0.1585255172289507
FREQ_MAG_FAMILY_FREQ_MAG_1_N=34_K5_MEAN=-0.192732461454_K5_MEDIAN=-0.166956087309
FREQ_MAG_FAMILY_FREQ_MAG_2_N=64_K5_MEAN=0.105691994991_K5_MEDIAN=0.0719475890387
FREQ_SHAPE_FAMILY_FREQ_SHAPE_1_N=63_K5_MEAN=0.0301661810913_K5_MEDIAN=0.00573379948421
FREQ_SHAPE_FAMILY_FREQ_SHAPE_2_N=35_K5_MEAN=-0.0550089184606_K5_MEDIAN=-0.112319590003
INTERPRETATION=Descriptive cross-axis comparison; K1/K2 branch-local and not pooled with K5
PHYSICAL_VARIABLE_COVERAGE_NOTE=M_DET/MC_DET/Q/ETA/CHI_EFF/CHI_P/SPIN1Z/SPIN2Z are available only on the exact 16-event K1/K2 source intersection; R/CHI_A are available on the 96-event K5 source
CAUSAL_CLAIM=FALSE
NEW_K_LAW_FIT=FALSE
HOLDOUT30_ACCESSED=FALSE


## Reproduction/provenance

The original source/output folders remain untouched. This folder is an
assembled evidence release, not a self-contained raw-data reproduction
package: external source paths and hashes are recorded in
`04_REFERENCE_INPUTS/INPUT_REFERENCE_PATHS.tsv`. The two analysis scripts are
copied under `03_SOURCE_SCRIPTS/`.
