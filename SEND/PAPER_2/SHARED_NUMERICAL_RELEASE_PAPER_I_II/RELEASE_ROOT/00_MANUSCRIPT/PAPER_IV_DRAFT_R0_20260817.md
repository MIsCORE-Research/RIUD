# RIUD Paper IV

## Population-Level Dynamical Organization and a Frozen Physical Clock in Gravitational-Wave Undiscovered Paths

### From recurrent paths to autonomous state dynamics, latent transition structure, and held-out directional replay

**Jae-Hyun Min**  
Independent Researcher, Republic of Korea  
Draft R0 | 17 August 2026

---

## Abstract

RIUD (Residual Is Undiscovered Data) treats post-model gravitational-wave structure as an observational object whose coordinates, statistical roles, and provenance are separated from later physical interpretation. Papers I–III established three sequential and non-poolable evidential layers: an operationally frozen detector-coherent morphology with explicit falsification history; fixed-coordinate support when later residual-derived paths were projected into H1/L1 raw strain; and control-native evidence for partially shared family-level dynamics. Paper III deliberately stopped short of a universal governing law. The present work asks the next question: when the analysis is expanded from a small frozen family panel to a much larger event population, do the recurrent paths form a population-level dynamical system, and can part of that system be summarized by a frozen physical ordering coordinate and transition clock?

A 99-event development population was processed with the frozen path engine without A2 binding. Structural paths were found in 98/99 events; 58 were rare under eventwise NULL200 controls, 40 were structural but not rare, and one event provided a natural no-path boundary. The resulting frozen representation contains 1,083 nodes and 985 transitions. Path complexity is strongly associated with rarity (Spearman ρ = 0.661980; 0/9,999 permutation exceedances, p = 0.0001). Detector-axis reconstruction produced no interpretation flips across 1,083 nodes, and same-coordinate IMRPhenomXP/IMRPhenomXPHM projection strongly preserved the frozen morphology.

The population is better described by stateful dynamics than by independent eventwise trajectories. A compact additive-memory model supports run-index and state-age dependence, and a multistate representation follows the progression N0→A1→G↔AR. Early common landmarks occur near 10.94%, 14.064%, and 17.188% of the frozen progression coordinate; a later 45.3125% maximum is instead a population-overlap peak and is not treated as a universal landmark. A latent transition coordinate, MT, separates a stable pre-transition regime from a weaker and heterogeneous post-transition regime. Under event-preserving balanced folds, PRE dynamics have macro R² = 0.131234 with all five folds positive and minimum fold R² = 0.106708, whereas POST dynamics have macro R² = 0.033268 and minimum fold R² = −0.104449. Within PRE, predictive structure weakens sharply in the final −20 to 0 ms interval relative to earlier intervals.

A later physical-ordering branch freezes an ordinal coordinate
S = 0.220300 z(R) + 0.345766 z(χ_A),
where R is based on irreducible-mass balance and χ_A is a normalized spin-asymmetry variable. The ordering survives a full-lineage search-aware null (primary p = 0.0006; fixed-score p = 0.0001). Integrating S into the frozen memory-conditioned transition model yields a compact global physical-clock model with coefficient γ = 0.316235. A law-specific search-aware NULL999 gives p = 0.004 for the primary statistic and p = 0.002 for the fixed P1 model. With all parameters frozen, the same law improves predictive log-likelihood and active-ordering direction in all four temporal maps: START→PEAK, PEAK→END, START→MT, and MT→END. Known-physics reduction recovers much, but not all, of the clock behavior: the strongest tested spin-based model recovers 82.64% of the original clock improvement, with horizon-rotation, QNM-relaxation, and area-based models providing partial recovery.

A separately frozen five-event historical validation subset preserves the W1–W3 directional results. W4 retains positive likelihood improvement but not the active-ordering direction; a development resampling audit shows that this ordering statistic is strongly underpowered at n = 4. The held-out numerical result is reproduced by a public frozen-replay package and independently stress-tested by a source-to-final portable package for the affected four frontend events. The evidence supports a population-level RIUD dynamical system with a frozen physical ordering coordinate and transition clock. It does not identify the generating mechanism, establish a physical merger-time identity for the latent transition coordinate, completely exclude detector or waveform systematics, falsify general relativity, or establish Beyond-GR or quantum-gravity physics.

**Keywords:** gravitational waves; residual analysis; Undiscovered data; path dynamics; population system; state memory; latent transition; physical clock; held-out replay; reproducibility

---

## Results at a glance

| Layer | Frozen result | Interpretation |
|---|---:|---|
| DEV99 path population | 98/99 structural paths | Population-scale path object |
| Rarity–complexity | ρ = 0.661980, p = 0.0001 | More complex paths are rarer under matched controls |
| Frozen representation | 1,083 nodes; 985 transitions | Continuous population state space |
| Detector tie audit | 0/1,083 interpretation flips | Same-coordinate interpretation is tie-stable |
| Global dynamics | M3 additive-memory compact model | Transition behavior depends on state history |
| Multistate flow | N0→A1→G↔AR | Recurrent state progression rather than one straight trajectory |
| PRE dynamics | macro R² = 0.131234; 5/5 folds positive | Stable common pre-transition empirical dynamics |
| POST dynamics | macro R² = 0.033268; fold minimum < 0 | Weaker, heterogeneous post-transition dynamics |
| Frozen physical score S | search-aware p = 0.0006 | Physical ordering coordinate survives lineage-aware null |
| Physical clock | γ = 0.316235 | S acts primarily on global transition rate |
| Law-specific null | primary p = 0.004; fixed P1 p = 0.002 | Frozen clock survives search-aware validation |
| Four-map replay | 4/4 positive ΔLogLik; 4/4 same direction | Clock direction is not restricted to one window |
| Known-physics reduction | best clock recovery = 82.64% | Much, but not all, clock behavior maps to tested known physics |
| Historical 5-event replay | W1–W3 direction reproduced; W4 likelihood positive, ordering underpowered | Directional replication with a small-sample boundary |

---

# 1. Introduction

Residual analyses of gravitational-wave observations are usually framed as endpoint diagnostics: after subtraction of a standard waveform description, the remaining data are tested for consistency with detector noise, glitches, calibration uncertainty, or model incompleteness. RIUD adopts a different but narrower operational stance. I regard residuals as undiscovered data. The term *Undiscovered* does not assign a physical origin. It marks a temporary scientific status: structured post-model data are retained as an observational object until evidence classifies them as instrumental, computational, waveform-related, source-related, or otherwise understood.

The first three RIUD papers built that object sequentially. Paper I defined and falsified recurrent detector-coherent morphology, preserved discovery provenance, and blocked several attractive but unsupported physical interpretations. Paper II asked whether later frozen residual-derived paths retained support in H1/L1 raw strain without a second free search, and added a selector-aware conditional complex-phase layer. Paper III then allowed controls to build their own maps, paths, trajectories, and family labels and found repeated partially shared family-level dynamics. The Paper III result was deliberately not promoted to a universal law: a separately frozen compact-law audit failed after the required search correction.

The present paper begins exactly at that boundary. If repeated dynamics exist in several frozen morphology families, the next question is not whether one can force those families into one equation. It is whether a larger population reveals a system-level organization that was invisible in the smaller panel. A population system can be shared without requiring every event to follow the same trajectory, frequency, duration, or physical mechanism. It can instead be expressed through recurrent state transitions, internal progression, variable speed, memory, and a common ordering rule.

The analysis therefore expands to a 99-event development population and proceeds through four conceptual steps. First, a frozen path representation is established at population scale and separated from path rarity. Second, the path population is analyzed as a continuous state system with history and internal progression rather than as eventwise wall-clock traces. Third, a latent transition coordinate and a three-phase temporal organization are used to test where common dynamics are stable or weak. Fourth, a physical-ordering coordinate is frozen and tested as a modifier of the population transition clock, followed by search-aware validation, four-window replay, known-physics reduction, and a separately frozen five-event validation replay.

No p-values are pooled across RIUD Papers I–IV or across the distinct null questions inside this paper. A path-existence null, a rarity–complexity permutation, a physical-coordinate lineage null, a law-specific search-aware null, and a held-out directional replay answer different questions. The central claim is therefore architectural rather than a single-number detection claim: the enlarged RIUD population is organized as a reproducible dynamical system whose transition rate is partially ordered by a frozen physical coordinate. Its generating mechanism remains unresolved.

---

# 2. Sequential relationship to RIUD Papers I–III

**Figure 1. Sequential RIUD architecture.**  
*Paper I: observational object → Paper II: fixed projection → Paper III: family dynamics → Paper IV: population system and frozen clock. Statistical layers remain non-poolable.*

Paper III established three prelocked family-level dynamical hypotheses in a 13-event panel. H1 multistep and H2 oscillatory trajectories supported the same raw/M5 representation, while H3 quasi-stationary trajectories supported raw/M3. Canonical and separately regenerated internal nulls supported all three hypotheses under the frozen thresholds, but the later compact-law audit did not establish one governing law.

Paper IV does not reinterpret that negative result. The Paper III compact-law candidate and the present population physical-clock model are different objects, derived from different event populations, representations, and search contracts. The failure of the Paper III low-dimensional relation is retained as a boundary that motivated, rather than contradicted, the present population expansion.

A DEV61 bridge preceded the 99-event expansion. In that population, shared geometry was already strong: the median observed Spearman relation was 0.8000, and a high-minus-low contrast gave p = 0.005. Tree structure also survived empirical testing, and context-transfer tests preserved a frozen functional relation without refitting. Conversely, GR-only and expanded extrinsic/visibility baselines did not close the population relation. These results are treated here as developmental bridge evidence, not as a second significance layer to be combined with DEV99.

---

# 3. DEV99 path population and frozen representation

## 3.1 Path population

The DEV99 path-only run evaluated 99 development events under the canonical path engine, with eventwise NULL200 controls. A2 binding was disabled and the original execution time origin was MERGER_ZERO. The final population contained:

- 98 events with structural paths;
- 58 rare structural paths;
- 40 structural but non-rare paths;
- one natural no-path event, GW241230_233618;
- zero technical failures.

The no-path event is retained as a natural system boundary. It is not assigned a synthetic trajectory and is not entered into path-PCA or trajectory clustering. Its path score is 0, with 200/200 null exceedances and empirical p = 1.0. Thus, path existence and path rarity are explicitly separated.

**Figure 2. DEV99 population map.**  
*Suggested panels: (A) 99-event path-status strip; (B) rare/non-rare/no-path counts; (C) node-count distribution; (D) representative rare and non-rare paths.*

## 3.2 Continuous frozen representation

Before system discovery, the path population was frozen into a native representation that did not use rarity, GR features, source physical variables, or Paper III family labels. The structural population contains 1,083 frozen node rows and 985 transition rows, with 4–16 nodes per path and a median of 11. The frozen representation includes continuous geometry, transition fingerprints, and fixed-length shape profiles.

This ordering matters. Rarity and source physics are attached only after the geometric state representation is fixed, preventing the physical variables later found to correlate with the system from defining the system in the first place.

## 3.3 Detector and waveform same-coordinate robustness

The detector-axis reconstruction was audited at the exact frozen coordinates. A technical tie/float reconstruction failure in an intermediate attempt produced no scientific result and was superseded by an exact reconstruction. A subsequent tie-invariance audit produced 0/1,083 interpretation flips.

The same frozen coordinates were also evaluated under IMRPhenomXP and IMRPhenomXPHM subtraction families across all 98 structural events. The morphology was strongly preserved under this same-coordinate waveform-family projection. This does not exhaust waveform uncertainty, but it reduces the possibility that the population state representation is an artifact of one trivial detector-tie convention or one of these two subtraction families.

---

# 4. Rarity and structural complexity

Path existence is common in the development population, but rarity is not. The primary population-level structural relation asks whether the complexity of a frozen path is associated with how unusual that path is under its eventwise controls.

The observed node-count–rarity Spearman correlation is

\[
\rho = 0.6619802493.
\]

Under 9,999 permutations, no null replicate equaled or exceeded the observed association, giving the finite-draw empirical value

\[
p = 0.0001.
\]

The result is not that every structural path is rare. Forty of the 98 structural events are explicitly classified as structural but non-rare. Rather, rarity is graded: more structurally complex paths tend to occupy the rarer tail of the matched control distribution.

**Figure 3. Rarity–complexity relation.**  
*Scatter of path complexity versus frozen rarity, with rare/non-rare classes shown only as descriptive overlays. The test is performed on the frozen continuous quantities rather than a post-hoc binary separation.*

This relation supplies the first population bridge from morphology to system organization. A set of unrelated event anomalies need not produce an ordered complexity–rarity relation. At the same time, the result remains observational. It does not identify why complex paths are rare or whether the cause is detector, waveform, source, or a mixture.

---

# 5. Population state space, memory, and autonomous dynamics

## 5.1 From trajectories to states

The enlarged path population was next analyzed as a state system. The key conceptual change is that equal merger-relative milliseconds are not assumed to correspond to equal internal dynamical phase across events. Instead, the analysis asks whether node order, state occupancy, run index, and state age provide a more informative progression coordinate.

The supported multistate flow is summarized as

\[
N0 \rightarrow A1 \rightarrow G \leftrightarrow AR.
\]

This representation allows progression and recurrence rather than forcing every event into one monotonic template.

## 5.2 Additive-memory dynamics

Among compact candidate models, the M3 additive-memory model provides the preferred state-transition description. Its support indicates that the next-state tendency depends not only on the instantaneous state coordinate but also on state history, including run index and state age.

The model reproduces the first three frozen common landmarks at approximately:

- L1 = 10.94%;
- L2 = 14.06421875%;
- L3 = 17.1884375%.

A later maximum at 45.3125% requires different interpretation. Autonomous reconstruction and population accounting show that this late maximum is not a universal eventwise landmark. It is a population-overlap peak produced by heterogeneous event phases occupying the same progression region. Paper IV therefore distinguishes early common landmarks from the late population-overlap maximum.

**Figure 4. State-flow and internal-clock schematic.**  
*Conceptual “lantern” figure: events enter the same frozen state geometry at different external times and traverse it at different speeds. The bright overlap region represents high population occupancy, not a mandatory eventwise landmark. This panel is explanatory, not an inferential statistic.*

## 5.3 Autonomous reconstruction boundary

The frozen M3 rate law passes exact teacher-forced replay and reproduces the early landmark topology in endogenous forward transport, but it does not recover the observed 45.3125% population-overlap peak as a universal autonomous landmark. The model instead peaks too early, near the first turnover. This failure is retained.

The correct interpretation is therefore narrower than “one autonomous equation generates the entire population.” The state-transition law captures early common dynamics and state-history dependence, while later population structure includes heterogeneity that is not fully generated by the compact autonomous model.

---

# 6. Latent transition coordinate and PRE/POST dynamical asymmetry

## 6.1 Frozen MT coordinate

For the frozen PRE/POST analysis, the operational transition coordinate is

\[
MT = \mathrm{LATENT\_COORD}
     - \mathrm{NOMINAL\_ZERO\_LATENT\_POSITION}.
\]

The original event-relative time is retained for audit only and is not used to define the PRE/POST segmentation. PRE is defined by MT < 0 and POST by MT ≥ 0. This is an operational RIUD coordinate; it is not asserted to be an independently measured physical common-horizon formation time.

Transitions crossing the boundary are excluded from the separate PRE and POST fits. The split contains:

- PRE: 730 nodes, 633 transitions, 90 events;
- POST: 347 nodes, 250 transitions, 92 events;
- boundary-crossing transitions excluded: 97.

## 6.2 Event-preserving PRE/POST comparison

After event-preserving fold rebalancing, the PRE empirical vector field remains stable:

\[
R^2_{\rm macro,PRE}=0.131234,
\]

with median fold R² = 0.132662, minimum fold R² = 0.106708, and all five folds positive.

The POST regime is substantially weaker:

\[
R^2_{\rm macro,POST}=0.033268,
\]

with median fold R² = 0.081658 and minimum fold R² = −0.104449.

The result supports a dynamical asymmetry around the operational MT boundary: common empirical dynamics are more reproducible before the transition and become weaker or more heterogeneous afterward.

## 6.3 PRE interval structure

The PRE-only global model contains 633 transitions across 90 events and has macro R² = 0.182188. Its predictive strength is not uniform in time:

| MT interval | n | R² |
|---|---:|---:|
| < −100 ms | 2 | insufficient |
| −100 to −80 ms | 27 | 0.2480 |
| −80 to −60 ms | 191 | 0.2545 |
| −60 to −40 ms | 175 | 0.2135 |
| −40 to −20 ms | 167 | 0.2749 |
| −20 to 0 ms | 71 | 0.0664 |

The final pre-transition interval is therefore qualitatively different from the earlier PRE regime. Predictive organization weakens sharply in the final −20 to 0 ms window rather than strengthening monotonically toward MT.

A subsequent trunk/branch smoke test did not establish a unique common trunk followed by discrete branches. That topology remains inconclusive and is not used as a Paper IV claim.

**Figure 5. PRE/POST split and interval dynamics.**  
*Panel A: latent MT axis with PRE and POST populations. Panel B: event-preserving fold R² for PRE and POST. Panel C: interval-wise PRE R². Panel D: conceptual split schematic showing that the observed population may separate without claiming a confirmed two-branch topology.*

---

# 7. Three-phase temporal organization and the latent depletion

## 7.1 Three-phase organization

A later frozen identity audit supports a three-phase temporal organization of the DEV99 system. The purpose of this stage is not to label a physical inspiral, merger, or ringdown mechanism. It is to test whether the population has reproducible internal landmarks and directional segments that survive frozen replay.

The corresponding temporal views used later in the physical-clock analysis are:

- W1: START → PEAK;
- W2: PEAK → END;
- W3: START → MT;
- W4: MT → END.

These windows are overlapping views of one frozen system, not four independently fitted laws.

## 7.2 Global depletion

A color-free global node atlas contains a complete local depletion interval:

\[
(0.01826073,\;0.01984139)
\]

in the latent coordinate, with width 0.00158066 and zero plotted points where the local expected count is approximately 14.94. The depletion ranks 1/540 by depth, width, and the original combined atlas ranking.

The depletion is not a trivial empty bin created by the original time labels. It appears under the data-derived affine shift/scale mapping, is absent in shift-only and scale-only views, and is not caused by the PRE/POST weighting convention. However, the strength of a gap somewhere in the transformed atlas is not rare under the frozen source-conditional null: 98/99 null realizations equal or exceed the observed depletion score, giving p = 0.99.

The absolute location is more interesting. The observed center is near the nominal zero mapping and showed 0/99 location matches in a later diagnostic, but that branch remains technically held because the exact frozen depletion detector could not be recovered for the required larger null. The gap is therefore reported as an observational transition marker, not as a statistically established physical merger-time detector.

**Figure 6. Latent population split and depletion.**  
*This should be the “split” figure: all mapped population points, the empty vertical interval, and the PRE/POST occupancy on either side. A separate inset may show that the gap strength itself is common under the matched null while the observed location is the unresolved quantity.*

The depletion makes the system-level gap easier to state without overclaiming: there is an empirical separation in the latent atlas, but the present data do not establish that its center equals the physical common-horizon formation time. Source-time and numerical-relativity mapping remain future work.

---

# 8. Frozen physical ordering coordinate

## 8.1 From physical candidates to an ordinal score

Simple physical regime searches did not produce a stable controller. A search over one- and two-dimensional physical regimes gave p = 0.1208 after the required search-aware correction. A distinct-block three/four-way gate using GR-local, mass-scale, and spin information gave p = 0.0961. A nonlinear GR-local phase candidate survived one conditioning method but failed method-robust controller validation. These negative results are retained.

A later physical branch instead asks a weaker question: is there a low-dimensional physical coordinate that orders the frozen population without claiming to explain it?

The primary irreducible-mass feature is

\[
R = \frac{M_{\rm irr,final}}
         {M_{\rm irr,1}+M_{\rm irr,2}}.
\]

A frozen ordinal physical score is then defined as

\[
S =
0.2203003149\,z(R)
+
0.3457660274\,z(\chi_{A,\rm normalized}).
\]

The development association gives observed Spearman ρ = 0.448135 and Kendall τ = 0.314551. Under the full-lineage search-aware NULL9999:

- primary exceedances: 5/9,999, p = 0.0006;
- frozen-score exceedances: 0/9,999, p = 0.0001;
- Kendall exceedances: 1/9,999, p = 0.0002.

This establishes S as a frozen population ordering coordinate under the stated development contract. It does not establish causation or a unique physical mechanism.

---

# 9. Global physical clock

## 9.1 Clock hypothesis

The central physical question is whether S changes the *shape* of the state system or primarily changes how quickly events progress through an already frozen state-transition structure.

Let the frozen M3 memory-conditioned transition predictor be

\[
\eta_{\mathrm{M3},j}(u,\mathrm{age},\mathrm{run}),
\]

where j indexes the transition family. The compact P1 physical-clock extension is

\[
\eta_{e,j}
=
\eta_{\mathrm{M3},j}
+
\gamma S_e,
\]

with

\[
\gamma = 0.3162354634393393.
\]

The transition intensity and probability are

\[
\lambda = \exp(\eta),
\]

\[
p = 1-\exp(-\lambda\,du).
\]

Under the P0–P6 model search, P1 is the best compact model. Its log-likelihood is −1120.5351 and its BIC is 2417.0336, improving on the P0 BIC by 2.6756 in the discovery comparison. More importantly for interpretation, the physical extension changes event-level activity ordering: event-active Spearman rises from a negative baseline relation to 0.393277, with Kendall 0.282341.

The compact interpretation is therefore a *physical clock*: S acts as a global rate modifier on top of the frozen morphology/state dynamics rather than selecting a different morphology for each event.

## 9.2 Law freeze and search-aware validation

The model was frozen as

**RIUD_R39_P1_GLOBAL_PHYSICAL_CLOCK**.

No window-specific refitting is permitted after this freeze.

A law-specific search-aware NULL999 subsequently produced:

- primary search-aware p = 0.004;
- fixed-P1 p = 0.002;
- active-ordering p = 0.001;
- Δactive p = 0.001;
- Kendall p = 0.001.

The most common null winner is P0, and the null distribution of the primary BIC-based discovery statistic is centered well below the observed value. The frozen P1 model therefore survives a null that repeats the allowed model-selection freedom.

**Figure 7. Frozen physical clock.**  
*Panel A: S distribution/order; Panel B: physical-clock model schematic; Panel C: observed primary statistic within the search-aware NULL999; Panel D: event-active ordering under P0 and P1.*

---

# 10. Four-map frozen predictive replay and coverage

## 10.1 Frozen temporal maps

The frozen physical clock was replayed without refitting across four temporal views:

| Map | Events | Transitions | ΔLogLik | ΔActive |
|---|---:|---:|---:|---:|
| W1 START→PEAK | 97 | 723 | +2.598373 | +0.124571 |
| W2 PEAK→END | 94 | 163 | +4.598773 | +0.005631 |
| W3 START→MT | 97 | 725 | +2.461908 | +0.073583 |
| W4 MT→END | 92 | 250 | +4.735239 | +0.001539 |

All four maps improve frozen predictive log-likelihood, and all four have the same active-ordering direction.

An initial map-level interpretation used BIC signs and appeared mixed. A later semantics audit showed that all model parameters, including γ, were already frozen and that P1 was being penalized again as if the physical parameter had been re-estimated inside each map. Because no window-specific parameter is fitted, the primary frozen-replay comparison is predictive log-likelihood rather than a second model-selection penalty. The earlier mixed BIC interpretation is therefore not used as the primary map verdict.

## 10.2 Coverage envelope

A master coverage bank evaluates the frozen clock over a wider set of windows. Directional support extends deep into the front and back portions of the progression coordinate rather than existing only at one hand-selected boundary. The largest tested front start retaining direction is 80%, and the minimum tested back end retaining direction is 60%, within the frozen coverage contract.

This coverage analysis is descriptive of the domain over which the already-frozen clock retains its direction. It is not a new law search.

**Figure 8. Four-map clock replay.**  
*Four aligned panels with ΔLogLik and ΔActive for W1–W4, plus a narrow coverage strip showing the directional-validity envelope.*

---

# 11. Known-physics reduction

A frozen empirical coordinate is scientifically more useful if its relation to known quantities is tested directly. The known-physics reduction therefore asks how much of S itself, and how much of the physical-clock improvement, can be reconstructed from familiar mass, spin, horizon, and QNM quantities.

For the physical score S, the best tested single variable is normalized spin asymmetry, with R² ≈ 0.6954. The best tested composite for the *shape of S* combines horizon rotation with spin asymmetry and reaches R² ≈ 0.7587. Thus approximately 24.13% of the variance of S remains outside the best tested known-physics composite.

The clock function gives a different ordering. The best tested clock surrogate is χ_eff + χ_A, with ΔLogLik = 4.410718 compared with the original S-clock ΔLogLik = 5.336951. The corresponding recovery fraction is approximately 0.826449, leaving about 17.36% of the original clock improvement unrecovered by the best tested known-physics clock surrogate.

The theory-mechanism scorecard gives:

- spin/hang-up family: 82.64% clock recovery;
- horizon rotation: 79.61%;
- QNM relaxation: 78.18%;
- horizon area: 67.63%.

These values show that the clock is substantially connected to known merger physics. They do not show that one known-physics quantity fully replaces the frozen RIUD coordinate. The best variables for reconstructing the *shape of S* and for reconstructing its *clock function* are not identical.

A natural interpretation is that S may compress information connecting binary spin history, merger evolution, and final-horizon state. This is an interpretation, not a causal identification.

**Figure 9. Known-physics reduction scorecard.**  
*Bars for spin, horizon rotation, QNM, and area clock recovery; separate inset for S-shape R². Keep the two quantities visually distinct.*

---

# 12. Frozen five-event validation replay

## 12.1 Validation role

The final directional check uses a separately frozen five-event historical validation subset:

- GW241114_024711;
- GW240830_211120;
- GW240612_081540;
- GW241130_110422;
- GW250119_190238.

This subset is treated as a frozen validation replay, not as a prospectively untouched 30-event study and not as a new law-discovery population. The remaining untouched reserve is not used in the present paper.

The law, γ, temporal maps, likelihood definition, active-ordering statistic, and coverage contract are fixed before the final replay.

## 12.2 Results

The final five-event replay gives:

| Window | ΔLogLik | Direction |
|---|---:|---|
| W1 START→PEAK | +1.1043334444 | True |
| W2 PEAK→END | +0.2230157037 | True |
| W3 START→MT | +1.0415943943 | True |
| W4 MT→END | +0.1348864351 | False for active ordering |

The frozen likelihood direction is positive in all four windows. The active-ordering direction reproduces in W1–W3 and does not reproduce in W4.

The W4 result is not rewritten as a full failure of the frozen law. The active-ordering statistic is based on only four scorable events in that window. A DEV resampling audit at n = 4 finds a failure rate of approximately 0.8735 for the W4 active-ordering direction. The appropriate frozen verdict is therefore:

**W1–W3 frozen directions reproduced; W4 likelihood direction reproduced, while active ordering is underpowered.**

No combined p-value is computed across the four windows.

**Figure 10. DEV-to-validation replay.**  
*Four window arrows with DEV ΔLogLik/ΔActive above and validation ΔLogLik/direction below. W4 should be visually marked “positive likelihood; ordering underpowered,” not red-failed.*

---

# 13. Reproducibility

The Paper IV result has two public reproduction levels.

The primary public frozen-replay package reproduces the reported Holdout5 analysis from archived sufficient analysis artifacts. It physically contains the Panel13 residual reference set (52 residuals), the frozen DEV97 sufficient global-system assets, the downstream rules, the Holdout5 frozen reproduction inputs, runtime records, manifests, and hashes. It has no external runtime dependency on the original research archive.

A deeper portable source-to-final package separately demonstrates the frontend on the four Holdout5 events whose IMRPhenomXP residual lineage required rebuilding. In an isolated smoke test, the package opens packaged RAW/PE/LONG inputs, regenerates residuals, generates NULL200, creates nodes and paths, and evaluates the frozen law without using the original research root. The fifth event was not packaged source-to-final and remains represented by its validated frozen downstream assets.

The rebuilt frontend preserves the historical scientific result: node coordinates, path structure, and window directions remain consistent, with the final W1–W4 values unchanged. The current reproducible runtime is frozen as a new reproducible execution environment; it is not claimed to be byte-identical to the original historical runtime.

This distinction is important. Reproducibility of the reported frozen statistics does not require redistribution of the full private research archive. Large public source datasets can be referenced by provenance while sufficient frozen artifacts are distributed directly.

---

# 14. Negative results and frozen claim boundary

The Paper IV system claim is strengthened by branches that did not survive.

1. **Simple physical regimes.**  
   A one/two-dimensional physical regime search did not survive the required look-elsewhere correction (p = 0.1208).

2. **Hard physical multigates.**  
   A mass-scale + spin + GR-local three-block candidate did not survive search-aware testing (p = 0.0961).

3. **GR-local phase controller.**  
   A nonlinear-conditioned GR-local phase candidate survived one method but failed cross-method controller robustness and is not promoted.

4. **Gap strength.**  
   The strongest visible latent depletion ranks first in the observed atlas but gap strength itself is common under the matched null (p = 0.99).

5. **Gap physical identity.**  
   The latent depletion is a candidate transition marker. Exact identity with physical merger/common-horizon formation is not established.

6. **Pure-GR population origin.**  
   A Pure-GR smoke event can produce a locally rare RIUD path, demonstrating that rare structure is not automatically Beyond-GR. The full GR97 population origin audit is incomplete and is not used as a Paper IV conclusion.

7. **SXS source-time bridge.**  
   Direct mapping from the latent transition to a numerical-relativity source-waveform merger marker remains technically unresolved.

8. **Autonomous completeness.**  
   The compact memory model reproduces early topology but does not generate the late 45.3125% population-overlap maximum as a universal landmark.

9. **Known-physics closure.**  
   Spin, horizon rotation, QNM, and area variables explain substantial fractions of the physical-clock behavior but do not fully replace the frozen empirical coordinate under the tested models.

Accordingly, the evidence **supports**:

- a population-scale structural path object;
- a strong rarity–complexity relation;
- detector- and tested waveform-family same-coordinate stability;
- stateful and memory-dependent population dynamics;
- a stable pre-transition empirical regime;
- a frozen physical ordering coordinate;
- a frozen global transition-clock model surviving search-aware validation;
- directional support across four temporal maps;
- W1–W3 directional reproduction in a separately frozen five-event validation subset;
- partial reduction of the clock to known physics;
- reproducibility from public frozen sufficient artifacts.

The evidence **does not establish**:

- the physical identity of the Undiscovered structures;
- a unique detector, waveform, or source mechanism;
- a physical common-horizon interpretation of MT or the latent depletion;
- a universal deterministic trajectory followed by every event;
- catalog-wide prevalence;
- complete artifact exclusion;
- falsification of general relativity;
- Beyond-GR, quantum-gravity, or string-theory physics;
- independent external-team replication.

---

# 15. Discussion

The principal transition from Paper III to Paper IV is a change of scientific object. Paper III asked whether several frozen morphology families exhibit repeated dynamics under controls with the same freedom to construct paths. Paper IV asks whether a much larger population can be represented as one system without erasing event heterogeneity.

The answer is not a universal template. Structural paths appear in 98/99 development events, but only 58 are rare; complexity and rarity form a continuous relation. State transitions depend on memory and internal progression. Early landmarks are shared, while a later population maximum is an overlap phenomenon rather than a universal eventwise phase. PRE dynamics are stable across event-preserving folds, POST dynamics are weaker and mixed, and the final pre-transition interval loses much of the predictive structure seen earlier. These results are more consistent with a population of variable-speed trajectories moving through a shared state architecture than with either thirteen unrelated anomalies or one rigid waveform-like trajectory.

The latent depletion helps visualize this architecture. The atlas contains a real empty interval between densely occupied regions, making the PRE/POST separation geometrically explicit. Yet the matched null shows that a strong gap somewhere is not rare. The scientifically useful statement is therefore not “the gap proves merger.” It is that the frozen system contains an observational transition boundary whose physical timing remains to be identified.

The physical-clock result adds a second layer. The frozen score S does not simply replace the state representation with source metadata. It modifies the rate of an already frozen memory-conditioned system. This distinction is why the clock interpretation is stronger than a generic correlation between source parameters and one residual feature. The law-specific search-aware null and the four frozen temporal maps show that the direction is not restricted to one window chosen after inspection.

At the same time, the known-physics scorecard argues against a simplistic new-physics interpretation. Spin-based variables recover most of the clock improvement, and horizon-rotation and QNM quantities recover substantial fractions. The residual information is therefore better described as incompletely reduced to the tested known-physics coordinates than as evidence for a known-theory failure. A useful future theory problem is to determine whether the remaining empirical coordinate corresponds to a more faithful combination of binary spin history, merger dynamics, waveform incompleteness, or detector-conditioned observability.

The five-event replay is intentionally modest. W1–W3 reproduce the frozen direction, while W4 retains positive likelihood support but lacks the active-ordering direction in a window with only four scorable events. Development resampling shows that this particular ordering statistic is expected to fail frequently at that sample size. The result therefore neither rescues W4 by redefining success nor discards the entire frozen clock because one underpowered secondary metric fails.

The overall RIUD sequence can now be summarized as:

**object → projection → family dynamics → population system → physical clock.**

Each arrow represents a different question and a different statistical role. None requires pooling the previous p-values. The strength of the program lies instead in preserving the same observational object while repeatedly changing the question asked of it.

---

# 16. Conclusion

A 99-event development expansion transforms RIUD from a small set of recurrent residual-path families into a population-level dynamical system. Structural paths are present in 98/99 events, their complexity is strongly associated with rarity, and their frozen same-coordinate interpretation is stable under detector-tie and tested waveform-family perturbations. The population admits a continuous state representation with additive memory, recurrent multistate flow, and early common progression landmarks. A latent MT split reveals stable pre-transition dynamics and weaker post-transition behavior, with a sharp reduction in predictive organization during the final pre-transition interval.

A frozen physical ordering coordinate built from irreducible-mass balance and spin asymmetry survives a full-lineage search-aware null. When added to the frozen memory-conditioned transition system, it acts as a compact global physical clock with γ = 0.316235. The clock survives a separate search-aware NULL999 and improves frozen predictive likelihood and active-ordering direction across START→PEAK, PEAK→END, START→MT, and MT→END views without window-specific refitting. Known spin, horizon-rotation, QNM, and area variables recover substantial but incomplete fractions of this behavior.

A frozen five-event validation replay reproduces the W1–W3 directions; W4 retains positive likelihood improvement while its active-ordering statistic is strongly underpowered at the available sample size. Public frozen-replay and source-to-final verification packages preserve the numerical result without requiring redistribution of the full research archive.

The strongest defensible conclusion is therefore system-level rather than mechanism-level: recurrent gravitational-wave Undiscovered paths behave as an organized, memory-bearing population whose transition rate is partially ordered by a frozen physical coordinate. The physical origin of that organization remains open.

---

# 17. Data, code, and reproducibility

The analysis uses publicly released gravitational-wave strain, catalog, and parameter-estimation products together with frozen RIUD intermediate artifacts and manifests. Large public source datasets are not unnecessarily duplicated in the primary reproduction archive.

The primary Paper IV public package reproduces the reported frozen analyses from archived sufficient analysis artifacts. It includes the frozen analysis engine, Panel13 reference residuals, frozen DEV97 sufficient global-system artifacts, Holdout5 frozen reproduction assets, rules, manifests, hashes, and a clean public verifier.

A separate portable source-to-final package demonstrates the validated current frontend on four affected Holdout5 events using packaged RAW, PE, and long-control inputs. That package regenerates residuals, event NULL200 structures, nodes, paths, and frozen-law outputs without dependence on the original research root.

The current reproducible runtime is version-frozen but is not claimed to be the historical runtime. Original research archives remain preserved separately. Exact package names and SHA-256 values should be inserted from the final public master manifest before submission.

---

# Appendix A. Proposed figure list

1. **Sequential RIUD I→IV architecture**  
   Object → fixed projection → family dynamics → population system/clock.

2. **DEV99 path population**  
   98 structural / 1 no-path; rare vs non-rare; node-count distribution.

3. **Rarity–complexity relation**  
   Frozen continuous relation and permutation null.

4. **Internal-clock / “lantern” schematic**  
   Shared state geometry, variable event speeds, early landmarks, late population-overlap peak.

5. **MT split and PRE interval dynamics**  
   PRE/POST fold performance plus interval R².

6. **Latent depletion / split population**  
   The gap figure. Show observed depletion and explicitly separate strength-null from location interpretation.

7. **Frozen physical score and law-specific null**  
   S ordering, γ clock equation, NULL999.

8. **Four-map frozen replay**  
   W1–W4 ΔLogLik and ΔActive.

9. **Known-physics reduction scorecard**  
   Spin / horizon rotation / QNM / area recovery.

10. **DEV→five-event frozen replay**  
    W1–W3 reproduced; W4 positive likelihood + underpowered ordering.

---

# Appendix B. Numerical lock table

| Quantity | Frozen value |
|---|---:|
| DEV99 events | 99 |
| Structural paths | 98 |
| Rare structural | 58 |
| Structural non-rare | 40 |
| No-path | 1 |
| Frozen nodes | 1,083 |
| Frozen transitions | 985 |
| Complexity–rarity ρ | 0.6619802493 |
| Complexity–rarity p | 0.0001 |
| PRE macro R² | 0.131234 |
| PRE fold min R² | 0.106708 |
| POST macro R² | 0.033268 |
| POST fold min R² | −0.104449 |
| S Spearman | 0.4481346864 |
| R38 primary p | 0.0006 |
| R38 fixed-score p | 0.0001 |
| Physical-clock γ | 0.3162354634 |
| R41 primary p | 0.004 |
| R41 fixed P1 p | 0.002 |
| W1 DEV ΔLogLik | +2.5983730031 |
| W2 DEV ΔLogLik | +4.5987734502 |
| W3 DEV ΔLogLik | +2.4619078574 |
| W4 DEV ΔLogLik | +4.7352385959 |
| W1 validation ΔLogLik | +1.1043334444 |
| W2 validation ΔLogLik | +0.2230157037 |
| W3 validation ΔLogLik | +1.0415943943 |
| W4 validation ΔLogLik | +0.1348864351 |
| Best known clock recovery | 0.8264490904 |
| S unexplained variance fraction | 0.2413405098 |

---

## Editorial notes before integration into Papers I–IV

- Do **not** rename the frozen PRE/POST MT coordinate as a proven physical merger time.
- Keep the gap as an observational candidate transition marker; gap strength itself has p = 0.99.
- Do **not** call the PRE trunk/branch topology confirmed.
- Do **not** combine Paper III compact-law failure with the Paper IV physical-clock result; they are different frozen objects.
- Do **not** use the late 45.3125% population-overlap peak as a universal landmark.
- In the four-map section, predictive ΔLogLik is primary because all parameters are frozen and no window-specific γ is fitted.
- The five-event replay is a frozen historical validation subset, not the untouched 30-event reserve.
- Keep the public frozen replay and the deeper source-to-final package as two distinct reproducibility tiers.
