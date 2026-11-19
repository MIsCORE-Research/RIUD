# MIsCORE mechanism branch reconciliation

This is a read-only reconciliation of completed R8, R10, R11, R12, and R13
branches. It does not rerun a scientific model and does not alter any frozen
upstream result.

## Scope-separated evidence

| Branch | Object/test | Result | Scientific boundary |
|---|---|---|---|
| R8 | Fixed-grid source-native path/state replay | PATH_FOUND=10/10; N0→A1→G=10/10; G→AR=6/6 among AR-scorable events; 4 unscorable; 0 true failures among scorable | Valid as fixed-grid state-label replay; not a full native physical chronology |
| R10 | Orbital/separation/spin transition registration | 32 RIUD transition rows; separation 10/32; component-spin orientation 10/32; h22 orbital frequency 24/32; remnant orientation 18/32 | Registration exists, but complete transition-wide mechanism test is not established |
| R11 | Common-horizon relaxation phase | Final verdict D_COMMON_HORIZON_REMNANT_PHASE_NOT_SUPPORTED | A sufficient horizon-relaxation explanation was not established |
| R12 | G↔AR phase/hazard relation | 10 source-supported G/AR rows; 4 events with both directions; median paired phase separation 2.1216436214719776; opposite derivative 2/4 | Correlation only; incremental closure of R40 memory not established |
| R13 | Strict native-map/support audit | N0→A1=0/10 in physical support; A1→G=8/10; G→AR=6/6; AR→G=0/6; AR source support missing=6 | Technical hold due missing post-reentry native support; not a contradiction of R8's scorable replay |

## Why the apparent topology disagreement is not a single number to average

R8 scores the previously frozen fixed-grid path/state-label object. R10
registers source-native variables wherever those variables exist. R13 asks a
stricter question: whether the relevant source-native support exists inside
the native-map physical-support domain for each transition. Consequently,
`AR→G=6/6` in R10's transition registration and `AR→G=0/6` in R13's
support-qualified scoring are different denominators and do not license a
claim of complete source-native post-reentry reproduction.

The R13 value `N0→A1=0/10 in physical support` is not an absence of the
transition. The R13 support predicate requires both AhC and waveform support,
whereas all ten N0→A1 rows are explicitly `PRE_COMMON_HORIZON`; the same
rows are therefore present as pre-horizon transitions but cannot be scored by
that post/overlap-qualified source-native predicate. Similarly, the two
A1→G rows outside support are post-common-horizon rows whose source support
is missing.

## Mechanism conclusion

The completed branches support a layered pure-GR-compatible source sequence
and a fixed-grid RIUD structural replay. They do not identify a unique
microscopic generator for the observational semi-Markov memory or frozen S
law. In particular, common-horizon relaxation alone is not sufficient,
orbital/spin support is incomplete across the topology, and post-reentry
native support is not complete under the strict R13 contract.

`R8_FIXED_GRID_REPLAY=SUPPORTED_WITH_SCOPE`

`R10_COMPLETE_ORBITAL_SPIN_MECHANISM=NOT_ESTABLISHED`

`R11_SUFFICIENT_RELAXATION_MECHANISM=NOT_SUPPORTED`

`R12_MEMORY_CLOSURE=NOT_ESTABLISHED`

`R13_FULL_NATIVE_MAP_TOPOLOGY=NOT_ESTABLISHED`

`DIRECT_EINSTEIN_DERIVATION=NOT_ESTABLISHED`

`NEW_PHYSICS=NOT_CLAIMED`
