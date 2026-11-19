# Locked residual paths receive raw-strain and selector-aware complex-phase support across 13 gravitational-wave events

**Author:** [AUTHOR NAME]  
**Affiliation:** Independent researcher / [AFFILIATION TO CONFIRM]  
**Correspondence:** [EMAIL]  
**Version:** Frozen-results draft R0, 2026-08-01

## Abstract

We test whether a set of previously locked time-frequency paths, defined in GR-subtracted residual complex maps for 13 gravitational-wave events, retains support when projected onto independently frozen raw-strain data and when evaluated with an exact selector-aware conditional complex-phase null. No path coordinates are reselected and no raw-strain free search is performed. Across 13 events and 26 H1/L1 strain files, the primary equal-weight fixed-path stack under WHITEN_BP40_400_NOTCH60 yields a stack statistic of 1.171221 with empirical p=9.9999e-6 from 100,000 draws. Support persists without the 60-Hz notch (p=9.9999e-4) and after locked-coordinate ablation (p=1.99998e-5), and all leave-one-event-out evaluations remain below 0.05. A prelocked 62,400-job calibration population gives an internal global statistic of 4.468201 with empirical p=9.9999e-6; four coherent or independent injected nuisance families do not reproduce the baseline population result, whereas single-detector transients remain weaker surviving nuisance classes and are not causally excluded. Direct complex-phase support also survives an exact selector-aware conditional phase-randomization null: the observed zero-direction real component is 0.367157, exceeding all 100,000 null draws (empirical p=9.9999e-6). This phase result is conditional rather than an empirical off-source detector-phase null because the off-source controls contain real H1/L1 selection arrays but no empirical complex phases. These results establish fixed-projection, population-level support for the locked paths in raw strain and conditional cross-event complex-phase support, without identifying the physical origin, completely excluding detector artifacts, or making a GR, beyond-GR, or quantum-gravity claim.

## 1. Introduction

Gravitational-wave parameter estimation removes a modeled compact-binary waveform from detector strain, leaving residual data that are usually treated primarily as a consistency diagnostic. This paper tests a narrower and operational question: whether coordinates locked in residual complex maps retain population support when evaluated in frozen raw strain and whether their cross-event complex phases remain directional under a selector-aware conditional null.

The analysis is intentionally separated into discovery-lock and evaluation layers. The residual paths were fixed before the raw-strain projection. The raw analysis contains no coordinate reselection and no free search. A separate calibration population tests six prelocked nuisance families, and an exact selector-aware randomization test evaluates the direct complex-phase statistic. This structure is designed to constrain overfitting and to preserve a clear claim boundary.

2. Methods

2.1 Frozen analysis contract
The analysis is integration-only. The scientific rules, event set, residual-path coordinates, lag mode, scorer, conditioning variants, selector, and decision rules were frozen before the present integration. Path reselection, raw-strain free search, parameter retuning, and cross-stage reuse were prohibited.

2.2 Event set and locked residual paths
The frozen panel contains 13 events and 172 locked path nodes. Each event contributes a path derived from GR-subtracted residual complex maps. The path provenance, node count, time range, frequency range, width range, residual family, source path, and SHA-256 hash are preserved in the frozen evidence tables.

2.3 Raw-strain fixed-path projection
For each event, 4-s, 4096-Hz H1 and L1 raw-strain files were frozen, giving 26 files in total. The locked residual-path coordinates were projected onto raw strain without a new search. The primary variant is WHITEN_BP40_400_NOTCH60 with equal event weighting. Prespecified robustness variants include canonical raw strain, band-passed strain without the 60-Hz notch, visibility weighting, and a locked-coordinate-drop ablation.

2.4 Population null and leave-one-event-out analysis
Global stack statistics were compared with 100,000-draw empirical nulls. Leave-one-event-out analyses omitted each event in turn. A result was treated as leave-one-event-out robust when every omitted-event empirical p value was at most 0.05.

2.5 Prelocked nuisance-family calibration
The authoritative calibration population contains 62,400 scorer jobs across 104 passing shards, 24 basis-amplitude cells, and 312 locked leave-one-event-out rows. Six nuisance families were evaluated at four prelocked amplitude levels. The primary summary is the median effect across all four levels; no best-amplitude selection was allowed. Internal z values are scorer statistics and must not be interpreted as Gaussian sigma.

2.6 Exact selector-aware conditional complex-phase null
For each event, 200 controls were passed through the same family-path selector, giving 2,600 selector runs. The observed frozen path was reproduced for all 13 events: eight by exact coordinate match and five by an eventwise constant tau-frame equivalence, with maximum absolute shift 0.032 s and maximum residual numerical mismatch 1.2143e-17 s. The primary null randomizes phase conditional on the same-family path being selected. The joint null also incorporates path-existence frequency. Each null uses 100,000 draws.

2.7 Locked decision boundaries
All empirical p values use the finite-draw convention encoded in the frozen outputs. No result is promoted beyond its frozen claim boundary. In particular, the complex-phase control population contains real H1/L1 selector arrays but no empirical complex phases and therefore cannot be described as an empirical off-source detector-phase null.

3. Results

3.1 Frozen residual-path panel
The integrated panel contains 13 events, 172 locked nodes, and frozen provenance for every event. No path was reselected. Event-level locked-path scores are heterogeneous, as expected for a fixed population projection, but the paper-level claim rests on the prespecified population statistics rather than on requiring every event to be individually significant.

3.2 Raw-strain fixed-path population support
The primary equal-weight WHITEN_BP40_400_NOTCH60 stack produced a statistic of 1.171221. None of 100,000 empirical-null draws reached this value, giving p=9.9999e-06. Every leave-one-event-out realization remained below 0.05, with maximum p=5.99994e-05. Thus, the population result is not carried by a single event.

3.3 Conditioning and coordinate-ablation robustness
Support remained under the prespecified no-notch variant (p=0.00099999) and under locked-coordinate removal (p=1.99998e-05). The complete variant panel shows that equal and visibility-weighted assignments preserve the qualitative result across the primary and robustness configurations. These tests address sensitivity to the selected conditioning and coordinate set; they do not constitute a new raw-strain search.

3.4 Calibration against prelocked nuisance families
The 62,400-job baseline population produced an internal global statistic of 4.468201 with empirical p=9.9999e-06. Common-mode linear chirps, common-mode same-phase and opposite-phase injections, and independent detector ringing did not reproduce the baseline population support. H1-only and L1-only transient families remained significant but weaker than baseline across their prelocked amplitude levels. They therefore remain surviving nuisance classes and are not causally excluded.

3.5 Selector-aware complex-phase support
All 13 observed frozen paths were reproduced by the selector. The observed zero-direction real component was 0.367157, the resultant length was 0.367704, and the mean phase was 0.054521 rad. In the primary conditional phase null, none of 100,000 draws exceeded the observed statistic (p=9.9999e-06); the null 99th percentile was 0.163338, and its maximum was 0.341506. The joint selector-plus-path-existence null likewise produced zero exceedances in 100,000 draws (p=9.9999e-06).

3.6 Evidence synthesis
The frozen chain contains three mutually distinct support layers: locked path provenance from residual complex maps; fixed-coordinate support in raw strain with leave-one-event-out and conditioning robustness; and exact selector-aware conditional complex-phase support. Together they show that the locked population structure is not confined to a single residual-map score or a single event. They do not determine what physical or instrumental mechanism generated the structure.

4. Discussion

The central result is deliberately narrower than an origin claim. A residual-derived coordinate set, frozen before the raw-strain analysis, receives population-level support when projected onto H1/L1 raw strain. This matters because it separates coordinate definition from raw-domain evaluation and avoids a second free search in the raw data. The persistence of the result under no-notch conditioning, coordinate ablation, and every leave-one-event-out omission reduces several straightforward explanations based on a single conditioning choice, a small subset of coordinates, or a single dominating event.

The calibration results further constrain interpretation. Four prelocked coherent or independent nuisance families fail to reproduce the baseline population behavior under the locked scoring rule. Single-detector transient families remain weaker but surviving alternatives. The correct conclusion is therefore not that detector artifacts have been eliminated, but that the tested nuisance basis does not provide a complete reproduction of the frozen population result.

The selector-aware complex-phase analysis adds a distinct layer. The observed directional phase statistic exceeds all conditional null draws after the family-path selector is applied under the same rules. However, the off-source controls do not contain empirical complex phases. The phase test is therefore a conditional randomization result and must not be described as an empirical off-source detector-phase measurement. Obtaining a fully empirical off-source complex-phase null would require separately frozen off-source complex-phase assets under a matched acquisition and conditioning contract.

The analysis also does not identify a violation of general relativity. The locked paths were defined in GR-subtracted residual products, but support in residual-derived coordinates is not equivalent to a beyond-GR detection. Waveform imperfection, calibration behavior, unmodeled detector coupling, or another structured nuisance mechanism remain possible. The result motivates independent reproduction using the frozen coordinates and rules rather than interpretive retuning.

5. Conclusion

Across 13 gravitational-wave events, a previously locked residual-path population receives support in frozen raw-strain projections, remains robust under the specified conditioning and coordinate-ablation tests, survives all leave-one-event-out omissions, and exhibits direct complex-phase support under an exact selector-aware conditional null. The result is a reproducible, fixed-projection population finding. Its physical origin remains unidentified.

## Frozen claim boundary

The frozen evidence supports a fixed projection of previously locked residual-path coordinates into raw strain, calibrated population support, robustness to the specified conditioning and coordinate ablation, and a selector-aware conditional complex-phase result. It does not identify the signal origin, does not completely exclude detector artifacts, does not constitute a raw-strain free-search discovery, does not provide an empirical off-source detector-phase null, and does not support a GR-violation, beyond-GR, or quantum-gravity claim.

6. Limitations and required next evidence

1. The complex-phase null is conditional and not an empirical off-source detector-phase null.
2. Single-detector transient families remain weaker surviving nuisance classes.
3. The analysis is a fixed projection and contains no raw-strain free search.
4. The frozen package does not establish a causal signal origin.
5. Internal z values are scorer statistics, not Gaussian-sigma significances.
6. Independent external reproduction has not been supplied in the frozen package.
7. Literature context, detector-state metadata, catalog citations, and journal-specific references are not contained in the frozen input package and must be inserted from verified external sources before submission.

Data and code availability
The present manuscript draft is generated only from the frozen R26C37 and R26C42H integration outputs supplied with the package. Paths and SHA-256 values for the frozen inputs are preserved in the accompanying manifests. Public-data citations, repository URLs, licenses, and executable reproduction instructions are not supplied by the frozen package and remain placeholders for the submission version.

References
[To be populated from verified primary sources only: GWOSC data releases, detector papers, waveform-model references, residual-analysis literature, empirical-randomization methodology, and the archived RIUD code/data release.]
