# MIsCORE Paper VI — Frequency, Timing, and Geometry

## Scope

This Paper VI record assembles existing DEV99 frequency-family, landmark,
ABC/GAP, geometry, physical-axis, prediction, mismatch, and Holdout5 replay
outputs. It is an evidence assembly; no science was rerun, no map/path was
rebuilt, no threshold or law was refit, and Holdout30 was not accessed.

```text
PUBLIC_FRAMEWORK=MIsCORE physical-law framework
NEW_SCIENCE_RUN=FALSE
NEW_MAP=FALSE
NEW_PATH=FALSE
NEW_FAMILY_RECLASSIFICATION=FALSE
HOLDOUT30_ACCESSED=FALSE
```

## 1. Frequency-family population

DEV99 contains 99 events: 98 PATH_FOUND and one NO_PATH event
(`GW241230_233618`). The frequency-only K=2 census produced FREQ_1=90 and
FREQ_2=8. The frozen two-axis census produced:

```text
FREQ_MAG_1=34, FREQ_MAG_2=64
FREQ_SHAPE_1=63, FREQ_SHAPE_2=35
```

MAG uses the frozen frequency-variation representation. SHAPE uses the
within-event normalized `f_shape_00..f_shape_31` profile. They were kept
separate; width, transition, node count, ABC, A2, S, and legacy H labels were
not used to define the frequency families.

## 2. Landmark and transition structure

The integrated landmark branch contains the exact PATH×A2 intersection of 96
events and includes available GAP, t0, MT, PEAK, MAX_FLOW, support, and W
fields without imputing incomplete W2/W4 fields. The R0Q finer census contains
28 event records with span cuts at 40 and 60 Hz.

The frequency-family physical audit contains 98 event joins and 985 transition
joins. Its descriptive candidate is `V_f=Δf/Δτ` conditioned on MAG×SHAPE,
with Kruskal net-rate p=5.131479928700461e-11. This remains an empirical
candidate, not a fundamental law.

The GAP score-field profile contains 16 records; 8/16 have an intermediate
maximum z below 1. The source interpretation is a representation-level
trough or connection penalty, not proof of physical signal disappearance.

## 3. Pre-transition prediction and geometry

The pre-transition OOF audit has 91 scorable events:

```text
direction accuracy=0.3956043956043956
net-rate Spearman=0.041645305678419536
direction-null p=0.683
net-rate-null p=0.264
```

Geometry augmentation did not improve the fixed branch:

```text
family-only direction=0.3956043956043956
family+geometry direction=0.3956043956043956
family+geometry net rho=-0.12630320869718734
GEOMETRY_INCREMENTAL_SUPPORT=NO_INCREMENTAL_GEOMETRY_SUPPORT
```

The fixed-rule mismatch audit found MAG=6, SHAPE=30, GAP-order=3, and
GAP-side=1 full-input mismatches. These remain diagnostic boundaries and were
not used to create a revised law.

## 4. Physical axes and R40 inheritance

The exploratory axes remain separate:

```text
K1=0.22727260016061515*z_BRANCH(CHI_P), N=16
K2=2.2539666336842394*z_BRANCH(M_DET)
   -1.9356907205819978*z_BRANCH(MC_DET), N=16
K5=0.22030031492055946*z(R)
   +0.3457660274266933*z(CHI_A_NORMALIZED), N=96
```

The canonical R40 layer remains:

```text
S=0.22030031492055946*z(R)+0.3457660274266933*z(CHI_A)
eta=eta_node+0.3162354634393393*S
lambda=exp(eta)
p=1-exp(-lambda*Delta_u)
```

R40 is the physical transition-rate sub-law. MAG/SHAPE/ABC/GAP are the
frequency–timing–geometry phenotype/application layer.

## 5. Holdout5 official replay

The DEV99 family system and fixed branch were applied without refit:

```text
DEV99_FAMILY_SYSTEM_FROZEN=TRUE
HOLDOUT5_NO_REFIT_REPLAY=PASS
MAG_REPLAY=5/5
SHAPE_REPLAY=4/4
ABC_GAP_REPLAY=4/4
PRESPECIFIED_EXCEPTION=1/5
```

`GW240612_081540` is excluded only from GAP-dependent outputs because its
GAP/ABC landmark is unavailable. The replay counts mean the frozen formulas
and branches were applied to scorable inputs; they are not a claim of
independent H5 label accuracy.

## 6. MIsCORE framework and claim boundary

```text
MIsCORE physical-law framework
├── R40: physical transition-rate layer (S → eta → lambda → p)
└── frequency layer: MAG / SHAPE / ABC / GAP / geometry application layer
```

Frequency-family separation is supported descriptively. The frequency-rate
candidate is empirical only. Strong pre-transition prediction and incremental
geometry support are not supported by the fixed OOF audits. No detector/source
identity claim, causal claim, GR-violation claim, direct Einstein derivation,
or new-physics claim is made.
