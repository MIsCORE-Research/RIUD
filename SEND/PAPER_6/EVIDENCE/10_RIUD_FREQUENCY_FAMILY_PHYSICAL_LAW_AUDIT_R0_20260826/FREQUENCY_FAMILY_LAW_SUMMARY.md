# FREQUENCY FAMILY PHYSICAL-LAW AUDIT R0

## Frozen input and scope

The existing frequency-only FREQ_MAG/FREQ_SHAPE labels are used without rebuilding them.
No GAP, node count, width, transition, ABC, A2, or S label is used to define the family.
EVENT_FAMILY_JOIN_N=98
TRANSITION_FAMILY_JOIN_N=985
LANDMARK_JOIN_N=96

## Empirical relation

Candidate relation: V_f = Delta f / Delta tau, conditioned on (FREQ_MAG, FREQ_SHAPE).
The shape family primarily fixes the sign of net frequency motion; the magnitude family changes the scale of total frequency activity.

FREQ_MAG_FAMILY FREQ_SHAPE_FAMILY             FAMILY_CELL  N_EVENTS  MEDIAN_NET_FREQ_RATE_HZ_S  MEAN_NET_FREQ_RATE_HZ_S  MEDIAN_TOTAL_FREQ_RATE_HZ_S  MEDIAN_NET_CHANGE_HZ  MEDIAN_TOTAL_VARIATION_HZ  MEDIAN_F_DIRECTNESS  MEDIAN_TURNS  MEDIAN_PATH_NODES  FALLING  FLAT  RISING
     FREQ_MAG_1      FREQ_SHAPE_1 FREQ_MAG_1|FREQ_SHAPE_1        21                 866.666667               831.374446                  1166.666667                  90.0                      120.0             0.800000           1.0               14.0        1     0      20
     FREQ_MAG_1      FREQ_SHAPE_2 FREQ_MAG_1|FREQ_SHAPE_2        13                -384.615385              -176.089722                  1266.666667                 -50.0                      170.0             0.368421           2.0               14.0        8     1       4
     FREQ_MAG_2      FREQ_SHAPE_1 FREQ_MAG_2|FREQ_SHAPE_1        42                 266.666667               306.566053                   516.666667                  20.0                       40.0             0.888889           0.5                9.5        3     7      32
     FREQ_MAG_2      FREQ_SHAPE_2 FREQ_MAG_2|FREQ_SHAPE_2        22                 -83.333333              -263.852814                   683.333333                 -10.0                       60.0             0.714286           1.0                8.5       12     7       3

KRUSKAL_NET_FREQ_RATE_STAT=50.902608677233985
KRUSKAL_NET_FREQ_RATE_P=5.131479928700461e-11

## Interpretation

FREQ_SHAPE is a direction/trajectory-shape axis, while FREQ_MAG is an activity-scale axis. Their combination produces four reproducible transition phenotypes rather than one universal scalar coefficient.
This is a family-conditioned empirical transition relation, not yet a fundamental physical law. It becomes a physical-law candidate only if the same coefficients/directions predict an independent event-disjoint transition outcome without family redefinition.

NO_GAP_BASED_FAMILY_REBUILD=TRUE
NO_NEW_NODE_DISCOVERY=TRUE
NO_NEW_PATH=TRUE
NO_CANONICAL_R40_CHANGE=TRUE
HOLDOUT30_ACCESSED=FALSE
