# RIUD Paper5 complete lineage and scientific boundary

Generated: 2026-08-22
Scope: all local directories whose names begin with RIUD_PAPER5 under E:\RIUD_ACTIVE_20260808.
Original Paper5 folders and scientific outputs were not modified.

## One-line lineage

anchor-extension preflights/retries
 -> canonical two-anchor extended candidate bank
 -> frozen Figure-6 color-free depletion recovery
 -> blind two-anchor gap/time reveal
 -> extended-path and W1-front-boundary replay
 -> support-gap / M-Time candidate audits
 -> terminology correction and W0/W1/W2/W3/W4 map freeze
 -> full-map frozen physical-clock replay
 -> W0/raw trigger and model-absorption diagnostics
 -> known-physics/QNM/thermodynamic/component/multi-law audits
 -> frozen internal-law extraction
 -> GR/waveform-model comparison.

## Main frozen numerical objects

- Figure-6 color-free latent gap: left=0.0182607298884202, right=0.0198413898273119, width=0.0015806599388917021, midpoint=0.01905105985786605.
- Global map: 1077 plotted rows, 97 events, physical-S support=96.
- Frozen law: S = 0.22030031492055946*z(R) + 0.3457660274266933*z(CHI_A_NORMALIZED).
- R = M_irr,final/(M_irr,1 + M_irr,2).
- CHI_A_NORMALIZED = (chi1z-chi2z)/(abs(chi1z)+abs(chi2z)).
- Frozen clock: gamma=0.3162354634393393; lambda=exp(eta); p=1-exp(-lambda*du); du=0.031250000000000125.
- Frozen state graph: N0->A1; A1->G; G->AR; AR->G.

## Anchor extension and W1 correction

The canonical W1-front file is RIUD_PAPER5_GW231221_W1_FRONT_BOUNDARY_SCAN_R0_20260820.
For GW231221_135041, original W1 starts at tau=-0.02 s and the extended support reaches tau=-0.11 s. W1 transitions increase 12 -> 14, but DeltaLogLik changes -0.6507951152402445 -> -0.779269585710443. The added front contribution is -0.12847447047019855. The file explicitly records W0_INTERPRETATION=ABSORBED_AS_W1_FRONT_EXTENSION and W1_EXTENDS_TO_FRONT_LIMIT. This is not a universal W0 law.

The two-anchor extension adds 21 new nodes to GW240601_061200 and 22 to GW231221_135041. No new node enters the frozen Figure-6 gap. The gap survives both extensions. The extended W4 rows remain directionally compatible, but this does not make the whole extended dynamics uniformly better: GW240601 total DeltaLogLik improves -0.8372678024253029 -> -0.7437353745475059, while GW231221 worsens -0.3552289826723811 -> -0.4837034531425788.

## GAP / M-Time boundary

The frozen gap survives extension, but its native-time relation to nominal t0 is not a physical merger-time confirmation. M-Time is frozen as a reproducible waveform-native temporal landmark / candidate; physical identity remains open. The blind gap audit found no common midpoint alignment between the two anchors and reported GAP_PRESENT_MT_T0_MIDPOINT_NOT_SUPPORTED.

## Corrected map terminology

- W0: extension-only prefix / sparse diagnostic; not a separately fitted law.
- W1: canonical start-to-peak; the GW231221 front scan shows the available W1 support extends to the front limit.
- W2: frozen peak-to-end.
- W3: frozen start-to-event-specific MT0; its post-gap tail is a local structural breakdown/limitation, not a merger-time identity.
- W4: frozen MT0-to-end.
- W5: post-extension diagnostic where present.

Full 97-event global replay reports W1/W2/W3/W4 positive DeltaLogLik and common direction, while W0 has only sparse support (2 transitions, one nonzero event) and is not identifiable as a separate law.

## Raw and known-physics branches

Raw audits found a fixed oscillation/zero-crossing activity -> frequency relaxation -> envelope-rise sequence as a descriptive trigger candidate. It is not a causal or universal trigger proof. The strongest all-known-physics descriptive associations were modest (maximum absolute Spearman about 0.2749 for the spectral-centroid endpoint and 0.2851 for envelope-rise delay). The frozen QNM-scale basis was insufficient for the raw sequence/S. The direct nonlinear mode-coupling test stopped at technical hold because the required mode-resolved frozen asset did not exist. Residual-to-S source identity was not established from the frozen assets.

## Final Paper5 claim boundary

The final internal result is an empirically supported frozen RIUD transition-hazard relation in its main domain W1/W2/W3-pre-gap/W4, with W0 as a single-event activation candidate and W3-post-gap as a local interruption/breakdown. Existing GR/waveform models are partially consistent in shared input physics but are not directly comparable as the same hazard law or coordinate. No causal W0 claim, physical merger-time identification, GR falsification, or new-physics claim is established.

## Branch classification

- MAIN: canonical anchor extension, Figure-6/gap evidence, W1-front correction, M-Time freeze, corrected map terminology, full-map frozen law replay, final internal-law extraction, final existing-physics comparison.
- DIAGNOSTIC: W0 trigger/raw sequence, raw-to-S crosswalk, component/multi-law/thermodynamic/known-physics/QNM audits, five-panel and selected-PE audits.
- TECHNICAL_HOLD: physical MT confirmation, pre-W0 exact model-absorption comparison, direct nonlinear mode-coupling test.
- SUPERSEDED: anchor retries, old W1-0/W3-MT terminology, early cross-event W0 trigger framing, pre-correction phase partition, non-parallel raw trigger audit.

## Explicit exclusions

No Holdout30 access is recorded in the Paper5 folders. No new S/gamma/law/null/refit was used in the final internal-law extraction or model comparison.

See PAPER5_STAGE_CATALOG.tsv for every Paper5 folder and PAPER5_AUTHORITY_FILE_INDEX.tsv for selected source-of-truth files and hashes.
