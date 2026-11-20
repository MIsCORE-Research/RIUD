# DEV99 forensic-informed branch lock and Holdout5 application

This is a fixed exploratory predictor audit, not a new frozen RIUD scientific law.
The model form was selected from the prior DEV99 mismatch forensic result and fitted only on DEV99 rows. Holdout5 was not used for fitting.

## Locked forms
- MAG: logistic model using S/K5, f_total_variation_hz, network_z_median, f_turns, and support_complexity.
- SHAPE: logistic model using f_turns, transition_entropy, network_z_median, support_complexity, MAG2, ABC indicators, and MAG2×ABC interactions.
- GAP diagnostic branch: predicted MAG2 + ABC in {C, OTHER} + path_nodes <= DEV lower-tertile threshold (9). It is a forensic branch flag, not a refit GAP law.

## Holdout5 applicability
The DEV99 ABC rule was recovered and verified independently on the 96-event DEV99 table (zero label mismatches). Holdout5 GAP was calculated from each canonical Holdout5 path using the existing frozen GAP postprocessor, and MAX_FLOW was calculated from the canonical Holdout5 H1/L1 raw 4-s inputs using the canonical 10-ms center-step, 10-ms lag, GAP±30-ms flow detector. The separate 5-ms refinement branch was excluded. No prior five-event diagnostic landmark table was used and no label was imputed.
The frozen frequency-family definitions are K=2: MAG uses the four frozen frequency variation fields, and SHAPE uses the frozen within-event shape profile. Holdout5 receives fixed-form out-of-sample predictions from DEV99-fitted models; Holdout5 is not used for fitting.

## Claim boundary
The coefficients and branch are frozen for this application only. The output does not establish that the forensic branch is causal, does not modify the canonical map/path, and does not replace the original frozen R40 law.
